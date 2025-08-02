import logging
import re
import time
import urllib.parse

import redis
from celery import shared_task
from sqlalchemy import insert, select, text
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.sql import func

from app.config import get_settings
from app.db import SessionLocal
from app.mastodon_client import MastoClient
from app.metrics import (accounts_scanned, analyses_flagged, analysis_latency,
                         cursor_lag_pages, queue_backlog, report_latency,
                         reports_submitted)
from app.models import Account, Analysis, Config, Cursor, Report
from app.rules import Rules
from app.util import make_dedupe_key

settings = get_settings()
rules = Rules.from_yaml("rules.yml")

# Don't create global client instances to avoid HTTPX reuse issues in Celery
# Instead, create fresh instances in each task

CURSOR_NAME = "admin_accounts"
CURSOR_NAME_LOCAL = "admin_accounts_local"


def _get_admin_client():
    """Get a fresh admin client instance."""
    return MastoClient(settings.ADMIN_TOKEN)


def _get_bot_client():
    """Get a fresh bot client instance."""
    return MastoClient(settings.BOT_TOKEN)


def _parse_next_max_id(link_header: str) -> str | None:
    # Look for: <...max_id=XYZ>; rel="next"
    if not link_header:
        return None
    for part in link_header.split(","):
        if 'rel="next"' in part:
            m = re.search(r"<([^>]+)>", part)
            if not m:
                continue
            url = m.group(1)
            qs = urllib.parse.urlparse(url).query
            params = urllib.parse.parse_qs(qs)
            return (params.get("max_id") or [None])[0]
    return None


def _should_pause():
    # Honor PANIC_STOP from DB or env
    if settings.PANIC_STOP:
        return True
    with SessionLocal() as db:
        row = db.execute(text("SELECT value FROM config WHERE key='panic_stop'")).scalar()
        if isinstance(row, dict):
            return bool(row.get("enabled", False))
    return False


def _persist_account(a: dict):
    acct_obj = a.get("account") or {}
    if not acct_obj:
        return
    acct = acct_obj.get("acct") or ""
    domain = acct.split("@")[-1] if "@" in acct else "local"
    with SessionLocal() as db:
        stmt = (
            pg_insert(Account)
            .values(mastodon_account_id=acct_obj.get("id"), acct=acct, domain=domain)
            .on_conflict_do_update(
                index_elements=["mastodon_account_id"], set_=dict(acct=acct, domain=domain, last_checked_at=func.now())
            )
        )
        db.execute(stmt)
        db.commit()


@shared_task(
    name="app.tasks.jobs.poll_admin_accounts",
    autoretry_for=(Exception,),
    retry_backoff=2,
    retry_backoff_max=60,
    retry_jitter=True,
)
def poll_admin_accounts():
    if _should_pause():
        logging.warning("PANIC_STOP enabled; skipping remote account poll")
        return
    # read cursor
    with SessionLocal() as db:
        pos = db.execute(text("SELECT position FROM cursors WHERE name=:n"), {"n": CURSOR_NAME}).scalar()
    pages = 0
    next_max = pos
    while pages < settings.MAX_PAGES_PER_POLL:
        params = {"origin": "remote", "status": "active", "limit": settings.BATCH_SIZE}
        if next_max:
            params["max_id"] = next_max
        admin = _get_admin_client()
        r = admin.get("/api/v1/admin/accounts", params=params)
        accounts = r.json()
        link = r.headers.get("link", "")
        for a in accounts:
            _persist_account(a)
            analyze_and_maybe_report.delay({"account": a.get("account"), "admin_obj": a})
        # after enqueueing the whole page, advance cursor
        new_next = _parse_next_max_id(link)
        with SessionLocal() as db:
            if new_next:
                stmt = pg_insert(Cursor).values(name=CURSOR_NAME, position=new_next)
                stmt = stmt.on_conflict_do_update(index_elements=["name"], set_=dict(position=new_next, updated_at=func.now()))
                db.execute(stmt)
                db.commit()
        # simple approximation of lag = 1 page per available 'next'
        cursor_lag_pages.labels(cursor=CURSOR_NAME).set(1.0 if new_next else 0.0)
        if not new_next:
            break
        next_max = new_next
        pages += 1


@shared_task(
    name="app.tasks.jobs.poll_admin_accounts_local",
    autoretry_for=(Exception,),
    retry_backoff=2,
    retry_backoff_max=60,
    retry_jitter=True,
)
def poll_admin_accounts_local():
    if _should_pause():
        logging.warning("PANIC_STOP enabled; skipping local account poll")
        return
    with SessionLocal() as db:
        pos = db.execute(text("SELECT position FROM cursors WHERE name=:n"), {"n": CURSOR_NAME_LOCAL}).scalar()
    pages = 0
    next_max = pos
    while pages < settings.MAX_PAGES_PER_POLL:
        params = {"origin": "local", "status": "active", "limit": settings.BATCH_SIZE}
        if next_max:
            params["max_id"] = next_max
        admin = _get_admin_client()
        r = admin.get("/api/v1/admin/accounts", params=params)
        accounts = r.json()
        link = r.headers.get("link", "")
        for a in accounts:
            _persist_account(a)
            analyze_and_maybe_report.delay({"account": a.get("account"), "admin_obj": a})
        new_next = _parse_next_max_id(link)
        with SessionLocal() as db:
            if new_next:
                stmt = pg_insert(Cursor).values(name=CURSOR_NAME_LOCAL, position=new_next)
                stmt = stmt.on_conflict_do_update(index_elements=["name"], set_=dict(position=new_next, updated_at=func.now()))
                db.execute(stmt)
                db.commit()
        cursor_lag_pages.labels(cursor=CURSOR_NAME_LOCAL).set(1.0 if new_next else 0.0)
        if not new_next:
            break
        next_max = new_next
        pages += 1


def _get_instance_rules():
    try:
        admin = _get_admin_client()
        r = admin.get("/api/v1/instance/rules")
        # Returns list of {"id": "...", "text": "..."}
        return r.json()
    except Exception:
        return []


@shared_task(name="app.tasks.jobs.record_queue_stats")
def record_queue_stats():
    try:
        q = "celery"
        r = redis.from_url(settings.REDIS_URL, decode_responses=False)
        # Celery default redis backend uses 'celery' list for queue
        backlog = r.llen(q)
        queue_backlog.labels(queue=q).set(float(backlog))
    except Exception as e:
        logging.warning("record_queue_stats: %s", e)


@shared_task(
    name="app.tasks.jobs.analyze_and_maybe_report",
    autoretry_for=(Exception,),
    retry_backoff=2,
    retry_backoff_max=60,
    retry_jitter=True,
)
def analyze_and_maybe_report(payload: dict):
    try:
        if _should_pause():
            logging.warning("PANIC_STOP enabled; skipping analyze/report")
            return
        started = time.time()
        # Allow both raw admin object or normalized dict
        acct = payload.get("account") or payload.get("admin_obj", {}).get("account") or {}
        acct_id = acct.get("id")
        if not acct_id:
            return
        admin = _get_admin_client()
        sr = admin.get(f"/api/v1/accounts/{acct_id}/statuses", params={"limit": settings.MAX_STATUSES_TO_FETCH})
        statuses = sr.json()
        accounts_scanned.inc()
        score, hits = rules.eval_account(acct, statuses)
        analysis_latency.observe(max(0.0, time.time() - started))
        if not hits:
            return

        with SessionLocal() as db:
            for rk, w, ev in hits:
                db.execute(
                    insert(Analysis).values(
                        mastodon_account_id=acct_id, status_id=ev.get("status_id"), rule_key=rk, score=w, evidence=ev
                    )
                )
                analyses_flagged.labels(rule=rk).inc()
            db.commit()

        if float(score) < float(rules.cfg.get("report_threshold", 1.0)):
            return

        status_ids = [h[2].get("status_id") for h in hits if h[2].get("status_id")]
        comment = f"[AUTO] score={score:.2f}; hits=" + ", ".join(h[0] for h in hits)
        dedupe = make_dedupe_key(acct_id, status_ids, settings.POLICY_VERSION, rules.ruleset_sha256, {"hit_count": len(hits)})

        # Try UPSERT via RETURNING: if row already exists, result is None
        # UPSERT report row to enforce idempotency before hitting the API

        stmt = (
            pg_insert(Report)
            .values(
                mastodon_account_id=acct_id,
                status_id=status_ids[0] if status_ids else None,
                mastodon_report_id=None,
                dedupe_key=dedupe,
                comment=comment,
            )
            .on_conflict_do_nothing(index_elements=["dedupe_key"])
            .returning(Report.id)
        )
        with SessionLocal() as db:
            inserted_id = db.execute(stmt).scalar_one_or_none()
            db.commit()
            if inserted_id is None:
                return  # duplicate

        if settings.DRY_RUN:
            logging.info("DRY-RUN report acct=%s score=%.2f hits=%d", acct.get("acct"), score, len(hits))
            return

        payload = {"account_id": acct_id, "comment": comment}
        for sid in status_ids or []:
            payload.setdefault("status_ids[]", []).append(sid)
        # Reporting category/forward per Mastodon API
        payload["category"] = settings.REPORT_CATEGORY_DEFAULT
        acct_acct = acct.get("acct", "")
        is_remote = "@" in acct_acct
        if is_remote:
            payload["forward"] = settings.FORWARD_REMOTE_REPORTS
        # Optional: map rule names -> instance rule IDs if configured server rules are available
        rule_entities = _get_instance_rules()
        if rule_entities and payload["category"] == "violation":
            # naive example: include all rule ids when category is violation
            payload["rule_ids[]"] = [r.get("id") for r in rule_entities if r.get("id")]

        bot = _get_bot_client()
        rr = bot.post("/api/v1/reports", data=payload)
        rep_id = rr.json().get("id", "")

        with SessionLocal() as db:
            from sqlalchemy import text

            db.execute(
                text("UPDATE reports SET mastodon_report_id = :rid WHERE dedupe_key = :dk"), {"rid": rep_id, "dk": dedupe}
            )
            db.commit()

        domain = acct.get("acct", "").split("@")[-1] if "@" in acct.get("acct", "") else "local"
        reports_submitted.labels(domain=domain).inc()
        report_latency.observe(max(0.0, time.time() - started))
    except Exception as e:
        logging.exception("analyze_and_maybe_report error: %s", e)
        raise
