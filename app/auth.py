from fastapi import Depends, Header, HTTPException, status
from app.config import get_settings

def require_api_key(x_api_key: str | None = Header(default=None, alias="X-API-Key")):
    settings = get_settings()
    if not settings.API_KEY:
        # If not configured, deny writes by default.
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="API key not configured"
        )
    if x_api_key != settings.API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key"
        )
    return True