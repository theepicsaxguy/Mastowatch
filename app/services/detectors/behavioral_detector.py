"""Behavioral detector for account behavior analysis."""

from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from app.db import engine
from app.models import AccountBehaviorMetrics, InteractionHistory, Rule
from app.schemas import Evidence, Violation
from app.services.detectors.base import BaseDetector


class BehavioralDetector(BaseDetector):
    """Detector for behavioral patterns in account activity."""

    def evaluate(self, rule: Rule, account_data: dict[str, any], statuses: list[dict[str, any]]) -> list[Violation]:
        """Evaluate account behavior against rule patterns."""
        violations: list[Violation] = []
        mastodon_account_id = account_data.get("mastodon_account_id")

        if not mastodon_account_id:
            return violations

        with Session(engine) as session:
            # Use rule.pattern to determine which behavior to check
            behavior_type = rule.pattern.lower().strip()

            if behavior_type == "rapid_posting":
                # Check for rapid posting behavior
                one_hour_ago = datetime.utcnow() - timedelta(hours=1)
                posts_last_1h = (
                    session.query(InteractionHistory)
                    .filter(
                        InteractionHistory.source_account_id == mastodon_account_id,
                        InteractionHistory.created_at >= one_hour_ago,
                    )
                    .count()
                )

                if posts_last_1h >= rule.trigger_threshold:
                    violations.append(
                        Violation(
                            rule_name=rule.name,
                            score=rule.weight,
                            evidence=Evidence(
                                matched_terms=[],
                                matched_status_ids=[],
                                metrics={"posts_last_1h": posts_last_1h, "threshold": rule.trigger_threshold},
                            ),
                        )
                    )

            elif behavior_type == "interaction_spam":
                # Check for unusual interaction patterns (many interactions with different accounts)
                recent_interactions = (
                    session.query(InteractionHistory)
                    .filter(InteractionHistory.source_account_id == mastodon_account_id)
                    .order_by(InteractionHistory.created_at.desc())
                    .limit(100)
                    .all()
                )

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
                                metrics={
                                    "unique_targets": len(unique_targets),
                                    "recent_interactions_count": len(recent_interactions),
                                    "threshold": rule.trigger_threshold,
                                },
                            ),
                        )
                    )

            elif behavior_type == "daily_posting":
                # Check for excessive daily posting
                twenty_four_hours_ago = datetime.utcnow() - timedelta(hours=24)
                posts_last_24h = (
                    session.query(InteractionHistory)
                    .filter(
                        InteractionHistory.source_account_id == mastodon_account_id,
                        InteractionHistory.created_at >= twenty_four_hours_ago,
                    )
                    .count()
                )

                if posts_last_24h >= rule.trigger_threshold:
                    violations.append(
                        Violation(
                            rule_name=rule.name,
                            score=rule.weight,
                            evidence=Evidence(
                                matched_terms=[],
                                matched_status_ids=[],
                                metrics={"posts_last_24h": posts_last_24h, "threshold": rule.trigger_threshold},
                            ),
                        )
                    )

            # Update or create AccountBehaviorMetrics
            one_hour_ago = datetime.utcnow() - timedelta(hours=1)
            twenty_four_hours_ago = datetime.utcnow() - timedelta(hours=24)

            posts_last_1h = (
                session.query(InteractionHistory)
                .filter(
                    InteractionHistory.source_account_id == mastodon_account_id,
                    InteractionHistory.created_at >= one_hour_ago,
                )
                .count()
            )

            posts_last_24h = (
                session.query(InteractionHistory)
                .filter(
                    InteractionHistory.source_account_id == mastodon_account_id,
                    InteractionHistory.created_at >= twenty_four_hours_ago,
                )
                .count()
            )

            metrics = (
                session.query(AccountBehaviorMetrics)
                .filter(AccountBehaviorMetrics.mastodon_account_id == mastodon_account_id)
                .first()
            )

            if not metrics:
                metrics = AccountBehaviorMetrics(
                    mastodon_account_id=mastodon_account_id,
                    posts_last_1h=posts_last_1h,
                    posts_last_24h=posts_last_24h,
                    last_calculated_at=datetime.utcnow(),
                )
                session.add(metrics)
            else:
                metrics.posts_last_1h = posts_last_1h
                metrics.posts_last_24h = posts_last_24h
                metrics.last_calculated_at = datetime.utcnow()
            session.commit()

        return violations
