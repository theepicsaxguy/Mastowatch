"""JWT-based authentication for API access"""

import logging
from datetime import datetime, timedelta
from typing import Any, Dict, Optional

import jwt
from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
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


class JWTConfig:
    def __init__(self, settings):
        self.settings = settings
        self.algorithm = "HS256"
        self.access_token_expire_hours = 24 * 7  # 7 days
        
    def create_access_token(self, user_data: Dict[str, Any]) -> str:
        """Create a JWT access token"""
        to_encode = user_data.copy()
        expire = datetime.utcnow() + timedelta(hours=self.access_token_expire_hours)
        to_encode.update({"exp": expire, "iat": datetime.utcnow()})
        
        encoded_jwt = jwt.encode(
            to_encode, 
            self.settings.SESSION_SECRET_KEY, 
            algorithm=self.algorithm
        )
        return encoded_jwt
    
    def verify_token(self, token: str) -> Dict[str, Any]:
        """Verify and decode JWT token"""
        try:
            payload = jwt.decode(
                token, 
                self.settings.SESSION_SECRET_KEY, 
                algorithms=[self.algorithm]
            )
            return payload
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired"
            )
        except jwt.JWTError as e:
            logger.debug(f"Invalid JWT token: {e}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )


# Global JWT config instance
_jwt_config: Optional[JWTConfig] = None


def get_jwt_config() -> JWTConfig:
    """Get the global JWT configuration"""
    global _jwt_config
    if _jwt_config is None:
        _jwt_config = JWTConfig(get_settings())
    return _jwt_config


# Security scheme for JWT tokens (optional to support hybrid auth)
security = HTTPBearer(auto_error=False)


def get_current_user_from_token(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> Optional[User]:
    """Get current user from JWT token"""
    jwt_config = get_jwt_config()
    
    try:
        user_data = jwt_config.verify_token(credentials.credentials)
        # Remove JWT specific fields
        user_data.pop("exp", None)
        user_data.pop("iat", None)
        return User(**user_data)
    except HTTPException:
        return None


def require_admin_token(current_user: Optional[User] = Depends(get_current_user_from_token)) -> User:
    """Dependency that requires an authenticated admin user via JWT"""
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    
    return current_user


def require_authenticated_token(current_user: Optional[User] = Depends(get_current_user_from_token)) -> User:
    """Dependency that requires any authenticated user via JWT"""
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return current_user


# Hybrid authentication: supports both cookies and JWT tokens
def get_current_user_hybrid(
    request: Request,
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)
) -> Optional[User]:
    """Get current user from either JWT token or session cookie"""
    # Try JWT token first
    if credentials:
        try:
            jwt_config = get_jwt_config()
            user_data = jwt_config.verify_token(credentials.credentials)
            user_data.pop("exp", None)
            user_data.pop("iat", None)
            return User(**user_data)
        except HTTPException:
            pass
    
    # Fallback to session cookie
    from app.oauth import get_current_user
    return get_current_user(request)


def require_admin_hybrid(current_user: Optional[User] = Depends(get_current_user_hybrid)) -> User:
    """Dependency that requires an authenticated admin user via JWT or cookie"""
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


def require_authenticated_hybrid(current_user: Optional[User] = Depends(get_current_user_hybrid)) -> User:
    """Dependency that requires any authenticated user via JWT or cookie"""
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required"
        )
    
    return current_user
