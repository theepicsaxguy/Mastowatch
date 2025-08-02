from fastapi import APIRouter, Depends, HTTPException, status
from typing import Dict, Any, List
from datetime import datetime, timedelta

from app.auth import require_api_key, get_api_key
from app.db import SessionLocal
from app.models import Account, Analysis, Report, ContentScan
from app.oauth import User, require_admin_hybrid
from sqlalchemy import desc, func

router = APIRouter()

@router.get("/analytics/overview", tags=["analytics"])
def get_analytics_overview(_: User = Depends(require_admin_hybrid)):
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
        logger.error("Failed to fetch analytics overview", extra={"error": str(e), "error_type": type(e).__name__})
        raise HTTPException(
            status_code=500, detail={"error": "analytics_fetch_failed", "message": "Failed to fetch analytics overview"}
        )


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
        logger.error(
            "Failed to fetch analytics timeline", extra={"error": str(e), "error_type": type(e).__name__, "days": days}
        )
        raise HTTPException(
            status_code=500, detail={"error": "timeline_fetch_failed", "message": "Failed to fetch analytics timeline"}
        )


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