"""Authentication and authorization API endpoints."""

import hashlib
import hmac
import logging
import secrets
from typing import Any
from urllib.parse import urlencode

import httpx
from fastapi import APIRouter, Depends, HTTPException, Request, Response
from fastapi.responses import HTMLResponse, RedirectResponse

from app.config import get_settings
from app.oauth import (
    User,
    clear_session_cookie,
    create_session_cookie,
    get_oauth_config,
    require_admin_hybrid,
)
from app.services.rule_service import rule_service
from app.tasks.jobs import process_new_report, process_new_status

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/admin/login", tags=["auth"])
def admin_login(request: Request):
    """Initiate admin OAuth login."""
    oauth_config = get_oauth_config()
    settings = get_settings()

    if not oauth_config.configured:
        raise HTTPException(status_code=500, detail="OAuth not configured")

    # Generate state parameter for CSRF protection
    state = secrets.token_urlsafe(32)
    request.session["oauth_state"] = state

    # Build OAuth authorization URL
    params = {
        "client_id": settings.OAUTH_CLIENT_ID,
        "redirect_uri": settings.OAUTH_REDIRECT_URI or f"{request.base_url}admin/callback",
        "response_type": "code",
        "scope": "read:accounts",
        "state": state,
    }

    auth_url = f"{settings.INSTANCE_BASE}/oauth/authorize?" + urlencode(params)

    return {"auth_url": auth_url}


@router.get("/admin/callback", tags=["auth"])
async def admin_callback(request: Request, response: Response, code: str = None, state: str = None, error: str = None):
    """Handle OAuth callback from Mastodon."""
    settings = get_settings()
    oauth_config = get_oauth_config()

    if not oauth_config.configured:
        raise HTTPException(status_code=500, detail="OAuth not configured")

    # Handle OAuth errors
    if error:
        logger.warning(f"OAuth error: {error}")
        raise HTTPException(status_code=400, detail=f"OAuth error: {error}")

    if not code:
        raise HTTPException(status_code=400, detail="Missing authorization code")

    # Verify state parameter for CSRF protection
    stored_state = request.session.get("oauth_state")
    if not stored_state or stored_state != state:
        raise HTTPException(status_code=400, detail="Invalid state parameter")

    try:
        # Exchange authorization code for access token
        token_data = {
            "client_id": settings.OAUTH_CLIENT_ID,
            "client_secret": settings.OAUTH_CLIENT_SECRET,
            "redirect_uri": settings.OAUTH_REDIRECT_URI or f"{request.base_url}admin/callback",
            "grant_type": "authorization_code",
            "code": code,
        }

        async with httpx.AsyncClient() as client:
            token_response = await client.post(
                f"{settings.INSTANCE_BASE}/oauth/token",
                data=token_data,
                headers={"Accept": "application/json"},
            )

        if token_response.status_code != 200:
            logger.error(f"Token exchange failed: {token_response.status_code} - {token_response.text}")
            raise HTTPException(status_code=500, detail="Failed to exchange authorization code")

        token_info = token_response.json()
        access_token = token_info.get("access_token")

        if not access_token:
            raise HTTPException(status_code=500, detail="No access token received")

        # Fetch user information
        user = await oauth_config.fetch_user_info(access_token)

        if not user:
            raise HTTPException(status_code=500, detail="Failed to fetch user information")

        if not user.is_admin:
            raise HTTPException(status_code=403, detail="Admin access required")

        # Create session cookie
        create_session_cookie(response, user, settings)

        # Clear OAuth state from session
        request.session.pop("oauth_state", None)

        # Redirect to admin dashboard
        return RedirectResponse(url="/dashboard", status_code=302)

    except Exception as e:
        logger.error("OAuth callback failed", extra={"error": str(e)})
        raise HTTPException(status_code=500, detail="Authentication failed") from e


@router.get("/admin/popup-callback", response_class=HTMLResponse, tags=["auth"])
def popup_callback(request: Request):
    """Handle popup OAuth callback"""
    return """
    <html>
        <head>
            <title>Authorization Complete</title>
        </head>
        <body>
            <script>
                // Close popup and notify parent window
                window.opener.postMessage({type: 'oauth_success'}, '*');
                window.close();
            </script>
            <p>Authorization complete. You can close this window.</p>
        </body>
    </html>
    """


@router.post("/admin/logout", tags=["auth"])
def admin_logout(response: Response, user: User = Depends(require_admin_hybrid)):
    """Logout current admin user"""
    clear_session_cookie(response)
    return {"message": "Logged out successfully"}


@router.get("/api/v1/me", tags=["auth"])
def get_current_user_info(user: User = Depends(require_admin_hybrid)):
    """Get current authenticated user information"""
    return {
        "username": user.username,
        "display_name": user.display_name,
        "is_admin": user.is_admin,
        "avatar_url": user.avatar_url,
    }


@router.post("/dryrun/evaluate", tags=["ops"])
def evaluate_dryrun(request_data: dict[str, Any], _: User = Depends(require_admin_hybrid)):
    """Evaluate content in dry-run mode without taking action."""
    try:
        # Mock account data for testing
        mock_account = request_data.get("account", {})

        # Evaluate using rule service
        violations = rule_service.evaluate_account(mock_account)

        return {
            "violations": [
                {"rule_name": v.rule_name, "score": v.score, "evidence": v.evidence, "action_type": v.action_type}
                for v in violations
            ],
            "total_score": sum(v.score for v in violations),
            "dry_run": True,
        }

    except Exception as e:
        logger.error("Failed to evaluate dry run", extra={"error": str(e)})
        raise HTTPException(status_code=500, detail="Failed to evaluate content") from e


@router.post("/webhooks/mastodon_events", tags=["webhooks"])
async def handle_mastodon_webhook(request: Request, payload: dict[str, Any]):
    """Handle incoming webhooks from Mastodon."""
    settings = get_settings()

    # Validate webhook signature if secret is configured
    if settings.WEBHOOK_SECRET:
        signature_header = request.headers.get(settings.WEBHOOK_SIG_HEADER)
        if not signature_header:
            raise HTTPException(status_code=401, detail="Missing webhook signature")

        # Extract signature from header (format: "sha256=<hexdigest>")
        try:
            algorithm, signature = signature_header.split("=", 1)
            if algorithm.lower() != "sha256":
                raise HTTPException(status_code=401, detail="Unsupported signature algorithm")
        except ValueError as e:
            raise HTTPException(status_code=401, detail="Invalid signature format") from e

        # Validate signature
        body = await request.body()
        expected_signature = hmac.new(settings.WEBHOOK_SECRET.encode(), body, hashlib.sha256).hexdigest()

        if not hmac.compare_digest(signature, expected_signature):
            logger.warning("Invalid webhook signature received")
            raise HTTPException(status_code=401, detail="Invalid webhook signature")

    try:
        event_type = request.headers.get("X-Event-Type", "unknown")

        if event_type == "report.created":
            # Process new report
            task = process_new_report.delay(payload)
            return {"message": "Report processing queued", "task_id": task.id}
        elif event_type == "status.created":
            # Process new status for proactive scanning
            task = process_new_status.delay(payload)
            return {"message": "Status processing queued", "task_id": task.id}
        else:
            return {"message": f"Ignored event type: {event_type}"}

    except Exception as e:
        logger.error("Failed to process webhook", extra={"error": str(e), "event_type": event_type})
        raise HTTPException(status_code=500, detail="Failed to process webhook") from e
