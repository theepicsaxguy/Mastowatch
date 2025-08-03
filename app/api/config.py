from fastapi import APIRouter, Depends, HTTPException, status
from typing import Dict, Any
from sqlalchemy import text

from app.auth import require_api_key
from app.config import get_settings
from app.db import SessionLocal
from app.oauth import User, require_admin_hybrid

router = APIRouter()

@router.get("/config", response_model=Dict[str, Any])
async def get_app_config(api_key_valid: bool = Depends(require_api_key)):
    """Get current application configuration."""
    settings = get_settings()
    return settings.dict()

@router.post("/config/panic_stop", status_code=status.HTTP_200_OK)
def set_panic_stop(enable: bool, _: User = Depends(require_admin_hybrid)):
    """Enable or disable panic stop."""
    with SessionLocal() as db:
        db.execute(text("INSERT INTO config (key, value) VALUES (:key, :value) ON CONFLICT (key) DO UPDATE SET value = :value"),
                   {"key": "panic_stop", "value": {"enabled": enable}})
        db.commit()
    return {"message": f"Panic stop set to {enable}"}


@router.post("/config/dry_run", tags=["ops"])
def set_dry_run_mode(enable: bool, _: User = Depends(require_admin_hybrid)):
    """Enable or disable dry run mode"""
    with SessionLocal() as db:
        db.execute(text("INSERT INTO config (key, value) VALUES (:key, :value) ON CONFLICT (key) DO UPDATE SET value = :value"),
                   {"key": "dry_run", "value": {"enabled": enable}})
        db.commit()
    return {"message": f"Dry run mode set to {enable}"}


@router.post("/config/report_threshold", tags=["ops"])
def set_report_threshold(threshold: float, _: User = Depends(require_admin_hybrid)):
    """Set the report threshold for automatic reporting"""
    if threshold < 0 or threshold > 10:
        raise HTTPException(status_code=400, detail="Threshold must be between 0 and 10")
    
    with SessionLocal() as db:
        db.execute(text("INSERT INTO config (key, value) VALUES (:key, :value) ON CONFLICT (key) DO UPDATE SET value = :value"),
                   {"key": "report_threshold", "value": {"threshold": threshold}})
        db.commit()
    return {"message": f"Report threshold set to {threshold}"}
