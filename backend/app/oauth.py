import logging
from typing import Any

try:
    from authlib.integrations.starlette_client import OAuth

    AUTHLIB_AVAILABLE = True
except ImportError:
    AUTHLIB_AVAILABLE = False

    # Create a dummy OAuth class for testing environments
    class OAuth:
        def register(self, **kwargs):
            pass


from app.config import get_settings
from app.mastodon_client import MastoClient
from fastapi import Cookie, Depends, HTTPException, Request, Response, status
from itsdangerous import BadSignature, SignatureExpired, URLSafeTimedSerializer
from pydantic import BaseModel

logger = logging.getLogger(__name__)


class User(BaseModel):
    id: str
    username: str
    acct: str
    display_name: str
    is_admin: bool
    avatar_url: str | None = None


class OAuthConfig:
    def __init__(self, settings):
        self.settings = settings

        if not AUTHLIB_AVAILABLE:
            logger.warning("authlib not available - OAuth admin features will be unavailable")
            self.configured = False
            return

        self.oauth = OAuth()

        if not all([settings.OAUTH_CLIENT_ID, settings.OAUTH_CLIENT_SECRET, settings.SESSION_SECRET_KEY]):
            logger.warning("OAuth not fully configured - admin features will be unavailable")
            self.configured = False
            return

        self.configured = True

        # Register Mastodon OAuth client
        self.oauth.register(
            name="mastodon",
            client_id=settings.OAUTH_CLIENT_ID,
            client_secret=settings.OAUTH_CLIENT_SECRET,
            authorize_url=f"{settings.INSTANCE_BASE}/oauth/authorize",
            access_token_url=f"{settings.INSTANCE_BASE}/oauth/token",
            client_kwargs={"scope": settings.OAUTH_SCOPE},
        )

        # Session serializer for secure cookies
        self.serializer = URLSafeTimedSerializer(settings.SESSION_SECRET_KEY)

    def create_session_token(self, user_data: dict[str, Any]) -> str:
        """Create a signed session token"""
        return self.serializer.dumps(user_data)

    def verify_session_token(self, token: str, max_age: int = None) -> dict[str, Any]:
        """Verify and decode session token"""
        if max_age is None:
            max_age = self.settings.SESSION_COOKIE_MAX_AGE

        try:
            return self.serializer.loads(token, max_age=max_age)
        except (BadSignature, SignatureExpired) as e:
            logger.debug(f"Invalid session token: {e}")
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired session")

    async def fetch_user_info(self, access_token: str) -> User | None:
        try:
            client = MastoClient(access_token)
            data = await client.verify_credentials()
            is_admin = False
            role_data = data.get("role")
            if role_data:
                try:
                    permissions = int(role_data.get("permissions", 0))
                    is_admin = bool(permissions & 1)
                except (ValueError, TypeError):
                    pass
                if not is_admin:
                    role_name = (role_data.get("name") or "").lower()
                    is_admin = role_name in ["admin", "moderator", "owner"]
            return User(
                id=data["id"],
                username=data["username"],
                acct=data["acct"],
                display_name=data.get("display_name") or data["username"],
                is_admin=is_admin,
                avatar_url=data.get("avatar"),
            )
        except Exception as e:
            logger.error(f"Error fetching user info: {e}")
            return None


# Global OAuth config instance
_oauth_config: OAuthConfig | None = None


def get_oauth_config() -> OAuthConfig:
    """Get the global OAuth configuration"""
    global _oauth_config
    if _oauth_config is None:
        _oauth_config = OAuthConfig(get_settings())
    return _oauth_config


def get_current_user(
    request: Request,
    session_cookie: str | None = Cookie(None, alias=None),  # Will be dynamically set
) -> User | None:
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


def require_admin(current_user: User | None = Depends(get_current_user)) -> User:
    """Dependency that requires an authenticated admin user"""
    if not current_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication required")

    if not current_user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin access required")

    return current_user


def require_authenticated(current_user: User | None = Depends(get_current_user)) -> User:
    """Dependency that requires any authenticated user"""
    if not current_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication required")

    return current_user


def require_admin_hybrid(current_user: User | None = Depends(get_current_user)) -> User:
    """Dependency that requires an authenticated admin user (hybrid OAuth/API key)."""
    if not current_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication required")

    if not current_user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin access required")

    return current_user


def create_session_cookie(response: Response, user: User, settings) -> None:
    """Create and set session cookie"""
    oauth_config = get_oauth_config()
    session_token = oauth_config.create_session_token(user.model_dump())

    # In development, we're always using HTTP for the local server
    # regardless of what the INSTANCE_BASE (Mastodon server) uses
    is_development = True  # Always use non-secure cookies in development

    logger.info(
        f"Creating session cookie: name={settings.SESSION_COOKIE_NAME}, "
        f"secure={not is_development}, domain=None, path=/"
    )

    response.set_cookie(
        key=settings.SESSION_COOKIE_NAME,
        value=session_token,
        max_age=settings.SESSION_COOKIE_MAX_AGE,
        path="/",  # Ensure cookie is sent for all paths
        httponly=True,
        secure=False,  # Always allow non-HTTPS in development
        samesite="lax",  # Keep it as lax for development
    )


def clear_session_cookie(response: Response, settings) -> None:
    """Clear session cookie"""
    # Don't use secure cookies in development (HTTP)
    is_development = str(settings.INSTANCE_BASE).startswith("http://")

    response.set_cookie(
        key=settings.SESSION_COOKIE_NAME,
        value="",
        max_age=0,
        path="/",
        httponly=True,
        secure=not is_development,  # Only secure in production (HTTPS)
        samesite="lax",
    )
