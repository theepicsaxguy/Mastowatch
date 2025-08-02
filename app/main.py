import hmac, hashlib, logging, time
from fastapi import FastAPI, Request, HTTPException, Depends, status
from fastapi.responses import PlainTextResponse, HTMLResponse
from sqlalchemy import text
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from app.logging_conf import setup_logging
from app.config import get_settings
from app.startup_validation import run_all_startup_validations
from app.rules import Rules
from pydantic import BaseModel
from app.db import SessionLocal
from app.models import Config, Account, Analysis, Report
from app.auth import require_api_key
from app.tasks.jobs import analyze_and_maybe_report  # reuse pipeline
from sqlalchemy import func, desc
from datetime import datetime, timedelta
from typing import List, Dict, Any

setup_logging()
logger = logging.getLogger(__name__)

# Run startup validations before anything else
run_all_startup_validations()

app = FastAPI(title="MastoWatch", version="1.0.0")
settings = get_settings()
rules = Rules.from_yaml("rules.yml")

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
        "timestamp": datetime.utcnow().isoformat()
    }
    
    try:
        from app.db import SessionLocal
        import redis
        
        # Test database connection
        try:
            with SessionLocal() as db:
                db.execute(text("SELECT 1"))
                health_data["db_ok"] = True
                logger.debug("Database health check passed")
        except Exception as e:
            logger.error(
                "Database health check failed",
                extra={
                    "error": str(e),
                    "error_type": type(e).__name__
                }
            )
            health_data["db_ok"] = False
            
        # Test Redis connection  
        try:
            r = redis.from_url(settings.REDIS_URL)
            health_data["redis_ok"] = r.ping()
            logger.debug("Redis health check passed")
        except Exception as e:
            logger.error(
                "Redis health check failed",
                extra={
                    "error": str(e),
                    "error_type": type(e).__name__
                }
            )
            health_data["redis_ok"] = False
            
        health_data["ok"] = health_data["db_ok"] and health_data["redis_ok"]
        health_data["response_time_ms"] = round((time.time() - start_time) * 1000, 1)
        
        if not health_data["ok"]:
            logger.warning(
                "Health check failed",
                extra={
                    "db_ok": health_data["db_ok"],
                    "redis_ok": health_data["redis_ok"],
                    "response_time_ms": health_data["response_time_ms"]
                }
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
                "response_time_ms": round((time.time() - start_time) * 1000, 1)
            }
        )
        raise HTTPException(
            status_code=500, 
            detail={
                "error": "health_check_failed",
                "message": "Health check endpoint encountered an error"
            }
        )

@app.get("/metrics", response_class=PlainTextResponse, tags=["ops"])
def metrics():
    return PlainTextResponse(generate_latest(), media_type=CONTENT_TYPE_LATEST)

class DryRunToggle(BaseModel):
    dry_run: bool
    updated_by: str | None = None

@app.post("/config/dry_run", tags=["ops"])
def set_dry_run(body: DryRunToggle, _: bool = Depends(require_api_key)):
    """Toggle dry run mode and persist to database"""
    try:
        if body.dry_run is None:
            raise HTTPException(
                status_code=400, 
                detail={
                    "error": "missing_dry_run_flag",
                    "message": "dry_run flag cannot be null"
                }
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
                        "updated_by": body.updated_by
                    }
                )
                raise HTTPException(
                    status_code=500,
                    detail={
                        "error": "database_update_failed",
                        "message": "Failed to persist configuration to database"
                    }
                )
            
        settings.DRY_RUN = bool(body.dry_run)
        logger.info(
            "Dry run mode configuration updated",
            extra={
                "dry_run": body.dry_run,
                "updated_by": body.updated_by or "unknown",
                "persisted": True
            }
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
                "requested_dry_run": getattr(body, 'dry_run', None),
                "updated_by": getattr(body, 'updated_by', None)
            }
        )
        raise HTTPException(
            status_code=500, 
            detail={
                "error": "configuration_update_failed",
                "message": "Failed to update dry run setting"
            }
        )

class PanicToggle(BaseModel):
    panic_stop: bool
    updated_by: str | None = None

@app.post("/config/panic_stop", tags=["ops"])
def set_panic_stop(body: PanicToggle, _: bool = Depends(require_api_key)):
    """Toggle panic stop mode and persist to database"""
    try:
        if body.panic_stop is None:
            raise HTTPException(
                status_code=400, 
                detail={
                    "error": "missing_panic_stop_flag",
                    "message": "panic_stop flag cannot be null"
                }
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
                        "updated_by": body.updated_by
                    }
                )
                raise HTTPException(
                    status_code=500,
                    detail={
                        "error": "database_update_failed",
                        "message": "Failed to persist configuration to database"
                    }
                )
            
        settings.PANIC_STOP = bool(body.panic_stop)
        logger.warning(
            "Panic stop mode configuration updated",
            extra={
                "panic_stop": body.panic_stop,
                "updated_by": body.updated_by or "unknown",
                "persisted": True
            }
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
                "requested_panic_stop": getattr(body, 'panic_stop', None),
                "updated_by": getattr(body, 'updated_by', None)
            }
        )
        raise HTTPException(
            status_code=500, 
            detail={
                "error": "configuration_update_failed",
                "message": "Failed to update panic stop setting"
            }
        )

@app.post("/config/rules/reload", tags=["ops"])
def reload_rules(_: bool = Depends(require_api_key)):
    """Reload rules from rules.yml file"""
    try:
        global rules
        old_sha = rules.ruleset_sha256 if rules else "unknown"
        
        try:
            rules = Rules.from_yaml("rules.yml")
        except FileNotFoundError as e:
            logger.error(
                "Rules file not found",
                extra={
                    "error": str(e),
                    "file_path": "rules.yml"
                }
            )
            raise HTTPException(
                status_code=404,
                detail={
                    "error": "rules_file_not_found",
                    "message": "Rules configuration file (rules.yml) not found"
                }
            )
        except Exception as e:
            logger.error(
                "Failed to parse rules configuration",
                extra={
                    "error": str(e),
                    "error_type": type(e).__name__,
                    "file_path": "rules.yml"
                }
            )
            raise HTTPException(
                status_code=400,
                detail={
                    "error": "rules_parse_failed",
                    "message": f"Failed to parse rules configuration: {str(e)}"
                }
            )
        
        new_sha = rules.ruleset_sha256
        
        logger.info(
            "Rules configuration reloaded",
            extra={
                "old_sha": old_sha[:8] if old_sha != "unknown" else old_sha,
                "new_sha": new_sha[:8],
                "sha_changed": old_sha != new_sha
            }
        )
        
        return {
            "reloaded": True, 
            "ruleset_sha256": new_sha,
            "previous_sha256": old_sha,
            "changed": old_sha != new_sha
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            "Failed to reload rules",
            extra={
                "error": str(e),
                "error_type": type(e).__name__
            }
        )
        raise HTTPException(
            status_code=500, 
            detail={
                "error": "rules_reload_failed",
                "message": f"Failed to reload rules: {str(e)}"
            }
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
                "user_agent": request.headers.get("user-agent", "unknown")
            }
        )
        
        # Validate webhook is configured
        if not settings.WEBHOOK_SECRET:
            logger.warning(
                "Webhook received but WEBHOOK_SECRET not configured",
                extra={"request_id": request_id}
            )
            raise HTTPException(
                status_code=503, 
                detail={
                    "error": "webhook_not_configured",
                    "message": "Webhook secret not configured",
                    "request_id": request_id
                }
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
                    "provided_prefix": provided[:20] + "..." if len(provided) > 20 else provided
                }
            )
            raise HTTPException(
                status_code=401, 
                detail={
                    "error": "invalid_signature_format",
                    "message": "Invalid signature header format",
                    "request_id": request_id
                }
            )
            
        provided_hex = provided.split("=", 1)[1].strip()
        digest = hmac.new(settings.WEBHOOK_SECRET.encode("utf-8"), body, hashlib.sha256).hexdigest()
        
        if not hmac.compare_digest(digest, provided_hex):
            logger.warning(
                "Webhook signature mismatch",
                extra={
                    "request_id": request_id,
                    "expected_signature_prefix": digest[:8] + "...",
                    "provided_signature_prefix": provided_hex[:8] + "..."
                }
            )
            raise HTTPException(
                status_code=401, 
                detail={
                    "error": "signature_mismatch",
                    "message": "Webhook signature verification failed",
                    "request_id": request_id
                }
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
                    "content_type": request.headers.get("content-type", "unknown")
                }
            )
            raise HTTPException(
                status_code=400, 
                detail={
                    "error": "invalid_json_payload",
                    "message": "Failed to parse JSON payload",
                    "request_id": request_id
                }
            )

        # Extract account and statuses
        acct = payload.get("account") or {}
        statuses = payload.get("statuses") or ([payload["status"]] if "status" in payload else [])
        
        if not acct:
            logger.warning(
                "Webhook payload missing account information",
                extra={
                    "request_id": request_id,
                    "payload_keys": list(payload.keys())
                }
            )
            raise HTTPException(
                status_code=400, 
                detail={
                    "error": "missing_account_data",
                    "message": "Missing account information in payload",
                    "request_id": request_id
                }
            )

        account_id = acct.get('id', 'unknown')
        account_acct = acct.get('acct', 'unknown')

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
                        "account_acct": account_acct
                    }
                )
                return {
                    "ok": True, 
                    "enqueued": False, 
                    "reason": "duplicate",
                    "request_id": request_id,
                    "dedupe_key": dedupe_key
                }
                
            # Set dedupe key with 5 minute expiry
            r.setex(f"webhook_dedupe:{dedupe_key}", 300, "1")
            
        except Exception as e:
            logger.warning(
                "Webhook deduplication failed (continuing anyway)",
                extra={
                    "request_id": request_id,
                    "error": str(e),
                    "account_id": account_id
                }
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
                    "status_count": len(statuses)
                }
            )
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "task_enqueue_failed",
                    "message": "Failed to enqueue analysis task",
                    "request_id": request_id
                }
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
                "processing_time_ms": round(processing_time * 1000, 1)
            }
        )
        
        return {
            "ok": True, 
            "enqueued": True,
            "task_id": task.id,
            "account_id": account_id,
            "status_count": len(statuses),
            "processing_time_ms": round(processing_time * 1000, 1),
            "request_id": request_id
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
                "processing_time_ms": round(processing_time * 1000, 1)
            }
        )
        raise HTTPException(
            status_code=500, 
            detail={
                "error": "internal_server_error",
                "message": "Webhook processing failed",
                "request_id": request_id
            }
        )

# Analytics and Dashboard Endpoints
@app.get("/analytics/overview", tags=["analytics"])
def get_analytics_overview():
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
            rule_stats = db.query(
                Analysis.rule_key,
                func.count(Analysis.id).label('count'),
                func.avg(Analysis.score).label('avg_score')
            ).group_by(Analysis.rule_key).all()
            
            # Top domains with most activity
            domain_stats = db.query(
                Account.domain,
                func.count(Analysis.id).label('analysis_count')
            ).join(Analysis, Account.mastodon_account_id == Analysis.mastodon_account_id)\
             .group_by(Account.domain)\
             .order_by(desc('analysis_count'))\
             .limit(10).all()
            
            return {
                "totals": {
                    "accounts": total_accounts,
                    "analyses": total_analyses,
                    "reports": total_reports
                },
                "recent_24h": {
                    "analyses": recent_analyses,
                    "reports": recent_reports
                },
                "rules": [
                    {
                        "rule_key": rule.rule_key,
                        "count": rule.count,
                        "avg_score": float(rule.avg_score) if rule.avg_score else 0
                    }
                    for rule in rule_stats
                ],
                "top_domains": [
                    {
                        "domain": domain.domain,
                        "analysis_count": domain.analysis_count
                    }
                    for domain in domain_stats
                ]
            }
    except Exception as e:
        logger.error(
            "Failed to fetch analytics overview",
            extra={
                "error": str(e),
                "error_type": type(e).__name__
            }
        )
        raise HTTPException(
            status_code=500,
            detail={
                "error": "analytics_fetch_failed",
                "message": "Failed to fetch analytics overview"
            }
        )

@app.get("/analytics/timeline", tags=["analytics"])
def get_analytics_timeline(days: int = 7):
    """Get timeline data for analyses and reports"""
    try:
        if days < 1 or days > 365:
            raise HTTPException(
                status_code=400,
                detail={
                    "error": "invalid_days_parameter",
                    "message": "Days parameter must be between 1 and 365"
                }
            )
            
        with SessionLocal() as db:
            end_date = datetime.utcnow()
            start_date = end_date - timedelta(days=days)
            
            # Daily analysis counts
            daily_analyses = db.query(
                func.date(Analysis.created_at).label('date'),
                func.count(Analysis.id).label('count')
            ).filter(Analysis.created_at >= start_date)\
             .group_by(func.date(Analysis.created_at))\
             .order_by('date').all()
            
            # Daily report counts  
            daily_reports = db.query(
                func.date(Report.created_at).label('date'),
                func.count(Report.id).label('count')
            ).filter(Report.created_at >= start_date)\
             .group_by(func.date(Report.created_at))\
             .order_by('date').all()
            
            return {
                "analyses": [
                    {
                        "date": str(item.date),
                        "count": item.count
                    }
                    for item in daily_analyses
                ],
                "reports": [
                    {
                        "date": str(item.date),
                        "count": item.count
                    }
                    for item in daily_reports
                ]
            }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            "Failed to fetch analytics timeline",
            extra={
                "error": str(e),
                "error_type": type(e).__name__,
                "days": days
            }
        )
        raise HTTPException(
            status_code=500,
            detail={
                "error": "timeline_fetch_failed",
                "message": "Failed to fetch analytics timeline"
            }
        )

@app.get("/analytics/accounts", tags=["analytics"])
def get_account_details(limit: int = 50, offset: int = 0):
    """Get detailed account information with analysis counts"""
    with SessionLocal() as db:
        accounts = db.query(
            Account,
            func.count(Analysis.id).label('analysis_count'),
            func.count(Report.id).label('report_count'),
            func.max(Analysis.created_at).label('last_analysis')
        ).outerjoin(Analysis, Account.mastodon_account_id == Analysis.mastodon_account_id)\
         .outerjoin(Report, Account.mastodon_account_id == Report.mastodon_account_id)\
         .group_by(Account.id)\
         .order_by(desc('analysis_count'))\
         .offset(offset).limit(limit).all()
        
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
                    "last_analysis": acc.last_analysis.isoformat() if acc.last_analysis else None
                }
                for acc in accounts
            ]
        }

@app.get("/analytics/reports", tags=["analytics"])
def get_report_details(limit: int = 50, offset: int = 0):
    """Get detailed report information"""
    with SessionLocal() as db:
        reports = db.query(Report, Account.acct, Account.domain)\
                   .join(Account, Report.mastodon_account_id == Account.mastodon_account_id)\
                   .order_by(desc(Report.created_at))\
                   .offset(offset).limit(limit).all()
        
        return {
            "reports": [
                {
                    "id": report.Report.id,
                    "mastodon_account_id": report.Report.mastodon_account_id,
                    "account": f"{report.acct}@{report.domain}",
                    "status_id": report.Report.status_id,
                    "mastodon_report_id": report.Report.mastodon_report_id,
                    "comment": report.Report.comment,
                    "created_at": report.Report.created_at.isoformat()
                }
                for report in reports
            ]
        }

@app.get("/analytics/analyses/{account_id}", tags=["analytics"])
def get_account_analyses(account_id: str, limit: int = 50, offset: int = 0):
    """Get detailed analysis information for a specific account"""
    with SessionLocal() as db:
        analyses = db.query(Analysis)\
                    .filter(Analysis.mastodon_account_id == account_id)\
                    .order_by(desc(Analysis.created_at))\
                    .offset(offset).limit(limit).all()
        
        return {
            "analyses": [
                {
                    "id": analysis.id,
                    "status_id": analysis.status_id,
                    "rule_key": analysis.rule_key,
                    "score": float(analysis.score),
                    "evidence": analysis.evidence,
                    "created_at": analysis.created_at.isoformat()
                }
                for analysis in analyses
            ]
        }

@app.get("/rules/current", tags=["rules"])
def get_current_rules():
    """Get current rule configuration"""
    return {
        "rules": rules.cfg,
        "report_threshold": rules.cfg.get("report_threshold", 1.0)
    }
