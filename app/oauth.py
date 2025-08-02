import logging
import secrets
from datetime import datetime, timedelta
from typing import Any, Dict, Optional

import httpx
from authlib.integrations.starlette_client import OAuth
from fastapi import Cookie, Depends, HTTPException, Request, Response, status
from itsdangerous import BadSignature, SignatureExpired, URLSafeTimedSerializer
from pydantic import BaseModel

from app.config import get_settings

logger = logging.getLogger(__name__)


class User(BaseModel):
    id: str
    username: str
    acct: str
    display_name: str
    is_admin: bool
    avatar: Optional[str] = None


class OAuthConfig:
    def __init__(self, settings):
        self.settings = settings
        self.oauth = OAuth()
        
        if not all([settings.OAUTH_CLIENT_ID, settings.OAUTH_CLIENT_SECRET, settings.SESSION_SECRET_KEY]):
            logger.warning("OAuth not fully configured - admin features will be unavailable")
            self.configured = False
            return
            
        self.configured = True
        
        # Register Mastodon OAuth client
        self.oauth.register(
            name='mastodon',
            client_id=settings.OAUTH_CLIENT_ID,
            client_secret=settings.OAUTH_CLIENT_SECRET,
            authorize_url=f"{settings.INSTANCE_BASE}/oauth/authorize",
            access_token_url=f"{settings.INSTANCE_BASE}/oauth/token",
            client_kwargs={
                'scope': 'read:accounts',
            },
        )
        
        # Session serializer for secure cookies
        self.serializer = URLSafeTimedSerializer(settings.SESSION_SECRET_KEY)

    def create_session_token(self, user_data: Dict[str, Any]) -> str:
        """Create a signed session token"""
        return self.serializer.dumps(user_data)

    def verify_session_token(self, token: str, max_age: int = None) -> Dict[str, Any]:
        """Verify and decode session token"""
        if max_age is None:
            max_age = self.settings.SESSION_COOKIE_MAX_AGE
        
        try:
            return self.serializer.loads(token, max_age=max_age)
        except (BadSignature, SignatureExpired) as e:
            logger.debug(f"Invalid session token: {e}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired session"
            )

    async def fetch_user_info(self, access_token: str) -> Optional[User]:
        """Fetch user information from Mastodon API"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.settings.INSTANCE_BASE}/api/v1/accounts/verify_credentials",
                    headers={"Authorization": f"Bearer {access_token}"},
                    timeout=10.0
                )
                
                if response.status_code != 200:
                    logger.warning(f"Failed to fetch user credentials: {response.status_code}")
                    return None
                
                data = response.json()
                
                # Check if user has admin role
                is_admin = bool(data.get("role", {}).get("permissions", 0) & 1)  # Admin permission bit
                
                # Fallback: check if user has elevated permissions
                if not is_admin:
                    # Some instances might use different role structures
                    role_name = data.get("role", {}).get("name", "").lower()
                    is_admin = role_name in ["admin", "moderator", "owner"]
                
                return User(
                    id=data["id"],
                    username=data["username"],
                    acct=data["acct"],
                    display_name=data.get("display_name", data["username"]),
                    is_admin=is_admin,
                    avatar=data.get("avatar")
                )
                
        except Exception as e:
            logger.error(f"Error fetching user info: {e}")
            return None


# Global OAuth config instance
_oauth_config: Optional[OAuthConfig] = None


def get_oauth_config() -> OAuthConfig:
    """Get the global OAuth configuration"""
    global _oauth_config
    if _oauth_config is None:
        _oauth_config = OAuthConfig(get_settings())
    return _oauth_config


def get_current_user(
    request: Request,
    session_cookie: Optional[str] = Cookie(None, alias=None)  # Will be dynamically set
) -> Optional[User]:
    """Get current user from session cookie"""
    oauth_config = get_oauth_config()
    
    if not oauth_config.configured:
        return None
    
    # Get cookie name from settings
    settings = get_settings()
    cookie_name = settings.SESSION_COOKIE_NAME
    
    # Extract session token from cookie
    session_token = request.cookies.get(cookie_name)
    
    if not session_token:
        return None
    
    try:
        user_data = oauth_config.verify_session_token(session_token)
        return User(**user_data)
    except HTTPException:
        return None


def require_admin(current_user: Optional[User] = Depends(get_current_user)) -> User:
    """Dependency that requires an authenticated admin user"""
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required"
        )
    
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    
    return current_user


def require_authenticated(current_user: Optional[User] = Depends(get_current_user)) -> User:
    """Dependency that requires any authenticated user"""
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required"
        )
    
    return current_user


def create_session_cookie(response: Response, user: User, settings) -> None:
    """Create and set session cookie"""
    oauth_config = get_oauth_config()
    session_token = oauth_config.create_session_token(user.model_dump())
    
    response.set_cookie(
        key=settings.SESSION_COOKIE_NAME,
        value=session_token,
        max_age=settings.SESSION_COOKIE_MAX_AGE,
        httponly=True,
        secure=str(settings.INSTANCE_BASE).startswith("https://"),
        samesite="lax"
    )


def clear_session_cookie(response: Response, settings) -> None:
    """Clear session cookie"""
    response.set_cookie(
        key=settings.SESSION_COOKIE_NAME,
        value="",
        max_age=0,
        httponly=True,
        secure=str(settings.INSTANCE_BASE).startswith("https://"),
        samesite="lax"
    )
