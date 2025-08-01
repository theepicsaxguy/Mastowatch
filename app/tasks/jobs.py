from celery import shared_task
from sqlalchemy import insert, select
from app.config import get_settings
from app.db import SessionLocal
from app.models import Analysis, Report
from app.mastodon_client import MastoClient
from app.rules import Rules
from app.util import make_dedupe_key
from app.metrics import analyses_flagged, reports_submitted
import logging, re, urllib.parse
from sqlalchemy.dialects.postgresql import insert as pg_insert
from app.models import Config, Cursor
from app.db import SessionLocal
from sqlalchemy import text

settings = get_settings()
rules = Rules()
admin = MastoClient(settings.ADMIN_TOKEN)
bot = MastoClient(settings.BOT_TOKEN)

CURSOR_NAME = "admin_accounts"

def _parse_next_max_id(link_header: str) -> str | None:
    # Look for: <...max_id=XYZ>; rel="next"
    if not link_header:
        return None
    for part in link_header.split(","):
        if 'rel="next"' in part:
            m = re.search(r'<([^>]+)>', part)
            if not m: 
                continue
            url = m.group(1)
            qs = urllib.parse.urlparse(url).query
            params = urllib.parse.parse_qs(qs)
            return (params.get("max_id") or [None])[0]
    return None

@shared_task(name="app.tasks.jobs.poll_admin_accounts",
             autoretry_for=(Exception,), retry_backoff=2, retry_backoff_max=60, retry_jitter=True)
def poll_admin_accounts():
    # read cursor
    with SessionLocal() as db:
        pos = db.execute(text("SELECT position FROM cursors WHERE name=:n"), {"n": CURSOR_NAME}).scalar()
    pages = 0
    next_max = pos
    while pages < settings.MAX_PAGES_PER_POLL:  # hard cap per beat tick
        params = {"origin":"remote", "status":"active", "limit": settings.BATCH_SIZE}
        if next_max:
            params["max_id"] = next_max
        r = admin.get("/api/v1/admin/accounts", params=params)
        accounts = r.json()
        link = r.headers.get("link","")
        for a in accounts:
            analyze_and_maybe_report.delay(a)
        # after enqueueing the whole page, advance cursor
        new_next = _parse_next_max_id(link)
        with SessionLocal() as db:
            if new_next:
                stmt = pg_insert(Cursor).values(name=CURSOR_NAME, position=new_next)
                stmt = stmt.on_conflict_do_update(index_elements=['name'], set_=dict(position=new_next, updated_at=func.now()))
                db.execute(stmt)
                db.commit()
        if not new_next:
            break
        next_max = new_next
        pages += 1


@shared_task(name="app.tasks.jobs.analyze_and_maybe_report",
             autoretry_for=(Exception,), retry_backoff=2, retry_backoff_max=60, retry_jitter=True)
def analyze_and_maybe_report(admin_account_obj: dict):
    try:
        acct = admin_account_obj.get("account") or {}
        acct_id = acct.get("id")
        if not acct_id:
            return
        sr = admin.get(f"/api/v1/accounts/{acct_id}/statuses", params={"limit": 5})
        statuses = sr.json()
        score, hits = rules.eval_account(acct, statuses)
        if not hits:
            return

        with SessionLocal() as db:
            for rk, w, ev in hits:
                db.execute(insert(Analysis).values(
                    mastodon_account_id=acct_id,
                    status_id=ev.get("status_id"),
                    rule_key=rk,
                    score=w,
                    evidence=ev
                ))
                analyses_flagged.labels(rule=rk).inc()
            db.commit()

        if float(score) < float(rules.cfg.get("report_threshold", 1.0)):
            return

        status_ids = [h[2].get("status_id") for h in hits if h[2].get("status_id")]
        comment = f"[AUTO] score={score:.2f}; hits=" + ", ".join(h[0] for h in hits)
        dedupe = make_dedupe_key(acct_id, status_ids, "v1", rules.ruleset_sha256, {"hit_count": len(hits)})

        # Try UPSERT via RETURNING: if row already exists, result is None
        # UPSERT report row to enforce idempotency before hitting the API

        stmt = pg_insert(Report).values(
                mastodon_account_id=acct_id,
                status_id=status_ids[0] if status_ids else None,
                mastodon_report_id=None,
                dedupe_key=dedupe,
                comment=comment
        ).on_conflict_do_nothing(index_elements=['dedupe_key']).returning(Report.id)
        with SessionLocal() as db:
            inserted_id = db.execute(stmt).scalar_one_or_none()
            db.commit()
            if inserted_id is None:
                return  # duplicate

        if settings.DRY_RUN:
            logging.info("DRY-RUN report acct=%s score=%.2f hits=%d", acct.get("acct"), score, len(hits))
            return

        payload = {"account_id": acct_id, "comment": comment}
        for sid in (status_ids or []):
            payload.setdefault("status_ids[]", []).append(sid)

        rr = bot.post("/api/v1/reports", data=payload)
        rep_id = rr.json().get("id", "")

        with SessionLocal() as db:
            db.execute(
                "UPDATE reports SET mastodon_report_id = :rid WHERE dedupe_key = :dk",
                {"rid": rep_id, "dk": dedupe}
            )
            db.commit()

        domain = (acct.get("acct","").split("@")[-1] if "@" in acct.get("acct","") else "local")
        reports_submitted.labels(domain=domain).inc()
    except Exception as e:
        logging.exception("analyze_and_maybe_report error: %s", e)
        raise
