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
from app.models import Config
from app.auth import require_api_key
from app.tasks.jobs import analyze_and_maybe_report  # reuse pipeline

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
