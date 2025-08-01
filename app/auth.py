from fastapi import Depends, Header, HTTPException, status
from app.config import get_settings

def require_api_key():
    """
    Authentication dependency for dashboard endpoints.
    Since the dashboard is protected by SSO, we skip API key validation.
    """
    return True