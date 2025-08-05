"""Configuration management API routes."""

from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status

from app.auth import require_api_key
from app.config import get_settings
from app.oauth import User, require_admin_hybrid
from app.services.config_service import ConfigService, get_config_service

router = APIRouter()

api_key_dep = Depends(require_api_key)
admin_dep = Depends(require_admin_hybrid)
service_dep = Depends(get_config_service)
MAX_THRESHOLD = 10


@router.get("/config", response_model=dict[str, Any])
async def get_app_config(
    api_key_valid: bool = api_key_dep,
    service: ConfigService = service_dep,
):
    """Return non-sensitive configuration values."""
    settings = get_settings()
    allowed = {
        "VERSION",
        "DRY_RUN",
        "PANIC_STOP",
        "REPORT_CATEGORY_DEFAULT",
        "FORWARD_REMOTE_REPORTS",
        "MAX_PAGES_PER_POLL",
        "MAX_STATUSES_TO_FETCH",
    }
    config: dict[str, Any] = {k: getattr(settings, k) for k in allowed}
    panic_stop = service.get_config("panic_stop")
    if panic_stop:
        config["PANIC_STOP"] = panic_stop.get("enabled", config["PANIC_STOP"])
    dry_run = service.get_config("dry_run")
    if dry_run:
        config["DRY_RUN"] = dry_run.get("enabled", config["DRY_RUN"])
    report_threshold = service.get_config("report_threshold")
    if report_threshold:
        config["REPORT_THRESHOLD"] = report_threshold.get("threshold")
    return config


@router.post("/config/panic_stop", status_code=status.HTTP_200_OK)
def set_panic_stop(
    enable: bool,
    user: User = admin_dep,
    service: ConfigService = service_dep,
):
    """Toggle panic stop flag."""
    service.set_flag("panic_stop", enable, updated_by=user.username)
    return {"panic_stop": enable}


@router.post("/config/dry_run", tags=["ops"])
def set_dry_run_mode(
    enable: bool,
    user: User = admin_dep,
    service: ConfigService = service_dep,
):
    """Toggle dry run mode."""
    service.set_flag("dry_run", enable, updated_by=user.username)
    return {"dry_run": enable}


@router.post("/config/report_threshold", tags=["ops"])
def set_report_threshold(
    threshold: float,
    user: User = admin_dep,
    service: ConfigService = service_dep,
):
    """Update report threshold."""
    if threshold < 0 or threshold > MAX_THRESHOLD:
        raise HTTPException(status_code=400, detail="Threshold must be between 0 and 10")
    service.set_threshold("report_threshold", threshold, updated_by=user.username)
    return {"report_threshold": threshold}
