from typing import Any, Dict, List
from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import desc, func
from sqlalchemy.orm import Session

from app.auth import require_admin_hybrid
from app.db import SessionLocal
from app.models import Account, Analysis, Report, ScanSession, ContentScan
from app.schemas import User
from app.enhanced_scanning import EnhancedScanningSystem

router = APIRouter()

# Database dependency
def get_db_session():
    """Dependency to get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/analytics/overview", tags=["analytics"])
def get_analytics_overview(_: User = Depends(require_admin_hybrid)):
    """Get overview metrics for the dashboard"""
    try:
        with SessionLocal() as db:
            # Time ranges
            now = datetime.utcnow()
            last_24h = now - timedelta(hours=24)

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
        raise HTTPException(status_code=500, detail=f"Failed to fetch analytics overview: {e}")


@router.get("/analytics/timeline", tags=["analytics"])
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
        raise HTTPException(status_code=500, detail=f"Failed to fetch analytics timeline: {e}")


@router.get("/analytics/accounts", tags=["analytics"])
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


@router.get("/analytics/reports", tags=["analytics"])
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


@router.get("/analytics/analyses/{account_id}", tags=["analytics"])
def get_account_analyses(account_id: str, limit: int = 50, offset: int = 0, _: User = Depends(require_admin_hybrid)):
    """Get detailed analysis information for a specific account including enhanced scan data"""
    with SessionLocal() as db:
        # Get traditional analyses
        analyses = (
            db.query(Analysis)
            .filter(Analysis.mastodon_account_id == account_id)
            .order_by(desc(Analysis.created_at))
            .offset(offset)
            .limit(limit)
            .all()
        )
        
        # Get enhanced content scans
        content_scans = (
            db.query(ContentScan)
            .filter(ContentScan.mastodon_account_id == account_id)
            .order_by(desc(ContentScan.last_scanned_at))
            .limit(limit // 2)  # Get fewer of these to avoid overwhelming
            .all()
        )

        # Convert traditional analyses
        traditional_analyses = [
            {
                "id": analysis.id,
                "status_id": analysis.status_id,
                "rule_key": analysis.rule_key,
                "score": float(analysis.score),
                "evidence": analysis.evidence,
                "created_at": analysis.created_at.isoformat(),
                "scan_type": "traditional"
            }
            for analysis in analyses
        ]
        
        # Convert enhanced content scans
        enhanced_scans = [
            {
                "id": scan.id,
                "status_id": scan.status_id,
                "content_hash": scan.content_hash,
                "scan_type": scan.scan_type,
                "scan_result": scan.scan_result,
                "rules_version": scan.rules_version,
                "last_scanned_at": scan.last_scanned_at.isoformat() if scan.last_scanned_at else None,
                "needs_rescan": scan.needs_rescan,
                "rule_key": "enhanced_scan",
                "score": scan.scan_result.get("total_score", 0.0) if scan.scan_result else 0.0,
                "evidence": scan.scan_result,
                "created_at": scan.last_scanned_at.isoformat() if scan.last_scanned_at else None
            }
            for scan in content_scans
        ]
        
        # Combine and sort by date
        all_analyses = traditional_analyses + enhanced_scans
        all_analyses.sort(key=lambda x: x["created_at"] or "", reverse=True)

        return {
            "analyses": all_analyses[:limit]
        }


@router.get("/analytics/scanning", tags=["analytics"])
def get_scanning_analytics(_: User = Depends(require_admin_hybrid)):
    """Get real-time scanning analytics and job tracking (15-second refresh)
    """
    try:
        enhanced_scanner = EnhancedScanningSystem()
        
        # Get active jobs from Redis/Celery
        import redis
        r = redis.from_url(settings.REDIS_URL, decode_responses=True)
        
        # Get Celery queue length
        queue_length = r.llen("celery") # Assuming default Celery queue name is "celery"

        with SessionLocal() as db:
            # Get active scan sessions
            active_sessions = db.query(ScanSession).filter(ScanSession.status == 'active').all()
            
            # Get recent completed sessions
            recent_sessions = (
                db.query(ScanSession)
                .filter(ScanSession.completed_at.isnot(None))
                .order_by(desc(ScanSession.completed_at))
                .limit(5) # Latest 5 sessions
                .all()
            )

            # Get last federated scan and domain check times
            last_federated_scan_record = db.query(ScanSession.completed_at)
                                    .filter(ScanSession.session_type == 'federated', ScanSession.status == 'completed')
                                    .order_by(desc(ScanSession.completed_at)).first()
            last_domain_check_record = db.query(ScanSession.completed_at)
                                  .filter(ScanSession.session_type == 'domain_check', ScanSession.status == 'completed')
                                  .order_by(desc(ScanSession.completed_at)).first()
            
            # Get content scan statistics
            content_scan_stats = db.query(
                func.count(ContentScan.id).label('total_scans'),
                func.count(ContentScan.id).filter(ContentScan.needs_rescan == True).label('needs_rescan'),
                func.max(ContentScan.last_scanned_at).label('last_scan')
            ).first()
            
            return {
                "active_jobs": [], # Placeholder for actual active Celery jobs if needed
                "scan_sessions": [
                    {
                        "id": session.id,
                        "session_type": session.session_type,
                        "accounts_processed": session.accounts_processed,
                        "total_accounts": session.total_accounts,
                        "started_at": session.started_at.isoformat(),
                        "completed_at": session.completed_at.isoformat() if session.completed_at else None,
                        "status": session.status,
                        "current_cursor": session.current_cursor
                    }
                    for session in active_sessions + recent_sessions
                ],
                "system_status": {
                    "last_federated_scan": last_federated_scan_record[0].isoformat() if last_federated_scan_record else None,
                    "last_domain_check": last_domain_check_record[0].isoformat() if last_domain_check_record else None,
                    "queue_length": queue_length,
                    "system_load": "normal" # Placeholder, can be enhanced with system metrics
                },
                "content_scan_stats": {
                    "total_scans": content_scan_stats.total_scans or 0,
                    "needs_rescan": content_scan_stats.needs_rescan or 0,
                    "last_scan": content_scan_stats.last_scan.isoformat() if content_scan_stats.last_scan else None
                },
                "metadata": {
                    "last_updated": datetime.utcnow().isoformat(),
                    "refresh_interval_seconds": 15,
                    "supports_real_time": True,
                    "data_lag_seconds": 0
                }
            }
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get scanning analytics: {e}")


@router.get("/analytics/domains", tags=["analytics"])
def get_domain_analytics(_: User = Depends(require_admin_hybrid)):
    """Get domain-level analytics with real-time metrics (15-second refresh capability)
    """
    try:
        enhanced_scanner = EnhancedScanningSystem()
        domain_alerts = enhanced_scanner.get_domain_alerts(100)
        
        # Calculate comprehensive summary statistics
        total_domains = len(domain_alerts)
        defederated_count = sum(1 for alert in domain_alerts if alert.get("is_defederated", False))
        high_risk_count = sum(1 for alert in domain_alerts 
                            if alert.get("violation_count", 0) >= alert.get("defederation_threshold", 10) * 0.8
                            and not alert.get("is_defederated", False))
        monitored_count = total_domains - defederated_count
        
        # Get active scanning status
        current_time = datetime.utcnow()
        
        return {
            "summary": {
                "total_domains": total_domains,
                "monitored_domains": monitored_count,
                "high_risk_domains": high_risk_count, 
                "defederated_domains": defederated_count,
                "scan_in_progress": False  # TODO: Get from Redis/Celery
            },
            "domain_alerts": domain_alerts[:20],  # Top 20 for UI
            "metadata": {
                "last_updated": current_time.isoformat(),
                "refresh_interval_seconds": 15,
                "cache_status": "fresh",
                "supports_real_time": True
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch domain analytics: {e}")


@router.get("/analytics/rules/statistics", tags=["analytics"])
def get_rule_statistics(_: User = Depends(require_admin_hybrid)):
    """Get comprehensive rule statistics and performance metrics"""
    try:
        # Assuming rule_service has a method to get rule statistics
        rule_stats = rule_service.get_rule_statistics()
        return rule_stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch rule statistics: {e}")
