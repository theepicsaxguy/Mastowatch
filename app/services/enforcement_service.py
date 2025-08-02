import logging
import time
from typing import List, Optional
from datetime import datetime, timedelta


from app.db import SessionLocal
from app.models import ScheduledAction, AuditLog
from app.clients.mastodon.client import MastodonClient  # Assuming this is the generated client

logger = logging.getLogger(__name__)


class EnforcementService:
    def __init__(self, mastodon_client: MastodonClient, rate_limit_calls: int = 60, rate_limit_period_seconds: int = 60):
        self.mastodon_client = mastodon_client
        self.rate_limit_calls = rate_limit_calls
        self.rate_limit_period_seconds = rate_limit_period_seconds
        self._api_call_timestamps = []

    def _check_rate_limit(self):
        """Enforces a simple in-memory rate limit for API calls."""
        now = time.time()
        # Remove timestamps older than the rate limit period
        self._api_call_timestamps = [t for t in self._api_call_timestamps if now - t < self.rate_limit_period_seconds]

        if len(self._api_call_timestamps) >= self.rate_limit_calls:
            # Calculate time to wait until the oldest call in the window expires
            time_to_wait = self.rate_limit_period_seconds - (now - self._api_call_timestamps[0])
            logger.warning(f"Rate limit exceeded. Waiting for {time_to_wait:.2f} seconds.")
            time.sleep(time_to_wait)
            # After waiting, clear old timestamps again
            self._api_call_timestamps = [t for t in self._api_call_timestamps if time.time() - t < self.rate_limit_period_seconds]
        
        self._api_call_timestamps.append(time.time())

    from app.clients.mastodon.api.admin import perform_action as api_perform_action

    def perform_account_action(
        self,
        account_id: str,
        action_type: str,
        report_id: Optional[str] = None,
        warning_text: Optional[str] = None,
        preset_id: Optional[str] = None,
        duration: Optional[int] = None,
        comment: Optional[str] = None,
        status_ids: Optional[List[str]] = None,
    ):
        """
        Performs a moderation action on a Mastodon account.
        Logs the action to the audit log and schedules reversal if duration is provided.
        """
        self._check_rate_limit()
        try:
            api_response = api_perform_action.sync_detailed(
                client=self.mastodon_client._api_client,
                id=account_id,
                type=action_type,
                report_id=report_id,
                warning_text=warning_text,
                preset_id=preset_id,
                duration=duration,
                text=comment,
                status_ids=status_ids,
            )

            with SessionLocal() as session:
                # Log the action to the audit_log table
                audit_entry = AuditLog(
                    action_type=action_type,
                    target_account_id=account_id,
                    timestamp=datetime.utcnow(),
                    evidence={"report_id": report_id, "warning_text": warning_text, "preset_id": preset_id, "duration": duration, "comment": comment, "status_ids": status_ids},
                    api_response=api_response.parsed.to_dict() if api_response.parsed else None, # Assuming pydantic model
                )
                session.add(audit_entry)

                # If duration is provided, create a record in scheduled_actions
                if duration:
                    expires_at = datetime.utcnow() + timedelta(seconds=duration)
                    scheduled_action = ScheduledAction(
                        mastodon_account_id=account_id,
                        action_to_reverse=action_type,  # Store the action to reverse
                        expires_at=expires_at,
                    )
                    session.add(scheduled_action)
                session.commit()

            logger.info(f"Performed {action_type} on account {account_id}. Response: {api_response}")

            # After a successful action, resolve the report if report_id is provided
            if report_id:
                self.resolve_report(report_id)

            return api_response

        except Exception as e:
            logger.error(f"Failed to perform {action_type} on account {account_id}: {e}")
            raise

    def unsilence_account(self, account_id: str):
        """
        Reverses a silence action on an account.
        """
        logger.info(f"Unsliencing account {account_id}")
        return self.perform_account_action(account_id, "unsilence")

    def unsuspend_account(self, account_id: str):
        """
        Reverses a suspend action on an account.
        """
        logger.info(f"Unsuspending account {account_id}")
        return self.perform_account_action(account_id, "unsuspend")

    from app.clients.mastodon.api.admin import create_domain_block as api_create_domain_block

    def block_domain(self, domain: str, severity: str, public_comment: Optional[str] = None, private_comment: Optional[str] = None):
        """
        Blocks a domain.
        """
        self._check_rate_limit()
        try:
            api_response = api_create_domain_block.sync_detailed(
                client=self.mastodon_client._api_client,
                domain=domain,
                severity=severity,
                public_comment=public_comment,
                private_comment=private_comment
            )
            with SessionLocal() as session:
                audit_entry = AuditLog(
                    action_type="domain_block",
                    target_account_id=domain, # Using domain as target_account_id for consistency
                    timestamp=datetime.utcnow(),
                    evidence={"severity": severity, "public_comment": public_comment, "private_comment": private_comment},
                    api_response=api_response.parsed.to_dict() if api_response.parsed else None,
                )
                session.add(audit_entry)
                session.commit()
            logger.info(f"Blocked domain {domain} with severity {severity}. Response: {api_response}")
            return api_response
        except Exception as e:
            logger.error(f"Failed to block domain {domain}: {e}")
            raise

    from app.clients.mastodon.api.admin import resolve_report as api_resolve_report

    def resolve_report(self, report_id: str):
        """
        Resolves a Mastodon report.
        """
        self._check_rate_limit()
        try:
            api_response = api_resolve_report.sync_detailed(client=self.mastodon_client._api_client, id=report_id)
            logger.info(f"Resolved report {report_id}. Response: {api_response}")
            return api_response
        except Exception as e:
            logger.error(f"Failed to resolve report {report_id}: {e}")
            raise