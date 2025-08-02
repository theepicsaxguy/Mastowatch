import hashlib
import hmac
import logging
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

from app.auth import require_api_key
from app.config import get_settings
from app.db import SessionLocal
from app.logging_conf import setup_logging
from app.models import Account, Analysis, Config, Report
from app.oauth import (
    get_oauth_config, 
    get_current_user, 
    require_admin, 
    require_authenticated,
    create_session_cookie,
    clear_session_cookie,
    User
)
from app.jwt_auth import (
    get_jwt_config,
    require_admin_hybrid,
    require_authenticated_hybrid
)
from app.rules import Rules
from app.startup_validation import run_all_startup_validations
from app.tasks.jobs import analyze_and_maybe_report  # reuse pipeline

setup_logging()
logger = logging.getLogger(__name__)

# Run startup validations before anything else
run_all_startup_validations()

app = FastAPI(title="MastoWatch", version="1.0.0")
settings = get_settings()

# Load rules with graceful fallback
try:
    rules = Rules.from_yaml("rules.yml")
    logger.info("Rules loaded successfully")
except FileNotFoundError:
    logger.warning("Rules file not found, using minimal default rules")
    # Create minimal default rules to prevent hard failure
    rules = Rules({"rules": [], "report_threshold": 1.0})
except Exception as e:
    logger.error(f"Failed to parse rules.yml: {e}, using minimal default rules")
    rules = Rules({"rules": [], "report_threshold": 1.0})

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


@app.post("/config/rules/reload", tags=["ops"])
def reload_rules(_: User = Depends(require_admin_hybrid)):
    """Reload rules from rules.yml file"""
    try:
        global rules
        old_sha = rules.ruleset_sha256 if rules else "unknown"

        try:
            rules = Rules.from_yaml("rules.yml")
        except FileNotFoundError as e:
            logger.error("Rules file not found", extra={"error": str(e), "file_path": "rules.yml"})
            raise HTTPException(
                status_code=404,
                detail={"error": "rules_file_not_found", "message": "Rules configuration file (rules.yml) not found"},
            )
        except Exception as e:
            logger.error(
                "Failed to parse rules configuration",
                extra={"error": str(e), "error_type": type(e).__name__, "file_path": "rules.yml"},
            )
            raise HTTPException(
                status_code=400,
                detail={"error": "rules_parse_failed", "message": f"Failed to parse rules configuration: {str(e)}"},
            )

        new_sha = rules.ruleset_sha256

        logger.info(
            "Rules configuration reloaded",
            extra={
                "old_sha": old_sha[:8] if old_sha != "unknown" else old_sha,
                "new_sha": new_sha[:8],
                "sha_changed": old_sha != new_sha,
            },
        )

        return {"reloaded": True, "ruleset_sha256": new_sha, "previous_sha256": old_sha, "changed": old_sha != new_sha}
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to reload rules", extra={"error": str(e), "error_type": type(e).__name__})
        raise HTTPException(
            status_code=500, detail={"error": "rules_reload_failed", "message": f"Failed to reload rules: {str(e)}"}
        )


@app.post("/dryrun/evaluate", tags=["ops"])
async def dryrun_evaluate(payload: dict):
    acct = payload.get("account") or {}
    statuses = payload.get("statuses") or []
    score, hits = rules.eval_account(acct, statuses)
    return {"score": score, "hits": hits}


@app.post("/webhooks/status", tags=["webhooks"])
async def webhook_status(request: Request):
    """Handle incoming status webhooks with signature validation and deduplication"""
    start_time = time.time()
    request_id = f"webhook_{int(start_time * 1000)}"

    try:
        body = await request.body()
        content_length = len(body)

        logger.info(
            "Processing webhook request",
            extra={
                "request_id": request_id,
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

        # Extract account and statuses
        acct = payload.get("account") or {}
        statuses = payload.get("statuses") or ([payload["status"]] if "status" in payload else [])

        if not acct:
            logger.warning(
                "Webhook payload missing account information",
                extra={"request_id": request_id, "payload_keys": list(payload.keys())},
            )
            raise HTTPException(
                status_code=400,
                detail={
                    "error": "missing_account_data",
                    "message": "Missing account information in payload",
                    "request_id": request_id,
                },
            )

        account_id = acct.get("id", "unknown")
        account_acct = acct.get("acct", "unknown")

        # Simple deduplication using Redis (if available)
        dedupe_key = None
        try:
            import redis

            # Create deduplication key from account + statuses
            dedupe_data = f"{account_id}-{len(statuses)}-{hash(str(sorted(s.get('id', '') for s in statuses)))}"
            dedupe_key = hashlib.sha256(dedupe_data.encode()).hexdigest()[:16]

            r = redis.from_url(settings.REDIS_URL)
            if r.get(f"webhook_dedupe:{dedupe_key}"):
                logger.info(
                    "Webhook deduplicated",
                    extra={
                        "request_id": request_id,
                        "dedupe_key": dedupe_key,
                        "account_id": account_id,
                        "account_acct": account_acct,
                    },
                )
                return {
                    "ok": True,
                    "enqueued": False,
                    "reason": "duplicate",
                    "request_id": request_id,
                    "dedupe_key": dedupe_key,
                }

            # Set dedupe key with 5 minute expiry
            r.setex(f"webhook_dedupe:{dedupe_key}", 300, "1")

        except Exception as e:
            logger.warning(
                "Webhook deduplication failed (continuing anyway)",
                extra={"request_id": request_id, "error": str(e), "account_id": account_id},
            )

        # Enqueue for analysis
        try:
            task = analyze_and_maybe_report.delay({"account": acct, "statuses": statuses})
        except Exception as e:
            logger.error(
                "Failed to enqueue webhook for analysis",
                extra={
                    "request_id": request_id,
                    "error": str(e),
                    "account_id": account_id,
                    "account_acct": account_acct,
                    "status_count": len(statuses),
                },
            )
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "task_enqueue_failed",
                    "message": "Failed to enqueue analysis task",
                    "request_id": request_id,
                },
            )

        processing_time = time.time() - start_time
        logger.info(
            "Webhook processed successfully",
            extra={
                "request_id": request_id,
                "content_length": content_length,
                "status_count": len(statuses),
                "account_id": account_id,
                "account_acct": account_acct,
                "task_id": task.id,
                "dedupe_key": dedupe_key,
                "processing_time_ms": round(processing_time * 1000, 1),
            },
        )

        return {
            "ok": True,
            "enqueued": True,
            "task_id": task.id,
            "account_id": account_id,
            "status_count": len(statuses),
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
    
    redirect_uri = settings.OAUTH_REDIRECT_URI or f"{request.base_url}admin/callback"
    
    # For popup login, use a special callback endpoint
    if popup:
        redirect_uri = f"{request.base_url}admin/popup-callback"
    
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
    
    # Accept state from either cookie or Redis
    if not stored_state_cookie and not stored_state_redis:
        logger.warning(f"OAuth CSRF state missing - cookie: {stored_state_cookie}, redis: {stored_state_redis}, received: {state}")
        raise HTTPException(status_code=400, detail="Invalid state parameter")
        
    if not state:
        logger.warning("OAuth callback missing state parameter")
        raise HTTPException(status_code=400, detail="Missing state parameter")
    
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
    oauth_callback_html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>OAuth Callback</title>
        <style>
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                padding: 20px;
                text-align: center;
                background: #f5f5f5;
            }
            .container {
                max-width: 400px;
                margin: 50px auto;
                background: white;
                padding: 30px;
                border-radius: 8px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }
            .loading {
                color: #666;
            }
            .success {
                color: #28a745;
            }
            .error {
                color: #dc3545;
            }
            .spinner {
                border: 2px solid #f3f3f3;
                border-top: 2px solid #3498db;
                border-radius: 50%;
                width: 20px;
                height: 20px;
                animation: spin 1s linear infinite;
                margin: 10px auto;
            }
            @keyframes spin {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }
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
            (async function() {
                const urlParams = new URLSearchParams(window.location.search);
                const code = urlParams.get('code');
                const error = urlParams.get('error');
                const state = urlParams.get('state');

                try {
                    if (error) {
                        throw new Error(error);
                    }

                    if (!code) {
                        throw new Error('No authorization code received');
                    }

                    // Exchange code for token
                    const response = await fetch(`/admin/callback?format=token&code=${code}&state=${state}`);
                    
                    if (!response.ok) {
                        const text = await response.text();
                        throw new Error(`${response.status}: ${text}`);
                    }

                    const authData = await response.json();

                    // Show success
                    document.getElementById('status').innerHTML = `
                        <div class="success">
                            <p>✅ Authentication successful!</p>
                            <p>Welcome, ${authData.user.display_name}!</p>
                            <p>This window will close automatically...</p>
                        </div>
                    `;

                    // Send auth data to parent window
                    if (window.opener) {
                        window.opener.postMessage({
                            type: 'oauth-success',
                            auth: authData
                        }, 'http://localhost:5173'); // Send to frontend
                    }

                    // Close window after a short delay
                    setTimeout(() => {
                        window.close();
                    }, 2000);

                } catch (error) {
                    console.error('OAuth callback error:', error);
                    
                    // Show error
                    document.getElementById('status').innerHTML = `
                        <div class="error">
                            <p>❌ Authentication failed</p>
                            <p>${error.message}</p>
                            <p>This window will close automatically...</p>
                        </div>
                    `;

                    // Send error to parent window
                    if (window.opener) {
                        window.opener.postMessage({
                            type: 'oauth-error',
                            error: error.message
                        }, 'http://localhost:5173'); // Send to frontend
                    }

                    // Close window after a short delay
                    setTimeout(() => {
                        window.close();
                    }, 3000);
                }
            })();
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
    """Get detailed analysis information for a specific account"""
    with SessionLocal() as db:
        analyses = (
            db.query(Analysis)
            .filter(Analysis.mastodon_account_id == account_id)
            .order_by(desc(Analysis.created_at))
            .offset(offset)
            .limit(limit)
            .all()
        )

        return {
            "analyses": [
                {
                    "id": analysis.id,
                    "status_id": analysis.status_id,
                    "rule_key": analysis.rule_key,
                    "score": float(analysis.score),
                    "evidence": analysis.evidence,
                    "created_at": analysis.created_at.isoformat(),
                }
                for analysis in analyses
            ]
        }


@app.get("/rules/current", tags=["rules"])
def get_current_rules(_: User = Depends(require_admin_hybrid)):
    """Get current rule configuration"""
    return {"rules": rules.cfg, "report_threshold": rules.cfg.get("report_threshold", 1.0)}
