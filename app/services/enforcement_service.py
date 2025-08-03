import logging
import time
from typing import List, Optional
from datetime import datetime, timedelta

from app.db import SessionLocal
from app.models import ScheduledAction, AuditLog
from app.mastodon_client import MastoClient as MastodonClient

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
            # For now, make a direct HTTP call since the generated API imports are not working
            import httpx
            
            # Prepare the request data
            data = {
                "type": action_type,
            }
            if report_id:
                data["report_id"] = report_id
            if warning_text:
                data["warning_text"] = warning_text
            if preset_id:
                data["preset_id"] = preset_id
            if duration:
                data["duration"] = duration
            if comment:
                data["text"] = comment
            if status_ids:
                data["status_ids"] = status_ids

            # Make HTTP request to admin API
            headers = {
                "Authorization": f"Bearer {self.mastodon_client._token}",
                "Content-Type": "application/json"
            }
            
            url = f"{self.mastodon_client._base_url}/api/v1/admin/accounts/{account_id}/action"
            
            with httpx.Client() as client:
                response = client.post(url, json=data, headers=headers, timeout=30.0)
                response.raise_for_status()
                api_response_data = response.json()

            with SessionLocal() as session:
                # Log the action to the audit_log table
                audit_entry = AuditLog(
                    action_type=action_type,
                    target_account_id=account_id,
                    timestamp=datetime.utcnow(),
                    evidence={"report_id": report_id, "warning_text": warning_text, "preset_id": preset_id, "duration": duration, "comment": comment, "status_ids": status_ids},
                    api_response=api_response_data,
                )
                session.add(audit_entry)

                # If duration is provided, create a record in scheduled_actions
                if duration:
                    expires_at = datetime.utcnow() + timedelta(seconds=duration)
                    scheduled_action = ScheduledAction(
                        mastodon_account_id=account_id,
                        action_to_reverse=action_type,
                        expires_at=expires_at,
                    )
                    session.add(scheduled_action)
                session.commit()

            logger.info(f"Performed {action_type} on account {account_id}. Response: {response.status_code}")

            # After a successful action, resolve the report if report_id is provided
            if report_id:
                self.resolve_report(report_id)

            return api_response_data

        except Exception as e:
            logger.error(f"Failed to perform {action_type} on account {account_id}: {e}")
            raise

    def unsilence_account(self, account_id: str):
        """
        Reverses a silence action on an account by setting action_type to 'none'.
        """
        logger.info(f"Unsilencing account {account_id}")
        return self.perform_account_action(account_id, "none")

    def unsuspend_account(self, account_id: str):
        """
        Reverses a suspend action on an account by setting action_type to 'none'.
        """
        logger.info(f"Unsuspending account {account_id}")
        return self.perform_account_action(account_id, "none")

    def block_domain(self, domain: str, severity: str, public_comment: Optional[str] = None, private_comment: Optional[str] = None):
        """
        Blocks a domain.
        """
        self._check_rate_limit()
        try:
            import httpx
            
            data = {
                "domain": domain,
                "severity": severity,
            }
            if public_comment:
                data["public_comment"] = public_comment
            if private_comment:
                data["private_comment"] = private_comment

            headers = {
                "Authorization": f"Bearer {self.mastodon_client._token}",
                "Content-Type": "application/json"
            }
            
            url = f"{self.mastodon_client._base_url}/api/v1/admin/domain_blocks"
            
            with httpx.Client() as client:
                response = client.post(url, json=data, headers=headers, timeout=30.0)
                response.raise_for_status()
                api_response_data = response.json()

            with SessionLocal() as session:
                audit_entry = AuditLog(
                    action_type="domain_block",
                    target_account_id=domain,  # Using domain as target_account_id for consistency
                    timestamp=datetime.utcnow(),
                    evidence={"severity": severity, "public_comment": public_comment, "private_comment": private_comment},
                    api_response=api_response_data,
                )
                session.add(audit_entry)
                session.commit()
            logger.info(f"Blocked domain {domain} with severity {severity}. Response: {response.status_code}")
            return api_response_data
        except Exception as e:
            logger.error(f"Failed to block domain {domain}: {e}")
            raise

    def resolve_report(self, report_id: str):
        """
        Resolves a Mastodon report.
        """
        self._check_rate_limit()
        try:
            import httpx
            
            headers = {
                "Authorization": f"Bearer {self.mastodon_client._token}",
                "Content-Type": "application/json"
            }
            
            url = f"{self.mastodon_client._base_url}/api/v1/admin/reports/{report_id}/resolve"
            
            with httpx.Client() as client:
                response = client.post(url, headers=headers, timeout=30.0)
                response.raise_for_status()
                api_response_data = response.json()

            logger.info(f"Resolved report {report_id}. Response: {response.status_code}")
            return api_response_data
        except Exception as e:
            logger.error(f"Failed to resolve report {report_id}: {e}")
            raise