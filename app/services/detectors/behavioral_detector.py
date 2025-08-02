from typing import List, Dict, Any
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from app.services.detectors.base import BaseDetector
from app.schemas import Violation, Evidence
from app.db import engine
from app.models import InteractionHistory, AccountBehaviorMetrics


class BehavioralDetector(BaseDetector):
    def evaluate(self, rule: Any, account_data: Dict[str, Any], statuses: List[Dict[str, Any]]) -> List[Violation]:
        violations: List[Violation] = []
        mastodon_account_id = account_data.get("mastodon_account_id")

        if not mastodon_account_id:
            return violations

        with Session(engine) as session:
            # Check for rapid posting behavior
            one_hour_ago = datetime.utcnow() - timedelta(hours=1)
            posts_last_1h = session.query(InteractionHistory).filter(
                InteractionHistory.source_account_id == mastodon_account_id,
                InteractionHistory.created_at >= one_hour_ago
            ).count()

            if posts_last_1h >= rule.trigger_threshold:
                violations.append(
                    Violation(
                        rule_name=rule.name,
                        score=rule.weight,
                        evidence=Evidence(
                            matched_terms=[],
                            matched_status_ids=[],
                            metrics={"posts_last_1h": posts_last_1h}
                        )
                    )
                )
            
            # Check for unusual interaction patterns (e.g., many interactions with different accounts)
            # Limiting to 100 records to prevent performance issues
            recent_interactions = session.query(InteractionHistory).filter(
                InteractionHistory.source_account_id == mastodon_account_id
            ).order_by(InteractionHistory.created_at.desc()).limit(100).all()

            unique_targets = set()
            for interaction in recent_interactions:
                unique_targets.add(interaction.target_account_id)
            
            if len(unique_targets) >= rule.trigger_threshold:
                violations.append(
                    Violation(
                        rule_name=rule.name,
                        score=rule.weight,
                        evidence=Evidence(
                            matched_terms=[],
                            matched_status_ids=[],
                            metrics={"unique_targets": len(unique_targets), "recent_interactions_count": len(recent_interactions)}
                        )
                    )
                )

            # Update or create AccountBehaviorMetrics
            metrics = session.query(AccountBehaviorMetrics).filter(
                AccountBehaviorMetrics.mastodon_account_id == mastodon_account_id
            ).first()

            if not metrics:
                metrics = AccountBehaviorMetrics(
                    mastodon_account_id=mastodon_account_id,
                    posts_last_1h=posts_last_1h,
                    posts_last_24h=0, # This would be calculated over a longer period
                    last_calculated_at=datetime.utcnow()
                )
                session.add(metrics)
            else:
                metrics.posts_last_1h = posts_last_1h
                metrics.last_calculated_at = datetime.utcnow()
            session.commit()

        return violations
