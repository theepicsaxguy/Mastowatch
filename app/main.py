import logging
from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from app.logging_conf import setup_logging
from app.config import get_settings
from app.rules import Rules

setup_logging()
app = FastAPI(title="MastoWatch", version="1.0.0")
settings = get_settings()
rules = Rules()

@app.get("/healthz", tags=["ops"])
def healthz():
    return {"ok": True, "dry_run": settings.DRY_RUN, "batch_size": settings.BATCH_SIZE}

@app.get("/metrics", response_class=PlainTextResponse, tags=["ops"])
def metrics():
    return PlainTextResponse(generate_latest(), media_type=CONTENT_TYPE_LATEST)

@app.post("/config/dry_run", tags=["ops"])
def set_dry_run(flag: bool):
    # Persist to DB in a later patch; for scaffold, we allow in-memory toggle
    settings.DRY_RUN = bool(flag)
    return {"dry_run": settings.DRY_RUN}

@app.post("/dryrun/evaluate", tags=["ops"])
async def dryrun_evaluate(payload: dict):
    acct = payload.get("account") or {}
    statuses = payload.get("statuses") or []
    score, hits = rules.eval_account(acct, statuses)
    return {"score": score, "hits": hits}

@app.post("/webhooks/status", tags=["webhooks"])
async def webhook_status(request: Request):
    # TODO: Add HMAC verification before enabling in prod
    body = await request.body()
    logging.info("Webhook received: %d bytes", len(body))
    return {"ok": True}
