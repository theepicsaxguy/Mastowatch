from fastapi import APIRouter, Depends, HTTPException, status, Request, Response
from fastapi.responses import HTMLResponse, RedirectResponse
import logging
from typing import Dict, Any

from app.auth import get_api_key
from app.oauth import (
    User, 
    require_admin_hybrid, 
    require_authenticated_hybrid,
    get_oauth_config,
    get_current_user,
    create_session_cookie,
    clear_session_cookie
)
from app.jwt_auth import get_jwt_config

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get("/admin/login", tags=["auth"])
def admin_login(request: Request):
    """Initiate admin OAuth login"""
    oauth_config = get_oauth_config()
    if not oauth_config:
        raise HTTPException(status_code=500, detail="OAuth not configured")
    
    # OAuth login logic here - redirect to Mastodon OAuth
    # Implementation details would depend on your OAuth setup
    return {"auth_url": "oauth_login_url_here"}

@router.get("/admin/callback", tags=["auth"])
def admin_callback(request: Request, response: Response):
    """Handle OAuth callback from Mastodon"""
    # Handle OAuth callback logic
    # This would process the authorization code and create session
    return {"message": "OAuth callback processed"}

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
        "avatar_url": user.avatar_url
    }

@router.post("/dryrun/evaluate", tags=["ops"])
def evaluate_dryrun(request_data: Dict[str, Any], _: User = Depends(require_admin_hybrid)):
    """Evaluate content in dry-run mode without taking action"""
    try:
        from app.services.rule_service import rule_service
        
        # Mock account data for testing
        mock_account = request_data.get("account", {})
        
        # Evaluate using rule service
        violations = rule_service.evaluate_account(mock_account)
        
        return {
            "violations": [
                {
                    "rule_name": v.rule_name,
                    "score": v.score,
                    "evidence": v.evidence,
                    "action_type": v.action_type
                }
                for v in violations
            ],
            "total_score": sum(v.score for v in violations),
            "dry_run": True
        }
        
    except Exception as e:
        logger.error("Failed to evaluate dry run", extra={"error": str(e)})
        raise HTTPException(status_code=500, detail="Failed to evaluate content")

@router.post("/webhooks/mastodon_events", tags=["webhooks"])
def handle_mastodon_webhook(request: Request, payload: Dict[str, Any]):
    """Handle incoming webhooks from Mastodon"""
    try:
        from app.tasks.jobs import process_new_report, process_new_status
        
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
        raise HTTPException(status_code=500, detail="Failed to process webhook")
