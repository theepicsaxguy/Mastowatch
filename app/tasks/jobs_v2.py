"""
Updated jobs.py demonstrating how to use the new type-safe Mastodon client.

This shows how to migrate specific parts of your existing code while maintaining
full backward compatibility.
"""

import logging
import re
import time
import urllib.parse

from celery import shared_task
from sqlalchemy import insert, select, text
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.sql import func

from app.config import get_settings
from app.db import SessionLocal
from app.mastodon_client_v2 import MastoClientV2  # New typed client
from app.metrics import (accounts_scanned, analyses_flagged, analysis_latency,
                         cursor_lag_pages, queue_backlog, report_latency,
                         reports_submitted)
from app.models import Account, Analysis, Config, Cursor, Report
from app.rules import Rules
from app.util import make_dedupe_key

settings = get_settings()
rules = Rules.from_yaml("rules.yml")

# Initialize both admin and bot clients with the new type-safe client
admin = MastoClientV2(settings.ADMIN_TOKEN)
bot = MastoClientV2(settings.BOT_TOKEN)

# ... (keep existing helper functions unchanged)


def _parse_next_max_id(link_header: str) -> str | None:
    """Parse next max_id from Link header - unchanged."""
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
    """Check if processing should be paused - unchanged."""
    if settings.PANIC_STOP:
        return True
    with SessionLocal() as db:
        row = db.execute(text("SELECT value FROM config WHERE key='panic_stop'")).scalar()
        if isinstance(row, dict):
            return bool(row.get("enabled", False))
    return False


def _persist_account(a: dict):
    """Persist account information - unchanged."""
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
    name="app.tasks.jobs_v2.poll_admin_accounts",
    autoretry_for=(Exception,),
    retry_backoff=2,
    retry_backoff_max=60,
    retry_jitter=True,
)
def poll_admin_accounts():
    """
    Updated version using type-safe client where possible.
    Falls back to raw HTTP for admin endpoints not in OpenAPI spec.
    """
    if _should_pause():
        logging.warning("PANIC_STOP enabled; skipping remote account poll")
        return

    # Read cursor position
    with SessionLocal() as db:
        pos = db.execute(text("SELECT position FROM cursors WHERE name=:n"), {"n": "admin_accounts"}).scalar()

    pages = 0
    next_max = pos

    while pages < settings.MAX_PAGES_PER_POLL:
        # Admin endpoints still use raw HTTP until they're added to OpenAPI spec
        response = admin.get_admin_accounts(origin="remote", status="active", limit=settings.BATCH_SIZE, max_id=next_max)

        accounts = response.json()
        link = response.headers.get("link", "")

        for a in accounts:
            _persist_account(a)
            analyze_and_maybe_report_v2.delay({"account": a.get("account"), "admin_obj": a})

        # Advance cursor
        new_next = _parse_next_max_id(link)
        with SessionLocal() as db:
            if new_next:
                stmt = pg_insert(Cursor).values(name="admin_accounts", position=new_next)
                stmt = stmt.on_conflict_do_update(index_elements=["name"], set_=dict(position=new_next, updated_at=func.now()))
                db.execute(stmt)
                db.commit()

        cursor_lag_pages.labels(cursor="admin_accounts").set(1.0 if new_next else 0.0)
        if not new_next:
            break
        next_max = new_next
        pages += 1


def _get_instance_rules_v2():
    """Updated to use type-safe client method."""
    try:
        return admin.get_instance_rules()
    except Exception:
        return []


@shared_task(
    name="app.tasks.jobs_v2.analyze_and_maybe_report_v2",
    autoretry_for=(Exception,),
    retry_backoff=2,
    retry_backoff_max=60,
    retry_jitter=True,
)
def analyze_and_maybe_report_v2(payload: dict):
    """
    Updated version demonstrating type-safe API calls.
    Shows the benefits of using typed responses.
    """
    try:
        if _should_pause():
            logging.warning("PANIC_STOP enabled; skipping analyze/report")
            return

        started = time.time()

        # Extract account info - unchanged
        acct = payload.get("account") or payload.get("admin_obj", {}).get("account") or {}
        acct_id = acct.get("id")
        if not acct_id:
            return

        # TYPE-SAFE APPROACH: Get statuses using typed client
        try:
            # This returns List[Status] with full type information!
            statuses_typed = admin.get_account_statuses(account_id=acct_id, limit=settings.MAX_STATUSES_TO_FETCH)
            # Convert to dict format for compatibility with existing rules engine
            statuses = [status.__dict__ for status in statuses_typed]

        except Exception as e:
            # Fallback to raw HTTP if needed
            logging.warning(f"Falling back to raw HTTP for statuses: {e}")
            sr = admin.get(f"/api/v1/accounts/{acct_id}/statuses", params={"limit": settings.MAX_STATUSES_TO_FETCH})
            statuses = sr.json()

        accounts_scanned.inc()
        score, hits = rules.eval_account(acct, statuses)
        analysis_latency.observe(max(0.0, time.time() - started))

        if not hits:
            return

        # Store analysis results - unchanged
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

        # Prepare report data
        status_ids = [h[2].get("status_id") for h in hits if h[2].get("status_id")]
        comment = f"[AUTO] score={score:.2f}; hits=" + ", ".join(h[0] for h in hits)
        dedupe = make_dedupe_key(acct_id, status_ids, settings.POLICY_VERSION, rules.ruleset_sha256, {"hit_count": len(hits)})

        # Check for duplicate reports - unchanged
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

        # TYPE-SAFE APPROACH: Create report using typed client
        try:
            acct_acct = acct.get("acct", "")
            is_remote = "@" in acct_acct
            rule_entities = _get_instance_rules_v2()

            # Get rule IDs if this is a violation report
            rule_ids = None
            category = settings.REPORT_CATEGORY_DEFAULT
            if category == "violation" and rule_entities:
                rule_ids = [r.get("id") for r in rule_entities if r.get("id")]

            # Use type-safe report creation
            report = bot.create_report(
                account_id=acct_id,
                comment=comment,
                status_ids=status_ids,
                category=category,
                forward=is_remote and settings.FORWARD_REMOTE_REPORTS,
                rule_ids=rule_ids,
            )

            # report.id is now type-safe!
            rep_id = report.id

        except Exception as e:
            # Fallback to raw HTTP if needed
            logging.warning(f"Falling back to raw HTTP for report creation: {e}")
            payload_data = {"account_id": acct_id, "comment": comment}
            for sid in status_ids or []:
                payload_data.setdefault("status_ids[]", []).append(sid)
            payload_data["category"] = settings.REPORT_CATEGORY_DEFAULT

            if is_remote:
                payload_data["forward"] = settings.FORWARD_REMOTE_REPORTS
            if rule_entities and payload_data["category"] == "violation":
                payload_data["rule_ids[]"] = [r.get("id") for r in rule_entities if r.get("id")]

            rr = bot.post("/api/v1/reports", data=payload_data)
            rep_id = rr.json().get("id", "")

        # Update report with Mastodon ID
        with SessionLocal() as db:
            db.execute(
                text("UPDATE reports SET mastodon_report_id = :rid WHERE dedupe_key = :dk"), {"rid": rep_id, "dk": dedupe}
            )
            db.commit()

        domain = acct.get("acct", "").split("@")[-1] if "@" in acct.get("acct", "") else "local"
        reports_submitted.labels(domain=domain).inc()
        report_latency.observe(max(0.0, time.time() - started))

    except Exception as e:
        logging.exception("analyze_and_maybe_report_v2 error: %s", e)
        raise


# Keep existing tasks for backward compatibility
@shared_task(name="app.tasks.jobs_v2.record_queue_stats")
def record_queue_stats():
    """Queue statistics monitoring - unchanged."""
    try:
        import redis

        q = "celery"
        r = redis.from_url(settings.REDIS_URL, decode_responses=False)
        backlog = r.llen(q)
        queue_backlog.labels(queue=q).set(float(backlog))
    except Exception as e:
        logging.warning("record_queue_stats: %s", e)


# Example of completely type-safe new functionality
@shared_task(name="app.tasks.jobs_v2.analyze_specific_account")
def analyze_specific_account(account_id: str):
    """
    Example of a new task that's fully type-safe from the start.
    Demonstrates the benefits of using typed responses throughout.
    """
    try:
        # Get account with full type safety
        account = admin.get_account(account_id)

        # account.username, account.followers_count etc. are all typed!
        logging.info(f"Analyzing @{account.username} (followers: {account.followers_count})")

        # Get statuses with type safety
        statuses = admin.get_account_statuses(account_id, limit=50)

        # statuses is List[Status] - each status has typed fields
        for status in statuses:
            logging.info(
                f"Status {status.id}: {len(status.content)} chars, "
                f"{status.reblogs_count} reblogs, {status.favourites_count} favs"
            )

        # Use the data as needed...

    except Exception as e:
        logging.exception(f"Error analyzing account {account_id}: {e}")
        raise
