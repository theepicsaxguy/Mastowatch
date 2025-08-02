from fastapi import APIRouter, Depends, HTTPException, status
from typing import Dict, Any

from app.auth import get_api_key
from app.config import get_settings
from app.db import SessionLocal
from sqlalchemy import text

router = APIRouter()

@router.get("/config", response_model=Dict[str, Any])
async def get_app_config(api_key: str = Depends(get_api_key)):
    """Get current application configuration."""
    settings = get_settings()
    return settings.dict()

@router.post("/config/panic_stop", status_code=status.HTTP_200_OK)
async def set_panic_stop(enable: bool, api_key: str = Depends(get_api_key)):
    """Enable or disable panic stop."""
    with SessionLocal() as db:
        db.execute(text("INSERT INTO config (key, value) VALUES (:key, :value) ON CONFLICT (key) DO UPDATE SET value = :value"),
                   {"key": "panic_stop", "value": {"enabled": enable}})
        db.commit()
    return {"message": f"Panic stop set to {enable}"}
