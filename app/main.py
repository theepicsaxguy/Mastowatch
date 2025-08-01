import hmac, hashlib, logging, time
from fastapi import FastAPI, Request, HTTPException, Depends, status
from fastapi.responses import PlainTextResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from app.logging_conf import setup_logging
from app.config import get_settings
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
app = FastAPI(title="MastoWatch", version="1.0.0")
settings = get_settings()
rules = Rules()

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
    # Shallow checks for DB and Redis
    from app.db import SessionLocal
    import redis
    db_ok = False
    redis_ok = False
    try:
        with SessionLocal() as db:
            db.execute("SELECT 1")
            db_ok = True
    except Exception:
        db_ok = False
    try:
        r = redis.from_url(settings.REDIS_URL)
        redis_ok = r.ping()
    except Exception:
        redis_ok = False
    return {
        "ok": db_ok and redis_ok,
        "db_ok": db_ok,
        "redis_ok": redis_ok,
        "dry_run": settings.DRY_RUN,
        "panic_stop": settings.PANIC_STOP,
        "batch_size": settings.BATCH_SIZE,
    }

@app.get("/metrics", response_class=PlainTextResponse, tags=["ops"])
def metrics():
    return PlainTextResponse(generate_latest(), media_type=CONTENT_TYPE_LATEST)

class DryRunToggle(BaseModel):
    dry_run: bool
    updated_by: str | None = None

@app.post("/config/dry_run", tags=["ops"])
def set_dry_run(body: DryRunToggle, _: bool = Depends(require_api_key)):
    if body.dry_run is None:
        raise HTTPException(status_code=400, detail="dry_run flag cannot be null")
    
    # Ensure only 'dry_run' key can be updated via this endpoint
    # The Config model's 'key' is a primary key, so merge handles upsert.
    # We explicitly set the key here to 'dry_run' to prevent arbitrary key updates.
    config_key = "dry_run"

    with SessionLocal() as db:
        db.merge(Config(key=config_key, value={"enabled": body.dry_run}, updated_by=body.updated_by))
        db.commit()
    settings.DRY_RUN = bool(body.dry_run)
    return {"dry_run": settings.DRY_RUN, "persisted": True}

class PanicToggle(BaseModel):
    panic_stop: bool
    updated_by: str | None = None

@app.post("/config/panic_stop", tags=["ops"])
def set_panic_stop(body: PanicToggle, _: bool = Depends(require_api_key)):
    if body.panic_stop is None:
        raise HTTPException(status_code=400, detail="panic_stop flag cannot be null")
    with SessionLocal() as db:
        db.merge(Config(key="panic_stop", value={"enabled": body.panic_stop}, updated_by=body.updated_by))
        db.commit()
    settings.PANIC_STOP = bool(body.panic_stop)
    return {"panic_stop": settings.PANIC_STOP, "persisted": True}

@app.post("/config/rules/reload", tags=["ops"])
def reload_rules(_: bool = Depends(require_api_key)):
    rules.reload()
    return {"reloaded": True, "ruleset_sha256": rules.ruleset_sha256}

@app.post("/dryrun/evaluate", tags=["ops"])
async def dryrun_evaluate(payload: dict):
    acct = payload.get("account") or {}
    statuses = payload.get("statuses") or []
    score, hits = rules.eval_account(acct, statuses)
    return {"score": score, "hits": hits}

@app.post("/webhooks/status", tags=["webhooks"])
async def webhook_status(request: Request):
    body = await request.body()
    if not settings.WEBHOOK_SECRET:
        raise HTTPException(status_code=503, detail="Webhook secret not configured")

    sig_hdr = settings.WEBHOOK_SIG_HEADER
    provided = request.headers.get(sig_hdr, "")
    if not provided.startswith("sha256="):
        raise HTTPException(status_code=401, detail="Invalid signature header")
    provided_hex = provided.split("=", 1)[1].strip()
    digest = hmac.new(settings.WEBHOOK_SECRET.encode("utf-8"), body, hashlib.sha256).hexdigest()
    if not hmac.compare_digest(digest, provided_hex):
        raise HTTPException(status_code=401, detail="Signature mismatch")

    try:
        payload = await request.json()
    except Exception:
        payload = {}

    # Expect payload to include 'account' and 'statuses' or a 'status' object.
    acct = payload.get("account") or {}
    statuses = payload.get("statuses") or ([payload["status"]] if "status" in payload else [])
    if acct:
        analyze_and_maybe_report.delay({"account": acct, "statuses": statuses})
    logging.info("Webhook accepted: %d bytes, enqueued analysis", len(body))
    return {"ok": True, "enqueued": bool(acct)}

# Analytics and Dashboard Endpoints
@app.get("/analytics/overview", tags=["analytics"])
def get_analytics_overview():
    """Get overview metrics for the dashboard"""
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

@app.get("/analytics/timeline", tags=["analytics"])
def get_analytics_timeline(days: int = 7):
    """Get timeline data for analyses and reports"""
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
        "rules": rules.to_dict(),
        "report_threshold": rules.report_threshold
    }
