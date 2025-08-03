import redis
import hashlib
import hmac
import json
import logging
import re
import time
import secrets
from datetime import datetime, timedelta
from typing import Any, Dict, List
from urllib.parse import urlencode

from fastapi import Depends, FastAPI, HTTPException, Request, Response, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, PlainTextResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from prometheus_client import CONTENT_TYPE_LATEST, generate_latest
from pydantic import BaseModel
from sqlalchemy import desc, func, text
from sqlalchemy.orm import Session

from app.auth import require_api_key
from app.config import get_settings
from app.db import SessionLocal
from app.logging_conf import setup_logging
from app.models import Account, Analysis, Config, Report, Rule, ScanSession, ContentScan, DomainAlert
from app.oauth import (
    get_oauth_config, 
    get_current_user, 
    create_session_cookie,
    clear_session_cookie,
    User
)
from sqlalchemy import inspect
from app.jwt_auth import (
    get_jwt_config,
    require_admin_hybrid,
    require_authenticated_hybrid
)
from app.services.rule_service import rule_service
from app.enhanced_scanning import EnhancedScanningSystem
from app.startup_validation import run_all_startup_validations
from app.tasks.jobs import analyze_and_maybe_report, scan_federated_content, check_domain_violations, process_new_report, process_new_status

# Import API routers
from app.api.analytics import router as analytics_router
from app.api.rules import router as rules_router
from app.api.config import router as config_router
from app.api.scanning import router as scanning_router
from app.api.auth import router as auth_router

setup_logging()
logger = logging.getLogger(__name__)

# Run startup validations before anything else
run_all_startup_validations()

app = FastAPI(title="MastoWatch", version="1.0.0")
settings = get_settings()

# Register API routers
app.include_router(analytics_router)
app.include_router(rules_router)
app.include_router(config_router)
app.include_router(scanning_router)
app.include_router(auth_router)

if settings.CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# Mount dashboard if present (built by the frontend build step)
try:
    app.mount("/dashboard", StaticFiles(directory="static/dashboard", html=True), name="dashboard")
except Exception:
    logging.info("Dashboard static assets not found; skipping mount.")


# Database dependency
def get_db_session():
    """Dependency to get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/healthz", tags=["ops"])
def healthz():
    """Health check endpoint with comprehensive system status"""
    start_time = time.time()
    health_data = {
        "ok": True,
        "db_ok": False,
        "redis_ok": False,
        "dry_run": settings.DRY_RUN,
        "panic_stop": settings.PANIC_STOP,
        "batch_size": settings.BATCH_SIZE,
        "version": settings.VERSION,
        "timestamp": datetime.utcnow().isoformat(),
    }

    try:
        import redis

        from app.db import SessionLocal

        # Test database connection
        try:
            with SessionLocal() as db:
                db.execute(text("SELECT 1"))
                health_data["db_ok"] = True
                logger.debug("Database health check passed")
        except Exception as e:
            logger.error("Database health check failed", extra={"error": str(e), "error_type": type(e).__name__})
            health_data["db_ok"] = False

        # Test Redis connection
        try:
            r = redis.from_url(settings.REDIS_URL)
            health_data["redis_ok"] = r.ping()
            logger.debug("Redis health check passed")
        except Exception as e:
            logger.error("Redis health check failed", extra={"error": str(e), "error_type": type(e).__name__})
            health_data["redis_ok"] = False

        health_data["ok"] = health_data["db_ok"] and health_data["redis_ok"]
        health_data["response_time_ms"] = round((time.time() - start_time) * 1000, 1)

        if not health_data["ok"]:
            logger.warning(
                "Health check failed",
                extra={
                    "db_ok": health_data["db_ok"],
                    "redis_ok": health_data["redis_ok"],
                    "response_time_ms": health_data["response_time_ms"],
                },
            )
            # Return 503 for failed health checks
            raise HTTPException(status_code=503, detail=health_data)

        return health_data

    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            "Health check endpoint failed with unexpected error",
            extra={
                "error": str(e),
                "error_type": type(e).__name__,
                "response_time_ms": round((time.time() - start_time) * 1000, 1),
            },
        )
        raise HTTPException(
            status_code=500, detail={"error": "health_check_failed", "message": "Health check endpoint encountered an error"}
        )


@app.get("/metrics", response_class=PlainTextResponse, tags=["ops"])
def metrics():
    return PlainTextResponse(generate_latest(), media_type=CONTENT_TYPE_LATEST)


@app.post("/dryrun/evaluate", tags=["ops"])
async def dryrun_evaluate(payload: dict):
    acct = payload.get("account") or {}
    statuses = payload.get("statuses") or []
    score, hits = rule_service.eval_account(acct, statuses)
    return {"score": score, "hits": hits}


@app.post("/webhooks/mastodon_events", tags=["webhooks"])
async def webhook_mastodon_events(request: Request):
    """Handle incoming Mastodon event webhooks with signature validation and event routing"""
    start_time = time.time()
    request_id = f"webhook_{int(start_time * 1000)}"

    try:
        body = await request.body()
        content_length = len(body)
        event_type = request.headers.get("X-Mastodon-Event", "unknown")

        logger.info(
            "Processing Mastodon webhook event",
            extra={
                "request_id": request_id,
                "event_type": event_type,
                "content_length": content_length,
                "source_ip": request.client.host if request.client else "unknown",
                "user_agent": request.headers.get("user-agent", "unknown"),
            },
        )

        # Validate webhook is configured
        if not settings.WEBHOOK_SECRET:
            logger.warning("Webhook received but WEBHOOK_SECRET not configured", extra={"request_id": request_id})
            raise HTTPException(
                status_code=503,
                detail={
                    "error": "webhook_not_configured",
                    "message": "Webhook secret not configured",
                    "request_id": request_id,
                },
            )

        # Validate signature
        sig_hdr = settings.WEBHOOK_SIG_HEADER
        provided = request.headers.get(sig_hdr, "")
        if not provided.startswith("sha256="):
            logger.warning(
                "Invalid signature header format",
                extra={
                    "request_id": request_id,
                    "signature_header": sig_hdr,
                    "provided_prefix": provided[:20] + "..." if len(provided) > 20 else provided,
                },
            )
            raise HTTPException(
                status_code=401,
                detail={
                    "error": "invalid_signature_format",
                    "message": "Invalid signature header format",
                    "request_id": request_id,
                },
            )

        provided_hex = provided.split("=", 1)[1].strip()
        digest = hmac.new(settings.WEBHOOK_SECRET.encode("utf-8"), body, hashlib.sha256).hexdigest()

        if not hmac.compare_digest(digest, provided_hex):
            logger.warning(
                "Webhook signature mismatch",
                extra={
                    "request_id": request_id,
                    "expected_signature_prefix": digest[:8] + "...",
                    "provided_signature_prefix": provided_hex[:8] + "...",
                },
            )
            raise HTTPException(
                status_code=401,
                detail={
                    "error": "signature_mismatch",
                    "message": "Webhook signature verification failed",
                    "request_id": request_id,
                },
            )

        # Parse payload
        try:
            payload = await request.json()
        except Exception as e:
            logger.error(
                "Failed to parse webhook JSON payload",
                extra={
                    "request_id": request_id,
                    "error": str(e),
                    "content_type": request.headers.get("content-type", "unknown"),
                },
            )
            raise HTTPException(
                status_code=400,
                detail={"error": "invalid_json_payload", "message": "Failed to parse JSON payload", "request_id": request_id},
            )

        # Route events to appropriate Celery tasks
        task_id = None
        # Deduplication using Redis SETNX
        r = redis.from_url(settings.REDIS_URL)
        event_dedupe_key = f"webhook_dedupe:{event_type}:{payload.get('id', hashlib.sha256(body).hexdigest())}"
        if r.setnx(event_dedupe_key, "1"):
            r.expire(event_dedupe_key, 60) # Deduplicate for 60 seconds
        else:
            logger.info(f"Duplicate webhook event received: {event_type}", extra={"request_id": request_id})
            return {"ok": True, "message": f"Duplicate event: {event_type}", "request_id": request_id}

        if event_type == "report.created":
            report_id = payload.get("report", {}).get("id")
            logger.info(f"Enqueuing report.created event for report ID: {report_id}", extra={"request_id": request_id})
            task = process_new_report.delay(payload)
            task_id = task.id
        elif event_type == "status.created":
            status_id = payload.get("status", {}).get("id")
            logger.info(f"Enqueuing status.created event for status ID: {status_id}", extra={"request_id": request_id})
            task = process_new_status.delay(payload)
            task_id = task.id
        else:
            logger.info(f"Received unhandled Mastodon event type: {event_type}", extra={"request_id": request_id})
            return {"ok": True, "message": f"Unhandled event type: {event_type}", "request_id": request_id}

        processing_time = time.time() - start_time
        logger.info(
            "Webhook processed successfully",
            extra={
                "request_id": request_id,
                "event_type": event_type,
                "content_length": content_length,
                "task_id": task_id,
                "processing_time_ms": round(processing_time * 1000, 1),
            },
        )

        return {
            "ok": True,
            "enqueued": True,
            "task_id": task_id,
            "event_type": event_type,
            "processing_time_ms": round(processing_time * 1000, 1),
            "request_id": request_id,
        }

    except HTTPException:
        raise
    except Exception as e:
        processing_time = time.time() - start_time
        logger.error(
            "Webhook processing failed with unexpected error",
            extra={
                "request_id": request_id,
                "error": str(e),
                "error_type": type(e).__name__,
                "processing_time_ms": round(processing_time * 1000, 1),
            },
        )
        raise HTTPException(
            status_code=500,
            detail={"error": "internal_server_error", "message": "Webhook processing failed", "request_id": request_id},
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)


class DryRunToggle(BaseModel):
    dry_run: bool
    updated_by: str | None = None


@app.post("/config/dry_run", tags=["ops"])
def set_dry_run(body: DryRunToggle, _: User = Depends(require_admin_hybrid)):
    """Toggle dry run mode and persist to database"""
    try:
        if body.dry_run is None:
            raise HTTPException(
                status_code=400, detail={"error": "missing_dry_run_flag", "message": "dry_run flag cannot be null"}
            )

        # Ensure only 'dry_run' key can be updated via this endpoint
        # The Config model's 'key' is a primary key, so merge handles upsert.
        # We explicitly set the key here to 'dry_run' to prevent arbitrary key updates.
        config_key = "dry_run"

        with SessionLocal() as db:
            try:
                db.merge(Config(key=config_key, value={"enabled": body.dry_run}, updated_by=body.updated_by))
                db.commit()
            except Exception as e:
                db.rollback()
                logger.error(
                    "Failed to persist dry run configuration to database",
                    extra={
                        "error": str(e),
                        "error_type": type(e).__name__,
                        "dry_run": body.dry_run,
                        "updated_by": body.updated_by,
                    },
                )
                raise HTTPException(
                    status_code=500,
                    detail={"error": "database_update_failed", "message": "Failed to persist configuration to database"},
                )

        settings.DRY_RUN = bool(body.dry_run)
        logger.info(
            "Dry run mode configuration updated",
            extra={"dry_run": body.dry_run, "updated_by": body.updated_by or "unknown", "persisted": True},
        )
        return {"dry_run": settings.DRY_RUN, "persisted": True}

    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            "Failed to update dry run setting",
            extra={
                "error": str(e),
                "error_type": type(e).__name__,
                "requested_dry_run": getattr(body, "dry_run", None),
                "updated_by": getattr(body, "updated_by", None),
            },
        )
        raise HTTPException(
            status_code=500, detail={"error": "configuration_update_failed", "message": "Failed to update dry run setting"}
        )


class PanicToggle(BaseModel):
    panic_stop: bool
    updated_by: str | None = None


@app.post("/config/panic_stop", tags=["ops"])
def set_panic_stop(body: PanicToggle, _: User = Depends(require_admin_hybrid)):
    """Toggle panic stop mode and persist to database"""
    try:
        if body.panic_stop is None:
            raise HTTPException(
                status_code=400, detail={"error": "missing_panic_stop_flag", "message": "panic_stop flag cannot be null"}
            )

        with SessionLocal() as db:
            try:
                db.merge(Config(key="panic_stop", value={"enabled": body.panic_stop}, updated_by=body.updated_by))
                db.commit()
            except Exception as e:
                db.rollback()
                logger.error(
                    "Failed to persist panic stop configuration to database",
                    extra={
                        "error": str(e),
                        "error_type": type(e).__name__,
                        "panic_stop": body.panic_stop,
                        "updated_by": body.updated_by,
                    },
                )
                raise HTTPException(
                    status_code=500,
                    detail={"error": "database_update_failed", "message": "Failed to persist configuration to database"},
                )

        settings.PANIC_STOP = bool(body.panic_stop)
        logger.warning(
            "Panic stop mode configuration updated",
            extra={"panic_stop": body.panic_stop, "updated_by": body.updated_by or "unknown", "persisted": True},
        )
        return {"panic_stop": settings.PANIC_STOP, "persisted": True}

    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            "Failed to update panic stop setting",
            extra={
                "error": str(e),
                "error_type": type(e).__name__,
                "requested_panic_stop": getattr(body, "panic_stop", None),
                "updated_by": getattr(body, "updated_by", None),
            },
        )
        raise HTTPException(
            status_code=500, detail={"error": "configuration_update_failed", "message": "Failed to update panic stop setting"}
        )


class ReportThresholdToggle(BaseModel):
    threshold: float
    updated_by: str | None = None


@app.post("/config/report_threshold", tags=["ops"])
def set_report_threshold(body: ReportThresholdToggle, _: User = Depends(require_admin_hybrid)):
    """Set report threshold and persist to database"""
    try:
        if body.threshold is None:
            raise HTTPException(
                status_code=400, detail={"error": "missing_threshold", "message": "threshold cannot be null"}
            )
        
        if body.threshold < 0 or body.threshold > 10.0:
            raise HTTPException(
                status_code=400, detail={"error": "invalid_threshold", "message": "threshold must be between 0 and 10.0"}
            )

        with SessionLocal() as db:
            try:
                db.merge(Config(key="report_threshold", value={"threshold": body.threshold}, updated_by=body.updated_by))
                db.commit()
            except Exception as e:
                db.rollback()
                logger.error(
                    "Failed to persist report threshold configuration to database",
                    extra={
                        "error": str(e),
                        "error_type": type(e).__name__,
                        "threshold": body.threshold,
                        "updated_by": body.updated_by,
                    },
                )
                raise HTTPException(
                    status_code=500,
                    detail={"error": "database_update_failed", "message": "Failed to persist configuration to database"},
                )

        # Reload rules to pick up new threshold
        rule_service.load_rules_from_database()
        
        logger.info(
            "Report threshold configuration updated",
            extra={"threshold": body.threshold, "updated_by": body.updated_by or "unknown", "persisted": True},
        )
        return {"threshold": body.threshold, "persisted": True}

    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            "Failed to update report threshold setting",
            extra={
                "error": str(e),
                "error_type": type(e).__name__,
                "requested_threshold": getattr(body, "threshold", None),
                "updated_by": getattr(body, "updated_by", None),
            },
        )
        raise HTTPException(
            status_code=500, detail={"error": "configuration_update_failed", "message": "Failed to update report threshold setting"}
        )


# OAuth Authentication Routes
@app.get("/admin/login", tags=["auth"])
async def admin_login(request: Request, response: Response, popup: bool = False):
    """Initiate OAuth login flow"""
    oauth_config = get_oauth_config()
    
    if not oauth_config.configured:
        raise HTTPException(
            status_code=503,
            detail="OAuth not configured - admin login unavailable"
        )
    
    # Generate state parameter for CSRF protection
    state = secrets.token_urlsafe(32)
    
    # Store state in Redis with short TTL instead of cookies to avoid cross-origin issues
    try:
        import redis
        r = redis.from_url(settings.REDIS_URL, decode_responses=True)
        r.setex(f"oauth_state:{state}", 600, "valid")  # 10 minutes TTL
    except Exception as e:
        logger.warning(f"Failed to store OAuth state in Redis: {e}")
        # Fallback: still try cookie approach
        response.set_cookie(
            key="oauth_state",
            value=state,
            max_age=600,  # 10 minutes
            httponly=False,  # Allow JavaScript access for debugging
            secure=False,  # HTTP only
            samesite="lax"  # More permissive for OAuth redirects
        )
    
    # Use configured redirect URIs or fall back to dynamic generation
    if popup:
        redirect_uri = settings.OAUTH_POPUP_REDIRECT_URI or settings.OAUTH_REDIRECT_URI or f"{request.base_url}admin/popup-callback"
    else:
        redirect_uri = settings.OAUTH_REDIRECT_URI or f"{request.base_url}admin/callback"
    
    # Build authorization URL
    params = {
        "client_id": settings.OAUTH_CLIENT_ID,
        "redirect_uri": redirect_uri,
        "response_type": "code",
        "scope": "read:accounts",
        "state": state
    }
    
    auth_url = f"{str(settings.INSTANCE_BASE).rstrip('/')}/oauth/authorize?" + urlencode(params)
    
    logger.info(f"Redirecting to OAuth login: {auth_url}")
    return RedirectResponse(url=auth_url)


@app.get("/admin/callback", tags=["auth"])
async def admin_callback(
    request: Request, 
    response: Response, 
    code: str = None, 
    error: str = None, 
    state: str = None,
    format: str = "redirect"  # "redirect" or "token"
):
    """Handle OAuth callback"""
    oauth_config = get_oauth_config()
    
    if not oauth_config.configured:
        raise HTTPException(status_code=503, detail="OAuth not configured")
    
    if error:
        logger.warning(f"OAuth error: {error}")
        raise HTTPException(status_code=400, detail=f"OAuth error: {error}")
    
    if not code:
        raise HTTPException(status_code=400, detail="Missing authorization code")
    
    # Verify CSRF state parameter using Redis instead of cookies
    stored_state_cookie = request.cookies.get("oauth_state")
    stored_state_redis = None
    
    try:
        import redis
        r = redis.from_url(settings.REDIS_URL, decode_responses=True)
        redis_key = f"oauth_state:{state}"
        stored_state_redis = r.get(redis_key)
        if stored_state_redis:
            r.delete(redis_key)  # Use once
    except Exception as e:
        logger.warning(f"Failed to retrieve OAuth state from Redis: {e}")
    
    logger.info(f"OAuth callback - cookie_state: {stored_state_cookie}, redis_state: {stored_state_redis}, received_state: {state}")
    
    # Strictly compare state parameter
    if not state or (state != stored_state_cookie and state != stored_state_redis):
        logger.warning(f"OAuth CSRF state mismatch - cookie: {stored_state_cookie}, redis: {stored_state_redis}, received: {state}")
        raise HTTPException(status_code=400, detail="Invalid state parameter")
    
    # Clear the state cookie
    response.set_cookie(
        key="oauth_state",
        value="",
        max_age=0,
        httponly=False,
        secure=False,
        samesite="lax"
    )
    
    try:
        # Exchange code for access token using generated client
        from app.clients.mastodon.client import Client
        
        # Determine the correct redirect URI based on the context
        # If format=token, this is from a popup, so use popup-callback URI
        # Use the same base URL logic as in the login endpoint to ensure consistency
        if format == "token":
            # Extract the base URL from the configured redirect URI if available
            if settings.OAUTH_REDIRECT_URI:
                # Replace /admin/callback with /admin/popup-callback
                redirect_uri = settings.OAUTH_REDIRECT_URI.replace("/admin/callback", "/admin/popup-callback")
            else:
                redirect_uri = f"{request.base_url}admin/popup-callback"
        else:
            redirect_uri = settings.OAUTH_REDIRECT_URI or f"{request.base_url}admin/callback"
        
        # Use generated client for OAuth token exchange
        oauth_client = Client(base_url=str(settings.INSTANCE_BASE))
        
        # Prepare token exchange data
        token_data = {
            "client_id": settings.OAUTH_CLIENT_ID,
            "client_secret": settings.OAUTH_CLIENT_SECRET,
            "code": code,
            "grant_type": "authorization_code",
            "redirect_uri": redirect_uri,
        }
        
        # Use the generated client's HTTP session for consistency
        async with oauth_client.get_async_httpx_client() as http_client:
            token_response = await http_client.post("/oauth/token", data=token_data)
        
        if token_response.status_code != 200:
            logger.error(f"Token exchange failed: {token_response.status_code}")
            raise HTTPException(status_code=400, detail="Failed to exchange authorization code")
        
        token_json = token_response.json()
        access_token = token_json.get("access_token")
        
        if not access_token:
            raise HTTPException(status_code=400, detail="No access token received")
        
        # Fetch user information
        user = await oauth_config.fetch_user_info(access_token)
        
        if not user:
            raise HTTPException(status_code=400, detail="Failed to fetch user information")
        
        if not user.is_admin:
            logger.warning(f"Non-admin user attempted login: {user.acct}")
            raise HTTPException(status_code=403, detail="Admin access required")
        
        logger.info(f"Admin user logged in: {user.acct}")
        
        # Handle different response formats
        if format == "token":
            # Return JWT token for API access
            jwt_config = get_jwt_config()
            token = jwt_config.create_access_token(user.model_dump())
            
            return {
                "access_token": token,
                "token_type": "bearer",
                "user": user.model_dump()
            }
        else:
            # Traditional redirect with session cookie
            create_session_cookie(response, user, settings)
            
            # Redirect to dashboard
            # For development, redirect to the frontend dev server
            frontend_url = "http://localhost:5173"
            return RedirectResponse(url=frontend_url, status_code=302)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"OAuth callback error: {e}")
        raise HTTPException(status_code=500, detail="Authentication failed")


@app.get("/admin/popup-callback", response_class=HTMLResponse, tags=["auth"])
async def admin_popup_callback(request: Request, code: str = None, error: str = None, state: str = None):
    """Handle OAuth callback for popup windows - returns HTML that communicates with parent"""
    oauth_callback_html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>OAuth Callback</title>
        <style>
            body {{
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                padding: 20px;
                text-align: center;
                background: #f5f5f5;
            }}
            .container {{
                max-width: 400px;
                margin: 50px auto;
                background: white;
                padding: 30px;
                border-radius: 8px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }}
            .loading {{
                color: #666;
            }}
            .success {{
                color: #28a745;
            }}
            .error {{
                color: #dc3545;
            }}
            .spinner {{
                border: 2px solid #f3f3f3;
                border-top: 2px solid #3498db;
                border-radius: 50%;
                width: 20px;
                height: 20px;
                animation: spin 1s linear infinite;
                margin: 10px auto;
            }}
            @keyframes spin {{
                0% {{ transform: rotate(0deg); }}
                100% {{ transform: rotate(360deg); }}
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div id="status" class="loading">
                <div class="spinner"></div>
                <p>Completing authentication...</p>
            </div>
        </div>

        <script>
            (async function() {{
                const urlParams = new URLSearchParams(window.location.search);
                const code = urlParams.get('code');
                const error = urlParams.get('error');
                const state = urlParams.get('state');

                try {{
                    if (error) {{
                        throw new Error(error);
                    }}

                    if (!code) {{
                        throw new Error('No authorization code received');
                    }}

                    // Exchange code for token
                    const response = await fetch(`/admin/callback?format=token&code=${{code}}&state=${{state}}}`);
                    
                    if (!response.ok) {{
                        const text = await response.text();
                        throw new Error(`${{response.status}}: ${{text}}`);
                    }}

                    const authData = await response.json();

                    // Show success
                    document.getElementById('status').innerHTML = `
                        <div class="success">
                            <p>✅ Authentication successful!</p>
                            <p>Welcome, ${{authData.user.display_name}}!</p>
                            <p>This window will close automatically...</p>
                        </div>
                    `;

                    // Send auth data to parent window
                    if (window.opener) {{
                        window.opener.postMessage({{
                            type: 'oauth-success',
                            auth: authData
                        }}, '{settings.UI_ORIGIN}');
                    }}

                    // Close window after a short delay
                    setTimeout(() => {{
                        window.close();
                    }}, 2000);

                }} catch (error) {{
                    console.error('OAuth callback error:', error);
                    
                    // Show error
                    document.getElementById('status').innerHTML = `
                        <div class="error">
                            <p>❌ Authentication failed</p>
                            <p>${{error.message}}</p>
                            <p>This window will close automatically...</p>
                        </div>
                    `;

                    // Send error to parent window
                    if (window.opener) {{
                        window.opener.postMessage({{
                            type: 'oauth-error',
                            error: error.message
                        }}, '{settings.UI_ORIGIN}');
                    }}

                    // Close window after a short delay
                    setTimeout(() => {{
                        window.close();
                    }}, 3000);
                }}
            }})();
        </script>
    </body>
    </html>
    """
    return oauth_callback_html


@app.post("/admin/logout", tags=["auth"])
async def admin_logout(response: Response):
    """Logout and clear session"""
    clear_session_cookie(response, settings)
    return {"logged_out": True}


@app.get("/api/v1/me", tags=["auth"])
async def get_current_user_info(current_user: User = Depends(require_authenticated_hybrid)):
    """Get current user information"""
    return {
        "id": current_user.id,
        "username": current_user.username,
        "acct": current_user.acct,
        "display_name": current_user.display_name,
        "is_admin": current_user.is_admin,
        "avatar": current_user.avatar
    }


@app.post("/dryrun/evaluate", tags=["ops"])
async def dryrun_evaluate(payload: dict):
    acct = payload.get("account") or {}
    statuses = payload.get("statuses") or []
    score, hits = rule_service.eval_account(acct, statuses)
    return {"score": score, "hits": hits}


@app.post("/webhooks/mastodon_events", tags=["webhooks"])
async def webhook_mastodon_events(request: Request):
    """Handle incoming Mastodon event webhooks with signature validation and event routing"""
    start_time = time.time()
    request_id = f"webhook_{int(start_time * 1000)}"

    try:
        body = await request.body()
        content_length = len(body)
        event_type = request.headers.get("X-Mastodon-Event", "unknown")

        logger.info(
            "Processing Mastodon webhook event",
            extra={
                "request_id": request_id,
                "event_type": event_type,
                "content_length": content_length,
                "source_ip": request.client.host if request.client else "unknown",
                "user_agent": request.headers.get("user-agent", "unknown"),
            },
        )

        # Validate webhook is configured
        if not settings.WEBHOOK_SECRET:
            logger.warning("Webhook received but WEBHOOK_SECRET not configured", extra={"request_id": request_id})
            raise HTTPException(
                status_code=503,
                detail={
                    "error": "webhook_not_configured",
                    "message": "Webhook secret not configured",
                    "request_id": request_id,
                },
            )

        # Validate signature
        sig_hdr = settings.WEBHOOK_SIG_HEADER
        provided = request.headers.get(sig_hdr, "")
        if not provided.startswith("sha256="):
            logger.warning(
                "Invalid signature header format",
                extra={
                    "request_id": request_id,
                    "signature_header": sig_hdr,
                    "provided_prefix": provided[:20] + "..." if len(provided) > 20 else provided,
                },
            )
            raise HTTPException(
                status_code=401,
                detail={
                    "error": "invalid_signature_format",
                    "message": "Invalid signature header format",
                    "request_id": request_id,
                },
            )

        provided_hex = provided.split("=", 1)[1].strip()
        digest = hmac.new(settings.WEBHOOK_SECRET.encode("utf-8"), body, hashlib.sha256).hexdigest()

        if not hmac.compare_digest(digest, provided_hex):
            logger.warning(
                "Webhook signature mismatch",
                extra={
                    "request_id": request_id,
                    "expected_signature_prefix": digest[:8] + "...",
                    "provided_signature_prefix": provided_hex[:8] + "...",
                },
            )
            raise HTTPException(
                status_code=401,
                detail={
                    "error": "signature_mismatch",
                    "message": "Webhook signature verification failed",
                    "request_id": request_id,
                },
            )

        # Parse payload
        try:
            payload = await request.json()
        except Exception as e:
            logger.error(
                "Failed to parse webhook JSON payload",
                extra={
                    "request_id": request_id,
                    "error": str(e),
                    "content_type": request.headers.get("content-type", "unknown"),
                },
            )
            raise HTTPException(
                status_code=400,
                detail={"error": "invalid_json_payload", "message": "Failed to parse JSON payload", "request_id": request_id},
            )

        # Route events to appropriate Celery tasks
        task_id = None
        # Deduplication using Redis SETNX
        r = redis.from_url(settings.REDIS_URL)
        event_dedupe_key = f"webhook_dedupe:{event_type}:{payload.get("id", hashlib.sha256(body).hexdigest())}"
        if r.setnx(event_dedupe_key, "1"):
            r.expire(event_dedupe_key, 60) # Deduplicate for 60 seconds
        else:
            logger.info(f"Duplicate webhook event received: {event_type}", extra={"request_id": request_id})
            return {"ok": True, "message": f"Duplicate event: {event_type}", "request_id": request_id}

        if event_type == "report.created":
            report_id = payload.get("report", {}).get("id")
            logger.info(f"Enqueuing report.created event for report ID: {report_id}", extra={"request_id": request_id})
            task = process_new_report.delay(payload)
            task_id = task.id
        elif event_type == "status.created":
            status_id = payload.get("status", {}).get("id")
            logger.info(f"Enqueuing status.created event for status ID: {status_id}", extra={"request_id": request_id})
            task = process_new_status.delay(payload)
            task_id = task.id
        else:
            logger.info(f"Received unhandled Mastodon event type: {event_type}", extra={"request_id": request_id})
            return {"ok": True, "message": f"Unhandled event type: {event_type}", "request_id": request_id}

        processing_time = time.time() - start_time
        logger.info(
            "Webhook processed successfully",
            extra={
                "request_id": request_id,
                "event_type": event_type,
                "content_length": content_length,
                "task_id": task_id,
                "processing_time_ms": round(processing_time * 1000, 1),
            },
        )

        return {
            "ok": True,
            "enqueued": True,
            "task_id": task_id,
            "event_type": event_type,
            "processing_time_ms": round(processing_time * 1000, 1),
            "request_id": request_id,
        }

    except HTTPException:
        raise
    except Exception as e:
        processing_time = time.time() - start_time
        logger.error(
            "Webhook processing failed with unexpected error",
            extra={
                "request_id": request_id,
                "error": str(e),
                "error_type": type(e).__name__,
                "processing_time_ms": round(processing_time * 1000, 1),
            },
        )
        raise HTTPException(
            status_code=500,
            detail={"error": "internal_server_error", "message": "Webhook processing failed", "request_id": request_id},
        )


# OAuth Authentication Routes
@app.get("/admin/login", tags=["auth"])
async def admin_login(request: Request, response: Response, popup: bool = False):
    """Initiate OAuth login flow"""
    oauth_config = get_oauth_config()
    
    if not oauth_config.configured:
        raise HTTPException(
            status_code=503,
            detail="OAuth not configured - admin login unavailable"
        )
    
    # Generate state parameter for CSRF protection
    state = secrets.token_urlsafe(32)
    
    # Store state in Redis with short TTL instead of cookies to avoid cross-origin issues
    try:
        import redis
        r = redis.from_url(settings.REDIS_URL, decode_responses=True)
        r.setex(f"oauth_state:{state}", 600, "valid")  # 10 minutes TTL
    except Exception as e:
        logger.warning(f"Failed to store OAuth state in Redis: {e}")
        # Fallback: still try cookie approach
        response.set_cookie(
            key="oauth_state",
            value=state,
            max_age=600,  # 10 minutes
            httponly=False,  # Allow JavaScript access for debugging
            secure=False,  # HTTP only
            samesite="lax"  # More permissive for OAuth redirects
        )
    
    # Use configured redirect URIs or fall back to dynamic generation
    if popup:
        redirect_uri = settings.OAUTH_POPUP_REDIRECT_URI or settings.OAUTH_REDIRECT_URI or f"{request.base_url}admin/popup-callback"
    else:
        redirect_uri = settings.OAUTH_REDIRECT_URI or f"{request.base_url}admin/callback"
    
    # Build authorization URL
    params = {
        "client_id": settings.OAUTH_CLIENT_ID,
        "redirect_uri": redirect_uri,
        "response_type": "code",
        "scope": "read:accounts",
        "state": state
    }
    
    auth_url = f"{str(settings.INSTANCE_BASE).rstrip('/')}/oauth/authorize?" + urlencode(params)
    
    logger.info(f"Redirecting to OAuth login: {auth_url}")
    return RedirectResponse(url=auth_url)


@app.get("/admin/callback", tags=["auth"])
async def admin_callback(
    request: Request, 
    response: Response, 
    code: str = None, 
    error: str = None, 
    state: str = None,
    format: str = "redirect"  # "redirect" or "token"
):
    """Handle OAuth callback"""
    oauth_config = get_oauth_config()
    
    if not oauth_config.configured:
        raise HTTPException(status_code=503, detail="OAuth not configured")
    
    if error:
        logger.warning(f"OAuth error: {error}")
        raise HTTPException(status_code=400, detail=f"OAuth error: {error}")
    
    if not code:
        raise HTTPException(status_code=400, detail="Missing authorization code")
    
    # Verify CSRF state parameter using Redis instead of cookies
    stored_state_cookie = request.cookies.get("oauth_state")
    stored_state_redis = None
    
    try:
        import redis
        r = redis.from_url(settings.REDIS_URL, decode_responses=True)
        redis_key = f"oauth_state:{state}"
        stored_state_redis = r.get(redis_key)
        if stored_state_redis:
            r.delete(redis_key)  # Use once
    except Exception as e:
        logger.warning(f"Failed to retrieve OAuth state from Redis: {e}")
    
    logger.info(f"OAuth callback - cookie_state: {stored_state_cookie}, redis_state: {stored_state_redis}, received_state: {state}")
    
    # Strictly compare state parameter
    if not state or (state != stored_state_cookie and state != stored_state_redis):
        logger.warning(f"OAuth CSRF state mismatch - cookie: {stored_state_cookie}, redis: {stored_state_redis}, received: {state}")
        raise HTTPException(status_code=400, detail="Invalid state parameter")
    
    # Clear the state cookie
    response.set_cookie(
        key="oauth_state",
        value="",
        max_age=0,
        httponly=False,
        secure=False,
        samesite="lax"
    )
    
    try:
        # Exchange code for access token using generated client
        from app.clients.mastodon.client import Client
        
        # Determine the correct redirect URI based on the context
        # If format=token, this is from a popup, so use popup-callback URI
        # Use the same base URL logic as in the login endpoint to ensure consistency
        if format == "token":
            # Extract the base URL from the configured redirect URI if available
            if settings.OAUTH_REDIRECT_URI:
                # Replace /admin/callback with /admin/popup-callback
                redirect_uri = settings.OAUTH_REDIRECT_URI.replace("/admin/callback", "/admin/popup-callback")
            else:
                redirect_uri = f"{request.base_url}admin/popup-callback"
        else:
            redirect_uri = settings.OAUTH_REDIRECT_URI or f"{request.base_url}admin/callback"
        
        # Use generated client for OAuth token exchange
        oauth_client = Client(base_url=str(settings.INSTANCE_BASE))
        
        # Prepare token exchange data
        token_data = {
            "client_id": settings.OAUTH_CLIENT_ID,
            "client_secret": settings.OAUTH_CLIENT_SECRET,
            "code": code,
            "grant_type": "authorization_code",
            "redirect_uri": redirect_uri,
        }
        
        # Use the generated client's HTTP session for consistency
        async with oauth_client.get_async_httpx_client() as http_client:
            token_response = await http_client.post("/oauth/token", data=token_data)
        
        if token_response.status_code != 200:
            logger.error(f"Token exchange failed: {token_response.status_code}")
            raise HTTPException(status_code=400, detail="Failed to exchange authorization code")
        
        token_json = token_response.json()
        access_token = token_json.get("access_token")
        
        if not access_token:
            raise HTTPException(status_code=400, detail="No access token received")
        
        # Fetch user information
        user = await oauth_config.fetch_user_info(access_token)
        
        if not user:
            raise HTTPException(status_code=400, detail="Failed to fetch user information")
        
        if not user.is_admin:
            logger.warning(f"Non-admin user attempted login: {user.acct}")
            raise HTTPException(status_code=403, detail="Admin access required")
        
        logger.info(f"Admin user logged in: {user.acct}")
        
        # Handle different response formats
        if format == "token":
            # Return JWT token for API access
            jwt_config = get_jwt_config()
            token = jwt_config.create_access_token(user.model_dump())
            
            return {
                "access_token": token,
                "token_type": "bearer",
                "user": user.model_dump()
            }
        else:
            # Traditional redirect with session cookie
            create_session_cookie(response, user, settings)
            
            # Redirect to dashboard
            # For development, redirect to the frontend dev server
            frontend_url = "http://localhost:5173"
            return RedirectResponse(url=frontend_url, status_code=302)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"OAuth callback error: {e}")
        raise HTTPException(status_code=500, detail="Authentication failed")


@app.get("/admin/popup-callback", response_class=HTMLResponse, tags=["auth"])
async def admin_popup_callback(request: Request, code: str = None, error: str = None, state: str = None):
    """Handle OAuth callback for popup windows - returns HTML that communicates with parent"""
    oauth_callback_html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>OAuth Callback</title>
        <style>
            body {{
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                padding: 20px;
                text-align: center;
                background: #f5f5f5;
            }}
            .container {{
                max-width: 400px;
                margin: 50px auto;
                background: white;
                padding: 30px;
                border-radius: 8px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }}
            .loading {{
                color: #666;
            }}
            .success {{
                color: #28a745;
            }}
            .error {{
                color: #dc3545;
            }}
            .spinner {{
                border: 2px solid #f3f3f3;
                border-top: 2px solid #3498db;
                border-radius: 50%;
                width: 20px;
                height: 20px;
                animation: spin 1s linear infinite;
                margin: 10px auto;
            }}
            @keyframes spin {{
                0% {{ transform: rotate(0deg); }}
                100% {{ transform: rotate(360deg); }}
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div id="status" class="loading">
                <div class="spinner"></div>
                <p>Completing authentication...</p>
            </div>
        </div>

        <script>
            (async function() {{
                const urlParams = new URLSearchParams(window.location.search);
                const code = urlParams.get('code');
                const error = urlParams.get('error');
                const state = urlParams.get('state');

                try {{
                    if (error) {{
                        throw new Error(error);
                    }}

                    if (!code) {{
                        throw new Error('No authorization code received');
                    }}

                    // Exchange code for token
                    const response = await fetch(`/admin/callback?format=token&code=${{code}}&state=${{state}}`);
                    
                    if (!response.ok) {{
                        const text = await response.text();
                        throw new Error(`${{response.status}}: ${{text}}`);
                    }}

                    const authData = await response.json();

                    // Show success
                    document.getElementById('status').innerHTML = `
                        <div class="success">
                            <p>✅ Authentication successful!</p>
                            <p>Welcome, ${{authData.user.display_name}}!</p>
                            <p>This window will close automatically...</p>
                        </div>
                    `;

                    // Send auth data to parent window
                    if (window.opener) {{
                        window.opener.postMessage({{
                            type: 'oauth-success',
                            auth: authData
                        }}, '{settings.UI_ORIGIN}');
                    }}

                    // Close window after a short delay
                    setTimeout(() => {{
                        window.close();
                    }}, 2000);

                }} catch (error) {{
                    console.error('OAuth callback error:', error);
                    
                    // Show error
                    document.getElementById('status').innerHTML = `
                        <div class="error">
                            <p>❌ Authentication failed</p>
                            <p>${{error.message}}</p>
                            <p>This window will close automatically...</p>
                        </div>
                    `;

                    // Send error to parent window
                    if (window.opener) {{
                        window.opener.postMessage({{
                            type: 'oauth-error',
                            error: error.message
                        }}, '{settings.UI_ORIGIN}');
                    }}

                    // Close window after a short delay
                    setTimeout(() => {{
                        window.close();
                    }}, 3000);
                }}
            }})();
        </script>
    </body>
    </html>
    """
    return oauth_callback_html


@app.post("/admin/logout", tags=["auth"])
async def admin_logout(response: Response):
    """Logout and clear session"""
    clear_session_cookie(response, settings)
    return {"logged_out": True}


@app.get("/api/v1/me", tags=["auth"])
async def get_current_user_info(current_user: User = Depends(require_authenticated_hybrid)):
    """Get current user information"""
    return {
        "id": current_user.id,
        "username": current_user.username,
        "acct": current_user.acct,
        "display_name": current_user.display_name,
        "is_admin": current_user.is_admin,
        "avatar": current_user.avatar
    }


# Analytics and Dashboard Endpoints
@app.get("/analytics/overview", tags=["analytics"])
def get_analytics_overview(_: User = Depends(require_admin_hybrid)):
    """Get overview metrics for the dashboard"""
    try:
        with SessionLocal() as db:
            # Time ranges
            now = datetime.utcnow()
            last_24h = now - timedelta(hours=24)
            last_7d = now - timedelta(days=7)
            last_30d = now - timedelta(days=30)

            # Total counts
            total_accounts = db.query(func.count(Account.id)).scalar() or 0
            total_analyses = db.query(func.count(Analysis.id)).scalar() or 0
            total_reports = db.query(func.count(Report.id)).scalar() or 0

            # Recent activity (last 24h)
            recent_analyses = db.query(func.count(Analysis.id)).filter(Analysis.created_at >= last_24h).scalar() or 0
            recent_reports = db.query(func.count(Report.id)).filter(Report.created_at >= last_24h).scalar() or 0

            # Rule effectiveness (analyses by rule)
            rule_stats = (
                db.query(
                    Analysis.rule_key, func.count(Analysis.id).label("count"), func.avg(Analysis.score).label("avg_score")
                )
                .group_by(Analysis.rule_key)
                .all()
            )

            # Top domains with most activity
            domain_stats = (
                db.query(Account.domain, func.count(Analysis.id).label("analysis_count"))
                .join(Analysis, Account.mastodon_account_id == Analysis.mastodon_account_id)
                .group_by(Account.domain)
                .order_by(desc("analysis_count"))
                .limit(10)
                .all()
            )

            return {
                "totals": {"accounts": total_accounts, "analyses": total_analyses, "reports": total_reports},
                "recent_24h": {"analyses": recent_analyses, "reports": recent_reports},
                "rules": [
                    {
                        "rule_key": rule.rule_key,
                        "count": rule.count,
                        "avg_score": float(rule.avg_score) if rule.avg_score else 0,
                    }
                    for rule in rule_stats
                ],
                "top_domains": [{"domain": domain.domain, "analysis_count": domain.analysis_count} for domain in domain_stats],
            }
    except Exception as e:
        logger.error("Failed to fetch analytics overview", extra={"error": str(e), "error_type": type(e).__name__})
        raise HTTPException(
            status_code=500, detail={"error": "analytics_fetch_failed", "message": "Failed to fetch analytics overview"}
        )


@app.get("/analytics/timeline", tags=["analytics"])
def get_analytics_timeline(days: int = 7, _: User = Depends(require_admin_hybrid)):
    """Get timeline data for analyses and reports"""
    try:
        if days < 1 or days > 365:
            raise HTTPException(
                status_code=400,
                detail={"error": "invalid_days_parameter", "message": "Days parameter must be between 1 and 365"},
            )

        with SessionLocal() as db:
            end_date = datetime.utcnow()
            start_date = end_date - timedelta(days=days)

            # Daily analysis counts
            daily_analyses = (
                db.query(func.date(Analysis.created_at).label("date"), func.count(Analysis.id).label("count"))
                .filter(Analysis.created_at >= start_date)
                .group_by(func.date(Analysis.created_at))
                .order_by("date")
                .all()
            )

            # Daily report counts
            daily_reports = (
                db.query(func.date(Report.created_at).label("date"), func.count(Report.id).label("count"))
                .filter(Report.created_at >= start_date)
                .group_by(func.date(Report.created_at))
                .order_by("date")
                .all()
            )

            return {
                "analyses": [{"date": str(item.date), "count": item.count} for item in daily_analyses],
                "reports": [{"date": str(item.date), "count": item.count} for item in daily_reports],
            }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            "Failed to fetch analytics timeline", extra={"error": str(e), "error_type": type(e).__name__, "days": days}
        )
        raise HTTPException(
            status_code=500, detail={"error": "timeline_fetch_failed", "message": "Failed to fetch analytics timeline"}
        )


@app.get("/analytics/accounts", tags=["analytics"])
def get_account_details(limit: int = 50, offset: int = 0, _: User = Depends(require_admin_hybrid)):
    """Get detailed account information with analysis counts"""
    with SessionLocal() as db:
        accounts = (
            db.query(
                Account,
                func.count(Analysis.id).label("analysis_count"),
                func.count(Report.id).label("report_count"),
                func.max(Analysis.created_at).label("last_analysis"),
            )
            .outerjoin(Analysis, Account.mastodon_account_id == Analysis.mastodon_account_id)
            .outerjoin(Report, Account.mastodon_account_id == Report.mastodon_account_id)
            .group_by(Account.id)
            .order_by(desc("analysis_count"))
            .offset(offset)
            .limit(limit)
            .all()
        )

        return {
            "accounts": [
                {
                    "id": acc.Account.id,
                    "mastodon_account_id": acc.Account.mastodon_account_id,
                    "acct": acc.Account.acct,
                    "domain": acc.Account.domain,
                    "last_checked_at": acc.Account.last_checked_at.isoformat() if acc.Account.last_checked_at else None,
                    "analysis_count": acc.analysis_count or 0,
                    "report_count": acc.report_count or 0,
                    "last_analysis": acc.last_analysis.isoformat() if acc.last_analysis else None,
                }
                for acc in accounts
            ]
        }


@app.get("/analytics/reports", tags=["analytics"])
def get_report_details(limit: int = 50, offset: int = 0, _: User = Depends(require_admin_hybrid)):
    """Get detailed report information"""
    with SessionLocal() as db:
        reports = (
            db.query(Report, Account.acct, Account.domain)
            .join(Account, Report.mastodon_account_id == Account.mastodon_account_id)
            .order_by(desc(Report.created_at))
            .offset(offset)
            .limit(limit)
            .all()
        )

        return {
            "reports": [
                {
                    "id": report.Report.id,
                    "mastodon_account_id": report.Report.mastodon_account_id,
                    "account": f"{report.acct}@{report.domain}",
                    "status_id": report.Report.status_id,
                    "mastodon_report_id": report.Report.mastodon_report_id,
                    "comment": report.Report.comment,
                    "created_at": report.Report.created_at.isoformat(),
                }
                for report in reports
            ]
        }


@app.get("/analytics/analyses/{account_id}", tags=["analytics"])
def get_account_analyses(account_id: str, limit: int = 50, offset: int = 0, _: User = Depends(require_admin_hybrid)):
    """Get detailed analysis information for a specific account including enhanced scan data"""
    with SessionLocal() as db:
        # Get traditional analyses
        analyses = (
            db.query(Analysis)
            .filter(Analysis.mastodon_account_id == account_id)
            .order_by(desc(Analysis.created_at))
            .offset(offset)
            .limit(limit)
            .all()
        )
        
        # Get enhanced content scans
        content_scans = (
            db.query(ContentScan)
            .filter(ContentScan.mastodon_account_id == account_id)
            .order_by(desc(ContentScan.last_scanned_at))
            .limit(limit // 2)  # Get fewer of these to avoid overwhelming
            .all()
        )

        # Convert traditional analyses
        traditional_analyses = [
            {
                "id": analysis.id,
                "status_id": analysis.status_id,
                "rule_key": analysis.rule_key,
                "score": float(analysis.score),
                "evidence": analysis.evidence,
                "created_at": analysis.created_at.isoformat(),
                "scan_type": "traditional"
            }
            for analysis in analyses
        ]
        
        # Convert enhanced content scans
        enhanced_scans = [
            {
                "id": scan.id,
                "status_id": scan.status_id,
                "content_hash": scan.content_hash,
                "scan_type": scan.scan_type,
                "scan_result": scan.scan_result,
                "rules_version": scan.rules_version,
                "last_scanned_at": scan.last_scanned_at.isoformat() if scan.last_scanned_at else None,
                "needs_rescan": scan.needs_rescan,
                "rule_key": "enhanced_scan",
                "score": scan.scan_result.get("total_score", 0.0) if scan.scan_result else 0.0,
                "evidence": scan.scan_result,
                "created_at": scan.last_scanned_at.isoformat() if scan.last_scanned_at else None
            }
            for scan in content_scans
        ]
        
        # Combine and sort by date
        all_analyses = traditional_analyses + enhanced_scans
        all_analyses.sort(key=lambda x: x["created_at"] or "", reverse=True)

        return {
            "analyses": all_analyses[:limit]
        }


@app.get("/rules/current", tags=["rules"])
def get_current_rules(_: User = Depends(require_admin_hybrid)):
    """Get current rule configuration including database rules"""
    all_rules, config, _ = rule_service.get_active_rules()
    return {
        "rules": {
            **all_rules,
            "report_threshold": config.get("report_threshold", 1.0)
        },
        "report_threshold": config.get("report_threshold", 1.0)
    }


@app.get("/rules", tags=["rules"])
def list_rules(_: User = Depends(require_admin_hybrid)):
    """List all rules (file-based and database rules)"""
    all_rules, _, _ = rule_service.get_active_rules()
    response = []
    
    # Convert to flat list for easier frontend consumption
    for rule_type, type_rules in all_rules.items():
        for rule in type_rules:
            response.append({
                **rule,
                "rule_type": rule_type
            })
    
    return {"rules": response}


@app.post("/rules", tags=["rules"])
def create_rule(
    rule_data: dict, 
    _: User = Depends(require_admin_hybrid),
    session: Session = Depends(get_db_session)
):
    """Create a new rule"""
    try:
        # Validate required fields
        required_fields = ["name", "rule_type", "pattern", "weight"]
        for field in required_fields:
            if field not in rule_data:
                raise HTTPException(
                    status_code=400, 
                    detail={
                        "error": f"Missing required field: {field}",
                        "required_fields": required_fields,
                        "help": "Use GET /rules/help for examples and guidance"
                    }
                )
        
        # Validate rule_type
        valid_types = ["username_regex", "display_name_regex", "content_regex"]
        if rule_data["rule_type"] not in valid_types:
            raise HTTPException(
                status_code=400, 
                detail={
                    "error": f"Invalid rule_type: {rule_data['rule_type']}",
                    "valid_types": valid_types,
                    "help": "Use GET /rules/help to see examples for each rule type"
                }
            )
        
        # Validate weight
        try:
            weight = float(rule_data["weight"])
            if weight < 0 or weight > 5.0:
                raise ValueError("Weight must be between 0 and 5.0")
        except (ValueError, TypeError) as e:
            raise HTTPException(
                status_code=400,
                detail={
                    "error": f"Invalid weight: {str(e)}",
                    "guidelines": "Weight should be 0.1-0.3 (mild), 0.4-0.6 (moderate), 0.7-0.9 (strong), 1.0+ (very strong)",
                    "help": "Use GET /rules/help for weight guidelines and examples"
                }
            )
        
        # Test regex pattern
        try:
            re.compile(rule_data["pattern"])
        except re.error as e:
            # Provide specific suggestions based on rule type
            suggestions = [
                "Check for unescaped special characters",
                "Ensure balanced parentheses and brackets", 
                "Test on regex101.com first",
                "Use POST /rules/validate-pattern to test your pattern"
            ]
            
            # Add rule-type specific suggestions
            if rule_data["rule_type"] == "username_regex":
                suggestions.extend([
                    "Username patterns: ^suspicious_prefix, _bot$, ^[0-9]+$",
                    "Remember usernames don't include @ symbol"
                ])
            elif rule_data["rule_type"] == "display_name_regex":
                suggestions.extend([
                    "Display name patterns: [🔥💰], URGENT|BUY NOW, ^Admin$",
                    "Display names can contain emojis and spaces"
                ])
            elif rule_data["rule_type"] == "content_regex":
                suggestions.extend([
                    "Content patterns: https?://[^\\s]+, #(crypto|forex), (?i)(buy.*now)",
                    "Use (?i) for case-insensitive matching"
                ])
                
            raise HTTPException(
                status_code=400, 
                detail={
                    "error": f"Invalid regex pattern: {str(e)}",
                    "pattern": rule_data["pattern"],
                    "rule_type": rule_data["rule_type"],
                    "suggestions": suggestions
                }
            )
        
        # Create rule
        new_rule = Rule(
            name=rule_data["name"],
            rule_type=rule_data["rule_type"],
            pattern=rule_data["pattern"],
            weight=rule_data["weight"],
            enabled=rule_data.get("enabled", True),
            is_default=False
        )
        
        session.add(new_rule)
        session.commit()
        session.refresh(new_rule)
        
        # Reload rules to include the new one
        rule_service.load_rules_from_database()
        
        return {
            "id": new_rule.id,
            "name": new_rule.name,
            "rule_type": new_rule.rule_type,
            "pattern": new_rule.pattern,
            "weight": float(new_rule.weight),
            "enabled": new_rule.enabled,
            "is_default": new_rule.is_default
        }
        
    except HTTPException:
        raise
    except Exception as e:
        session.rollback()
        logger.error("Failed to create rule", extra={"error": str(e), "rule_data": rule_data})
        raise HTTPException(status_code=500, detail="Failed to create rule")


@app.get("/rules/help", tags=["rules"])
def get_rule_creation_help():
    """Get comprehensive help text and examples for creating rules"""
    return {
        "rule_types": {
            "username_regex": {
                "description": "Matches against the username of an account",
                "field_name": "Username Pattern",
                "examples": [
                    {
                        "name": "Spam Bot Usernames",
                        "pattern": r"^(spam|bot|fake).*\d{3,}$",
                        "weight": 1.0,
                        "description": "Matches usernames starting with 'spam', 'bot', or 'fake' followed by 3+ digits",
                        "matches": ["spam123", "bot4567", "fake999"],
                        "non_matches": ["spammer", "robot", "fake12"]
                    },
                    {
                        "name": "Random Character Usernames",
                        "pattern": r"^[a-zA-Z]{1,3}\d{8,}$",
                        "weight": 0.8,
                        "description": "Matches very short letter combinations followed by long number sequences",
                        "matches": ["abc12345678", "xy987654321", "z123456789"],
                        "non_matches": ["alice123", "user4567", "realname99"]
                    },
                    {
                        "name": "Suspicious Patterns",
                        "pattern": r".*(crypto|nft|invest|money|rich|profit).*",
                        "weight": 0.6,
                        "description": "Matches usernames containing financial/crypto keywords",
                        "matches": ["crypto_expert", "nft_trader", "easy_money"],
                        "non_matches": ["photographer", "artist", "writer"]
                    }
                ]
            },
            "display_name_regex": {
                "description": "Matches against the display name of an account",
                "field_name": "Display Name Pattern", 
                "examples": [
                    {
                        "name": "Empty or Suspicious Display Names",
                        "pattern": r"^(|user\d+|account\d+|temp.*)$",
                        "weight": 0.5,
                        "description": "Matches empty, generic, or temporary-looking display names",
                        "matches": ["", "user123", "account456", "temp_user"],
                        "non_matches": ["John Smith", "Artist Name", "Real Person"]
                    },
                    {
                        "name": "Excessive Emojis",
                        "pattern": r"[\u{1F600}-\u{1F64F}\u{1F300}-\u{1F5FF}\u{1F680}-\u{1F6FF}\u{1F1E0}-\u{1F1FF}]{5,}",
                        "weight": 0.4,
                        "description": "Matches display names with 5 or more consecutive emojis",
                        "matches": ["😀😃😄😁😆", "🚀🚀🚀🚀🚀", "💰💰💰💰💰"],
                        "non_matches": ["Hello 😊", "Artist 🎨", "Name 👋"]
                    },
                    {
                        "name": "Promotion Keywords",
                        "pattern": r".*(free|win|prize|offer|limited|exclusive|urgent).*",
                        "weight": 0.7,
                        "description": "Matches display names with promotional/scam keywords",
                        "matches": ["Free Money!", "Win Big Prize", "Limited Offer"],
                        "non_matches": ["Freelancer", "Winner's Circle", "Prize Committee"]
                    }
                ]
            },
            "content_regex": {
                "description": "Matches against the text content of posts/statuses",
                "field_name": "Content Pattern",
                "examples": [
                    {
                        "name": "Spam URLs",
                        "pattern": r"https?://[a-zA-Z0-9.-]+\.(tk|ml|ga|cf|gq)/",
                        "weight": 1.5,
                        "description": "Matches suspicious free domain extensions often used for spam",
                        "matches": ["https://spam.tk/", "http://scam.ml/offer", "https://fake.ga/"],
                        "non_matches": ["https://google.com/", "https://example.org/", "https://site.net/"]
                    },
                    {
                        "name": "Cryptocurrency Scams",
                        "pattern": r".*(send.*bitcoin|free.*crypto|double.*coins|invest.*btc).*",
                        "weight": 1.2,
                        "description": "Matches common cryptocurrency scam phrases",
                        "matches": ["Send me bitcoin", "Free crypto giveaway", "Double your coins"],
                        "non_matches": ["Bitcoin news", "Crypto education", "Investment advice"]
                    },
                    {
                        "name": "Excessive Hashtags",
                        "pattern": r"(#\w+\s*){10,}",
                        "weight": 0.6,
                        "description": "Matches posts with 10 or more hashtags (potential spam)",
                        "matches": ["#spam #tags #everywhere #too #many #hashtags #content #promotion #fake #spam"],
                        "non_matches": ["#photography #art #nature", "#news #politics #society"]
                    }
                ]
            }
        },
        "weight_guidelines": {
            "description": "Rule weight determines how much each match contributes to the final score",
            "guidelines": [
                "0.1 - 0.3: Very mild indicators (suspicious but not conclusive)",
                "0.4 - 0.6: Moderate indicators (worth noting but not alarming)",
                "0.7 - 0.9: Strong indicators (likely problematic content)",
                "1.0 - 1.5: Very strong indicators (almost certainly spam/abuse)",
                "1.6+: Extreme indicators (immediate action warranted)"
            ],
            "examples": {
                "0.2": "Account has default avatar",
                "0.5": "Username contains numbers",
                "0.8": "Content has suspicious keywords",
                "1.0": "Classic spam pattern detected",
                "1.5": "Known scam content pattern"
            }
        },
        "regex_tips": {
            "description": "Tips for creating effective regex patterns",
            "tips": [
                "Use ^ and $ to match the entire string (^pattern$)",
                "Use .* to match any characters before/after your pattern",
                "Use \\d for digits, \\w for word characters, \\s for spaces",
                "Use + for one or more, * for zero or more, {3,} for 3 or more",
                "Use (option1|option2) for alternatives",
                "Escape special characters with backslash: \\. \\? \\+ \\*",
                "Test your patterns carefully - they affect real moderation decisions"
            ],
            "common_patterns": {
                "any_digits": r"\d+",
                "starts_with_word": r"^word.*",
                "contains_word": r".*word.*",
                "ends_with_word": r".*word$",
                "exact_match": r"^exactword$",
                "multiple_options": r"(spam|scam|fake)",
                "repeated_chars": r"(.)\1{3,}",
                "url_pattern": r"https?://[^\s]+",
                "email_pattern": r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
            }
        },
        "testing_guidance": {
            "description": "How to test and validate your rules",
            "steps": [
                "1. Test your regex pattern with online tools first",
                "2. Start with a low weight (0.1-0.3) for new rules",
                "3. Monitor rule performance after creation",
                "4. Adjust weights based on false positive/negative rates",
                "5. Use the dry-run mode to test before applying",
                "6. Review triggered rules regularly for accuracy"
            ],
            "validation_tools": [
                "regex101.com - Test regex patterns online",
                "regexpal.com - Simple regex testing",
                "Built-in pattern validation in this form"
            ]
        },
        "best_practices": {
            "description": "Best practices for effective moderation rules",
            "practices": [
                "Create specific rules rather than overly broad ones",
                "Use descriptive names that explain what the rule catches",
                "Start conservative and adjust based on results",
                "Combine multiple weak indicators rather than one strong one",
                "Regularly review and update rules as spam evolves",
                "Document the reasoning behind each rule",
                "Consider cultural and language differences"
            ]
        }
    }





@app.put("/rules/{rule_id}", tags=["rules"])
def update_rule(
    rule_id: int,
    rule_data: dict,
    _: User = Depends(require_admin_hybrid),
    session: Session = Depends(get_db_session)
):
    """Update an existing rule"""
    try:
        rule = session.query(Rule).filter(Rule.id == rule_id).first()
        if not rule:
            raise HTTPException(status_code=404, detail="Rule not found")
        
        updated_rule = rule_service.update_rule(session, rule_id, rule_data, _.username if _ else "admin")
        
        return {
            "id": updated_rule.id,
            "name": updated_rule.name,
            "rule_type": updated_rule.rule_type,
            "pattern": updated_rule.pattern,
            "weight": float(updated_rule.weight),
            "enabled": updated_rule.enabled,
            "is_default": updated_rule.is_default,
            "message": "Rule updated"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        session.rollback()
        logger.error("Failed to update rule", extra={"error": str(e), "rule_id": rule_id, "rule_data": rule_data})
        raise HTTPException(status_code=500, detail="Failed to update rule")


@app.delete("/rules/{rule_id}", tags=["rules"])
def delete_rule(
    rule_id: int,
    _: User = Depends(require_admin_hybrid),
    session: Session = Depends(get_db_session)
):
    """Delete a rule"""
    try:
        rule_service.delete_rule(session, rule_id)
        
        return {"message": "Rule deleted successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        session.rollback()
        logger.error("Failed to delete rule", extra={"error": str(e), "rule_id": rule_id})
        raise HTTPException(status_code=500, detail="Failed to delete rule")


@app.post("/rules/{rule_id}/toggle", tags=["rules"])
def toggle_rule(
    rule_id: int,
    _: User = Depends(require_admin_hybrid),
    session: Session = Depends(get_db_session)
):
    """Toggle rule enabled/disabled status"""
    try:
        toggled_rule = rule_service.toggle_rule(session, rule_id)
        
        # Invalidate content scans due to rule changes
        enhanced_scanner = EnhancedScanningSystem()
        enhanced_scanner.invalidate_content_scans(rule_changes=True)
        
        return {
            "id": toggled_rule.id,
            "name": toggled_rule.name,
            "enabled": toggled_rule.enabled,
            "message": f"Rule {'enabled' if toggled_rule.enabled else 'disabled'}"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        session.rollback()
        logger.error("Failed to toggle rule", extra={"error": str(e), "rule_id": rule_id})
        raise HTTPException(status_code=500, detail="Failed to toggle rule")


# Enhanced Analytics and Scanning Endpoints
@app.get("/analytics/scanning", tags=["analytics"])
def get_scanning_analytics(_: User = Depends(require_admin_hybrid)):
    """Get real-time scanning analytics and job tracking (15-second refresh)"""
    try:
        enhanced_scanner = EnhancedScanningSystem()
        
        # Get active jobs from Redis/Celery
        import redis
        r = redis.from_url(settings.REDIS_URL, decode_responses=True)
        
        # Get Celery queue length
        queue_length = r.llen("celery") # Assuming default Celery queue name is "celery"

        with SessionLocal() as db:
            # Get active scan sessions
            active_sessions = db.query(ScanSession).filter(ScanSession.status == 'active').all()
            
            # Get recent completed sessions
            recent_sessions = (
                db.query(ScanSession)
                .filter(ScanSession.completed_at.isnot(None))
                .order_by(desc(ScanSession.completed_at))
                .limit(5) # Latest 5 sessions
                .all()
            )

            # Get last federated scan and domain check times
            last_federated_scan_record = db.query(ScanSession.completed_at)
                                    .filter(ScanSession.session_type == 'federated', ScanSession.status == 'completed')
                                    .order_by(desc(ScanSession.completed_at)).first()
            last_domain_check_record = db.query(ScanSession.completed_at)
                                  .filter(ScanSession.session_type == 'domain_check', ScanSession.status == 'completed')
                                  .order_by(desc(ScanSession.completed_at)).first()
            
            # Get content scan statistics
            content_scan_stats = db.query(
                func.count(ContentScan.id).label('total_scans'),
                func.count(ContentScan.id).filter(ContentScan.needs_rescan == True).label('needs_rescan'),
                func.max(ContentScan.last_scanned_at).label('last_scan')
            ).first()
            
            return {
                "active_jobs": [], # Placeholder for actual active Celery jobs if needed
                "scan_sessions": [
                    {
                        "id": session.id,
                        "session_type": session.session_type,
                        "accounts_processed": session.accounts_processed,
                        "total_accounts": session.total_accounts,
                        "started_at": session.started_at.isoformat(),
                        "completed_at": session.completed_at.isoformat() if session.completed_at else None,
                        "status": session.status,
                        "current_cursor": session.current_cursor
                    }
                    for session in active_sessions + recent_sessions
                ],
                "system_status": {
                    "last_federated_scan": last_federated_scan_record[0].isoformat() if last_federated_scan_record else None,
                    "last_domain_check": last_domain_check_record[0].isoformat() if last_domain_check_record else None,
                    "queue_length": queue_length,
                    "system_load": "normal" # Placeholder, can be enhanced with system metrics
                },
                "content_scan_stats": {
                    "total_scans": content_scan_stats.total_scans or 0,
                    "needs_rescan": content_scan_stats.needs_rescan or 0,
                    "last_scan": content_scan_stats.last_scan.isoformat() if content_scan_stats.last_scan else None
                },
                "metadata": {
                    "last_updated": datetime.utcnow().isoformat(),
                    "refresh_interval_seconds": 15,
                    "supports_real_time": True,
                    "data_lag_seconds": 0
                }
            }
            
    except Exception as e:
        logger.error("Failed to get scanning analytics", extra={"error": str(e)})
        raise HTTPException(status_code=500, detail="Failed to get scanning analytics")


@app.get("/analytics/domains", tags=["analytics"])
def get_domain_analytics(_: User = Depends(require_admin_hybrid)):
    """Get domain-level analytics with real-time metrics (15-second refresh capability)"""
    try:
        enhanced_scanner = EnhancedScanningSystem()
        domain_alerts = enhanced_scanner.get_domain_alerts(100)
        
        # Calculate comprehensive summary statistics
        total_domains = len(domain_alerts)
        defederated_count = sum(1 for alert in domain_alerts if alert.get("is_defederated", False))
        high_risk_count = sum(1 for alert in domain_alerts 
                            if alert.get("violation_count", 0) >= alert.get("defederation_threshold", 10) * 0.8
                            and not alert.get("is_defederated", False))
        monitored_count = total_domains - defederated_count
        
        # Get active scanning status
        current_time = datetime.utcnow()
        
        return {
            "summary": {
                "total_domains": total_domains,
                "monitored_domains": monitored_count,
                "high_risk_domains": high_risk_count, 
                "defederated_domains": defederated_count,
                "scan_in_progress": False  # TODO: Get from Redis/Celery
            },
            "domain_alerts": domain_alerts[:20],  # Top 20 for UI
            "metadata": {
                "last_updated": current_time.isoformat(),
                "refresh_interval_seconds": 15,
                "cache_status": "fresh",
                "supports_real_time": True
            }
        }
    except Exception as e:
        logger.error("Failed to fetch domain analytics", extra={"error": str(e)})
        raise HTTPException(status_code=500, detail="Failed to fetch domain analytics")


@app.get("/analytics/rules/statistics", tags=["analytics"])
def get_rule_statistics(_: User = Depends(require_admin_hybrid)):
    """Get comprehensive rule statistics and performance metrics"""
    try:
        rule_stats = rule_service.get_rule_statistics()
        return rule_stats
    except Exception as e:
        logger.error("Failed to fetch rule statistics", extra={"error": str(e)})
        raise HTTPException(status_code=500, detail="Failed to fetch rule statistics")



@app.get("/analytics/domains", tags=["analytics"])
def get_domain_analytics(_: User = Depends(require_admin_hybrid)):
    """Get domain-level analytics with real-time metrics (15-second refresh capability)"""
    try:
        enhanced_scanner = EnhancedScanningSystem()
        domain_alerts = enhanced_scanner.get_domain_alerts(100)
        
        # Calculate comprehensive summary statistics
        total_domains = len(domain_alerts)
        defederated_count = sum(1 for alert in domain_alerts if alert.get("is_defederated", False))
        high_risk_count = sum(1 for alert in domain_alerts 
                            if alert.get("violation_count", 0) >= alert.get("defederation_threshold", 10) * 0.8
                            and not alert.get("is_defederated", False))
        monitored_count = total_domains - defederated_count
        
        # Get active scanning status
        current_time = datetime.utcnow()
        
        return {
            "summary": {
                "total_domains": total_domains,
                "monitored_domains": monitored_count,
                "high_risk_domains": high_risk_count, 
                "defederated_domains": defederated_count,
                "scan_in_progress": False  # TODO: Get from Redis/Celery
            },
            "domain_alerts": domain_alerts[:20],  # Top 20 for UI
            "metadata": {
                "last_updated": current_time.isoformat(),
                "refresh_interval_seconds": 15,
                "cache_status": "fresh",
                "supports_real_time": True
            }
        }
    except Exception as e:
        logger.error("Failed to fetch domain analytics", extra={"error": str(e)})
        raise HTTPException(status_code=500, detail="Failed to fetch domain analytics")


@app.get("/analytics/rules/statistics", tags=["analytics"])
def get_rule_statistics(_: User = Depends(require_admin_hybrid)):
    """Get comprehensive rule statistics and performance metrics"""
    try:
        rule_stats = rules.get_rule_statistics()
        return rule_stats
    except Exception as e:
        logger.error("Failed to fetch rule statistics", extra={"error": str(e)})
        raise HTTPException(status_code=500, detail="Failed to fetch rule statistics")


@app.post("/scanning/federated", tags=["scanning"])
def trigger_federated_scan(
    domains: List[str] = None, 
    _: User = Depends(require_admin_hybrid)
):
    """Trigger a federated content scan with improved error handling"""
    try:
        # Validate domains if provided
        if domains:
            for domain in domains:
                if not domain or len(domain) > 255:
                    raise HTTPException(status_code=400, detail=f"Invalid domain: {domain}")
        
        task = scan_federated_content.delay(domains)
        return {
            "task_id": task.id,
            "message": "Federated scan started",
            "target_domains": domains or "all_active",
            "status": "queued"
        }
    except HTTPException:
        raise
    except ConnectionError as e:
        logger.error("Connection error during federated scan", extra={"error": str(e), "domains": domains})
        raise HTTPException(status_code=503, detail="Cannot connect to Mastodon instance for federated scan")
    except Exception as e:
        error_msg = str(e)
        if "422" in error_msg or "Unprocessable" in error_msg:
            logger.warning("422 error in federated scan - invalid content", extra={"error": error_msg, "domains": domains})
            raise HTTPException(status_code=422, detail="Federated scan failed due to invalid content format")
        elif "Connection refused" in error_msg:
            logger.error("Connection refused during federated scan", extra={"error": error_msg, "domains": domains})
            raise HTTPException(status_code=503, detail="Connection refused - Mastodon instance may be unavailable")
        else:
            logger.error("Failed to trigger federated scan", extra={"error": error_msg, "domains": domains})
            raise HTTPException(status_code=500, detail=f"Failed to trigger federated scan: {error_msg}")


@app.post("/scanning/domain-check", tags=["scanning"])
def trigger_domain_check(_: User = Depends(require_admin_hybrid)):
    """Trigger domain violation check with improved error handling"""
    try:
        task = check_domain_violations.delay()
        return {
            "task_id": task.id,
            "message": "Domain violation check started",
            "status": "queued"
        }
    except ConnectionError as e:
        logger.error("Connection error during domain check", extra={"error": str(e)})
        raise HTTPException(status_code=503, detail="Cannot connect to services for domain validation")
    except Exception as e:
        error_msg = str(e)
        if "Connection refused" in error_msg or "localhost" in error_msg:
            logger.error("Domain validation connection error", extra={"error": error_msg})
            raise HTTPException(status_code=503, detail="Domain validation service unavailable - connection refused")
        elif "hostname defaulting" in error_msg:
            logger.error("Hostname resolution error", extra={"error": error_msg})
            raise HTTPException(status_code=502, detail="Domain hostname resolution failed")
        else:
            logger.error("Failed to trigger domain check", extra={"error": error_msg})
            raise HTTPException(status_code=500, detail=f"Failed to trigger domain check: {error_msg}")


@app.post("/scanning/invalidate-cache", tags=["scanning"])
def invalidate_scan_cache(
    rule_changes: bool = False,
    _: User = Depends(require_admin_hybrid)
):
    """Invalidate content scan cache with frontend update coordination"""
    try:
        enhanced_scanner = EnhancedScanningSystem()
        enhanced_scanner.invalidate_content_scans(rule_changes=rule_changes)
        
        # Store invalidation event in Redis for frontend coordination
        try:
            import redis
            r = redis.from_url(settings.REDIS_URL, decode_responses=True)
            invalidation_event = {
                "type": "cache_invalidation",
                "rule_changes": rule_changes,
                "invalidated_at": datetime.utcnow().isoformat(),
                "invalidated_by": _.username if _ else "system"
            }
            # Store for 5 minutes to allow frontend to detect changes
            r.setex("cache_invalidation_event", 300, json.dumps(invalidation_event))
        except Exception as redis_error:
            logger.warning(f"Failed to store cache invalidation event in Redis: {redis_error}")
        
        return {
            "message": "Scan cache invalidated successfully",
            "rule_changes": rule_changes,
            "invalidated_at": datetime.utcnow().isoformat(),
            "frontend_refresh_recommended": True,
            "invalidated_by": _.username if _ else "system"
        }
    except Exception as e:
        logger.error("Failed to invalidate scan cache", extra={"error": str(e)})
        raise HTTPException(status_code=500, detail="Failed to invalidate scan cache")


@app.get("/scanning/cache-status", tags=["scanning"])
def get_cache_status(_: User = Depends(require_admin_hybrid)):
    """Get cache status and invalidation events for frontend coordination"""
    try:
        import redis
        r = redis.from_url(settings.REDIS_URL, decode_responses=True)
        
        # Check for recent cache invalidation events
        invalidation_data = r.get("cache_invalidation_event")
        
        if invalidation_data:
            invalidation_event = json.loads(invalidation_data)
            return {
                "cache_status": "invalidated",
                "last_invalidation": invalidation_event,
                "refresh_recommended": True
            }
        else:
            return {
                "cache_status": "valid",
                "last_invalidation": None,
                "refresh_recommended": False
            }
            
    except Exception as e:
        logger.error("Failed to get cache status", extra={"error": str(e)})
        return {
            "cache_status": "unknown",
            "last_invalidation": None,
            "refresh_recommended": True,
            "error": "Failed to check cache status"
        }


@app.get("/analytics/scanning", tags=["analytics"])
def get_scanning_analytics(_: User = Depends(require_admin_hybrid)):
    """Get real-time scanning analytics and job tracking (15-second refresh)"""
    try:
        enhanced_scanner = EnhancedScanningSystem()
        
        # Get active jobs from Redis/Celery
        import redis
        r = redis.from_url(settings.REDIS_URL, decode_responses=True)
        
        # Mock active jobs data - in real implementation, get from Celery
        active_jobs = []
        
        # Get scan session progress
        scan_sessions = enhanced_scanner.get_scanning_analytics() if hasattr(enhanced_scanner, 'get_scanning_analytics') else []
        
        current_time = datetime.utcnow()
        
        return {
            "active_jobs": active_jobs,
            "scan_sessions": scan_sessions[:5],  # Latest 5 sessions
            "system_status": {
                "last_federated_scan": None,  # TODO: Get from database
                "last_domain_check": None,    # TODO: Get from database
                "queue_length": 0,            # TODO: Get from Celery
                "system_load": "normal"
            },
            "metadata": {
                "last_updated": current_time.isoformat(),
                "refresh_interval_seconds": 15,
                "supports_real_time": True,
                "data_lag_seconds": 0
            }
        }
        
    except Exception as e:
        logger.error("Failed to get scanning analytics", extra={"error": str(e)})
        raise HTTPException(status_code=500, detail="Failed to get scanning analytics")


# Enhanced Rules Management
@app.post("/rules/bulk-toggle", tags=["rules"])
def bulk_toggle_rules(
    rule_ids: List[int],
    enabled: bool,
    _: User = Depends(require_admin_hybrid),
    session: Session = Depends(get_db_session)
):
    """Toggle multiple rules at once"""
    try:
        updated_rules = []
        for rule_id in rule_ids:
            rule = session.query(Rule).filter(Rule.id == rule_id).first()
            if rule and not rule.is_default:
                rule.enabled = enabled
                updated_rules.append(rule.name)
        
        session.commit()
        
        # Reload rules
        global rules
        rules = Rules.from_database()
        
        # Invalidate content scans due to rule changes
        enhanced_scanner = EnhancedScanningSystem()
        enhanced_scanner.invalidate_content_scans(rule_changes=True)
        
        return {
            "updated_rules": updated_rules,
            "enabled": enabled,
            "message": f"{len(updated_rules)} rules {'enabled' if enabled else 'disabled'}"
        }
        
    except Exception as e:
        session.rollback()
        logger.error("Failed to bulk toggle rules", extra={"error": str(e), "rule_ids": rule_ids})
        raise HTTPException(status_code=500, detail="Failed to bulk toggle rules")


@app.get("/rules/{rule_id}/details", tags=["rules"])
def get_rule_details(
    rule_id: int,
    _: User = Depends(require_admin_hybrid),
    session: Session = Depends(get_db_session)
):
    """Get detailed information about a specific rule"""
    try:
        rule = session.query(Rule).filter(Rule.id == rule_id).first()
        if not rule:
            raise HTTPException(status_code=404, detail="Rule not found")
        
        # Get recent analyses using this rule
        recent_analyses = (
            session.query(Analysis)
            .filter(Analysis.rule_key.like(f"%{rule.name}%"))
            .order_by(desc(Analysis.created_at))
            .limit(10)
            .all()
        )
        
        return {
            "id": rule.id,
            "name": rule.name,
            "rule_type": rule.rule_type,
            "pattern": rule.pattern,
            "weight": float(rule.weight),
            "enabled": rule.enabled,
            "is_default": rule.is_default,
            "trigger_count": rule.trigger_count or 0,
            "last_triggered_at": rule.last_triggered_at.isoformat() if rule.last_triggered_at else None,
            "last_triggered_content": rule.last_triggered_content,
            "created_by": rule.created_by,
            "updated_by": rule.updated_by,
            "description": rule.description,
            "created_at": rule.created_at.isoformat() if rule.created_at else None,
            "updated_at": rule.updated_at.isoformat() if rule.updated_at else None,
            "recent_analyses": [
                {
                    "id": analysis.id,
                    "mastodon_account_id": analysis.mastodon_account_id,
                    "score": float(analysis.score),
                    "created_at": analysis.created_at.isoformat(),
                    "evidence": analysis.evidence
                }
                for analysis in recent_analyses
            ]
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to get rule details", extra={"error": str(e), "rule_id": rule_id})
        raise HTTPException(status_code=500, detail="Failed to get rule details")
