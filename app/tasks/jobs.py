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
from app.clients.mastodon.client import Client
from app.metrics import (accounts_scanned, analyses_flagged, analysis_latency,
                         cursor_lag_pages, queue_backlog, report_latency,
                         reports_submitted)
from app.models import Account, Analysis, Config, Cursor, Report
from app.services.rule_service import rule_service
from app.enhanced_scanning import EnhancedScanningSystem
from app.util import make_dedupe_key
import os

settings = get_settings()

# Don't create global client instances to avoid HTTPX reuse issues in Celery
# Instead, create fresh instances in each task

CURSOR_NAME = "admin_accounts"
CURSOR_NAME_LOCAL = "admin_accounts_local"


def _get_admin_client():
    """Get a fresh admin client instance."""
    return Client(base_url=str(settings.INSTANCE_BASE), token=settings.ADMIN_TOKEN)


def _get_bot_client():
    """Get a fresh bot client instance."""
    return Client(base_url=str(settings.INSTANCE_BASE), token=settings.BOT_TOKEN)





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
    """Enhanced polling of remote admin accounts with efficient scanning"""
    if _should_pause():
        logging.warning("PANIC_STOP enabled; skipping remote account poll")
        return
    
    enhanced_scanner = EnhancedScanningSystem()
    session_id = enhanced_scanner.start_scan_session("remote")
    
    try:
        # Read cursor
        with SessionLocal() as db:
            pos = db.execute(text("SELECT position FROM cursors WHERE name=:n"), {"n": CURSOR_NAME}).scalar()
        
        pages = 0
        next_max = pos
        accounts_processed = 0
        
        while pages < settings.MAX_PAGES_PER_POLL:
            # Get next batch of accounts
            accounts, new_next = enhanced_scanner.get_next_accounts_to_scan(
                "remote", 
                limit=settings.BATCH_SIZE, 
                cursor=next_max
            )
            
            if not accounts:
                break
            
            for account_data in accounts:
                try:
                    # Persist account information
                    _persist_account(account_data)
                    
                    # Use enhanced scanning with deduplication
                    scan_result = enhanced_scanner.scan_account_efficiently(
                        account_data.get("account", {}), 
                        session_id
                    )
                    
                    if scan_result:
                        accounts_processed += 1
                        # Enqueue for analysis if needed
                        if scan_result.get("score", 0) > 0:
                            analyze_and_maybe_report.delay({
                                "account": account_data.get("account"), 
                                "admin_obj": account_data,
                                "scan_result": scan_result
                            })
                
                except Exception as e:
                    logging.error(f"Error processing account: {e}")
            
            # Update cursor after processing the page
            with SessionLocal() as db:
                if new_next:
                    stmt = pg_insert(Cursor).values(name=CURSOR_NAME, position=new_next)
                    stmt = stmt.on_conflict_do_update(
                        index_elements=["name"], 
                        set_=dict(position=new_next, updated_at=func.now())
                    )
                    db.execute(stmt)
                    db.commit()
            
            # Update cursor lag metric
            cursor_lag_pages.labels(cursor=CURSOR_NAME).set(1.0 if new_next else 0.0)
            
            if not new_next:
                break
            
            next_max = new_next
            pages += 1
        
        enhanced_scanner.complete_scan_session(session_id)
        logging.info(f"Remote account poll completed: {accounts_processed} accounts processed, {pages} pages")
        
    except Exception as e:
        logging.error(f"Error in remote account poll: {e}")
        enhanced_scanner.complete_scan_session(session_id, 'failed')


@shared_task(
    name="app.tasks.jobs.poll_admin_accounts_local",
    autoretry_for=(Exception,),
    retry_backoff=2,
    retry_backoff_max=60,
    retry_jitter=True,
)
def poll_admin_accounts_local():
    """Enhanced polling of local admin accounts with efficient scanning"""
    if _should_pause():
        logging.warning("PANIC_STOP enabled; skipping local account poll")
        return
    
    enhanced_scanner = EnhancedScanningSystem()
    session_id = enhanced_scanner.start_scan_session("local")
    
    try:
        # Read cursor
        with SessionLocal() as db:
            pos = db.execute(text("SELECT position FROM cursors WHERE name=:n"), {"n": CURSOR_NAME_LOCAL}).scalar()
        
        pages = 0
        next_max = pos
        accounts_processed = 0
        
        while pages < settings.MAX_PAGES_PER_POLL:
            # Get next batch of accounts
            accounts, new_next = enhanced_scanner.get_next_accounts_to_scan(
                "local", 
                limit=settings.BATCH_SIZE, 
                cursor=next_max
            )
            
            if not accounts:
                break
            
            for account_data in accounts:
                try:
                    # Persist account information
                    _persist_account(account_data)
                    
                    # Use enhanced scanning with deduplication
                    scan_result = enhanced_scanner.scan_account_efficiently(
                        account_data.get("account", {}), 
                        session_id
                    )
                    
                    if scan_result:
                        accounts_processed += 1
                        # Enqueue for analysis if needed
                        if scan_result.get("score", 0) > 0:
                            analyze_and_maybe_report.delay({
                                "account": account_data.get("account"), 
                                "admin_obj": account_data,
                                "scan_result": scan_result
                            })
                
                except Exception as e:
                    logging.error(f"Error processing account: {e}")
            
            # Update cursor after processing the page
            with SessionLocal() as db:
                if new_next:
                    stmt = pg_insert(Cursor).values(name=CURSOR_NAME_LOCAL, position=new_next)
                    stmt = stmt.on_conflict_do_update(
                        index_elements=["name"], 
                        set_=dict(position=new_next, updated_at=func.now())
                    )
                    db.execute(stmt)
                    db.commit()
            
            # Update cursor lag metric
            cursor_lag_pages.labels(cursor=CURSOR_NAME_LOCAL).set(1.0 if new_next else 0.0)
            
            if not new_next:
                break
            
            next_max = new_next
            pages += 1
        
        enhanced_scanner.complete_scan_session(session_id)
        logging.info(f"Local account poll completed: {accounts_processed} accounts processed, {pages} pages")
        
    except Exception as e:
        logging.error(f"Error in local account poll: {e}")
        enhanced_scanner.complete_scan_session(session_id, 'failed')


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
    name="app.tasks.jobs.scan_federated_content",
    autoretry_for=(Exception,),
    retry_backoff=5,
    retry_backoff_max=300,
    retry_jitter=True,
)
def scan_federated_content(target_domains=None):
    """Scan content across federated domains for violations"""
    if _should_pause():
        logging.warning("PANIC_STOP enabled; skipping federated content scan")
        return
    
    enhanced_scanner = EnhancedScanningSystem()
    
    try:
        results = enhanced_scanner.scan_federated_content(target_domains)
        logging.info(f"Federated scan completed: {results}")
        return results
    except Exception as e:
        logging.error(f"Error in federated content scan: {e}")
        raise


@shared_task(
    name="app.tasks.jobs.check_domain_violations",
    autoretry_for=(Exception,),
    retry_backoff=2,
    retry_backoff_max=60,
    retry_jitter=True,
)
def check_domain_violations():
    """Check and update domain violation tracking"""
    if _should_pause():
        logging.warning("PANIC_STOP enabled; skipping domain violation check")
        return
    
    enhanced_scanner = EnhancedScanningSystem()
    
    try:
        domain_alerts = enhanced_scanner.get_domain_alerts(100)
        defederated_count = sum(1 for alert in domain_alerts if alert["is_defederated"])
        
        logging.info(f"Domain violation check completed: {len(domain_alerts)} domains tracked, {defederated_count} defederated")
        return {
            "domains_tracked": len(domain_alerts),
            "defederated_domains": defederated_count,
            "high_risk_domains": sum(1 for alert in domain_alerts 
                                   if alert["violation_count"] >= alert["defederation_threshold"] * 0.8)
        }
    except Exception as e:
        logging.error(f"Error checking domain violations: {e}")
        raise


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
        
        # Check if we already have a cached scan result
        cached_result = payload.get("scan_result")
        if cached_result:
            # Use cached scan result
            score = cached_result.get("score", 0)
            hits = [(hit["rule"], hit["weight"], hit["evidence"]) for hit in cached_result.get("rule_hits", [])]
        else:
            # Perform fresh analysis
            current_rules = rule_service.get_current_rules_snapshot()
            admin = _get_admin_client()
            statuses = admin.get_account_statuses(
                account_id=acct_id,
                limit=settings.MAX_STATUSES_TO_FETCH
            )
            score, hits = current_rules.eval_account(acct, statuses)
        
        accounts_scanned.inc()
        analysis_latency.observe(max(0.0, time.time() - started))
        
        if not hits:
            return

        # Store analysis results
        with SessionLocal() as db:
            for rk, w, ev in hits:
                db.execute(
                    insert(Analysis).values(
                        mastodon_account_id=acct_id, 
                        status_id=ev.get("status_id"), 
                        rule_key=rk, 
                        score=w, 
                        evidence=ev
                    )
                )
                analyses_flagged.labels(rule=rk).inc()
            db.commit()

        # Check if score meets reporting threshold
        current_rules = rule_service.get_current_rules_snapshot()
        if float(score) < float(current_rules.cfg.get("report_threshold", 1.0)):
            return

        # Track domain violation
        domain = acct.get("acct", "").split("@")[-1] if "@" in acct.get("acct", "") else "local"
        if domain != "local":
            enhanced_scanner = EnhancedScanningSystem()
            enhanced_scanner._track_domain_violation(domain)

        # Prepare report
        status_ids = [h[2].get("status_id") for h in hits if h[2].get("status_id")]
        comment = f"[AUTO] score={score:.2f}; hits=" + ", ".join(h[0] for h in hits)
        dedupe = make_dedupe_key(acct_id, status_ids, settings.POLICY_VERSION, current_rules.ruleset_sha256, {"hit_count": len(hits)})

        # UPSERT report row to enforce idempotency
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

        # Submit report to Mastodon
        payload_data = {"account_id": acct_id, "comment": comment}
        for sid in status_ids or []:
            payload_data.setdefault("status_ids[]", []).append(sid)
        
        # Reporting category/forward per Mastodon API
        payload_data["category"] = settings.REPORT_CATEGORY_DEFAULT
        is_remote = "@" in acct.get("acct", "")
        if is_remote:
            payload_data["forward"] = settings.FORWARD_REMOTE_REPORTS
        
        # Optional: map rule names -> instance rule IDs if configured server rules are available
        # The generated client handles rule_ids directly in CreateReportBody
        # No need for _get_instance_rules() here, as the client will handle it if the API supports it.

        bot = _get_bot_client()
        # Use the generated client's create_report method
        from app.clients.mastodon.models.create_report_body import CreateReportBody
        report_body = CreateReportBody(
            account_id=acct_id,
            comment=comment,
            status_ids=status_ids,
            category=payload_data["category"],
            forward=payload_data["forward"] if "forward" in payload_data else False,
            # rule_ids are handled by the generated client if the API supports it
        )
        rr = bot.create_report(report_body=report_body)
        rep_id = rr.json().get("id", "")

        # Update report with Mastodon report ID
        with SessionLocal() as db:
            from sqlalchemy import text
            db.execute(
                text("UPDATE reports SET mastodon_report_id = :rid WHERE dedupe_key = :dk"), 
                {"rid": rep_id, "dk": dedupe}
            )
            db.commit()

        reports_submitted.labels(domain=domain).inc()
        report_latency.observe(max(0.0, time.time() - started))
        
    except Exception as e:
        logging.exception("analyze_and_maybe_report error: %s", e)
        raise
