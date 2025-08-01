import logging
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import PlainTextResponse
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from app.logging_conf import setup_logging
from app.config import get_settings
from app.rules import Rules
from pydantic import BaseModel
from app.db import SessionLocal
from app.models import Config

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

class DryRunToggle(BaseModel):
    dry_run: bool
    updated_by: str | None = None

@app.post("/config/dry_run", tags=["ops"])
def set_dry_run(body: DryRunToggle):
    with SessionLocal() as db:
        db.merge(Config(key="dry_run", value={"enabled": body.dry_run}, updated_by=body.updated_by))
        db.commit()
    settings.DRY_RUN = bool(body.dry_run)
    return {"dry_run": settings.DRY_RUN, "persisted": True}

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
