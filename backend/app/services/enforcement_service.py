"""Helpers for applying and reverting moderation actions."""

import logging
from typing import Any

from app.config import get_settings
from app.db import SessionLocal
from app.mastodon_client import MastoClient
from app.models import AuditLog

logger = logging.getLogger(__name__)
settings = get_settings()


class EnforcementService:
    """Wrap Mastodon admin endpoints used for moderation."""

    def __init__(self, mastodon_client: MastoClient):
        self.mastodon_client = mastodon_client

    def _log_action(
        self,
        *,
        action_type: str,
        account_id: str,
        rule_id: int | None,
        evidence: dict[str, Any] | None,
        api_response: Any,
    ) -> None:
        with SessionLocal() as session:
            session.add(
                AuditLog(
                    action_type=action_type,
                    triggered_by_rule_id=rule_id,
                    target_account_id=account_id,
                    evidence=evidence,
                    api_response=api_response,
                )
            )
            session.commit()

    def _post_action(
        self,
        account_id: str,
        payload: dict[str, Any],
        *,
        rule_id: int | None = None,
        evidence: dict[str, Any] | None = None,
    ) -> None:
        if settings.DRY_RUN:
            logger.info("DRY RUN: %s %s", account_id, payload.get("type"))
            self._log_action(
                action_type=payload.get("type", ""),
                account_id=account_id,
                rule_id=rule_id,
                evidence=evidence,
                api_response={"dry_run": True},
            )
            return
        path = f"/api/v1/admin/accounts/{account_id}/action"
        resp = self.mastodon_client._make_request("POST", path, json=payload)
        self._log_action(
            action_type=payload.get("type", ""),
            account_id=account_id,
            rule_id=rule_id,
            evidence=evidence,
            api_response=resp.json(),
        )

    def warn_account(
        self,
        account_id: str,
        *,
        text: str | None = None,
        warning_preset_id: str | None = None,
        rule_id: int | None = None,
        evidence: dict[str, Any] | None = None,
    ) -> None:
        """Send an admin warning."""
        payload: dict[str, Any] = {"type": "none"}
        if text:
            payload["text"] = text
        if warning_preset_id:
            payload["warning_preset_id"] = warning_preset_id
        self._post_action(account_id, payload, rule_id=rule_id, evidence=evidence)

    def silence_account(
        self,
        account_id: str,
        *,
        text: str | None = None,
        warning_preset_id: str | None = None,
        rule_id: int | None = None,
        evidence: dict[str, Any] | None = None,
    ) -> None:
        """Silence an account."""
        payload: dict[str, Any] = {"type": "silence"}
        if text:
            payload["text"] = text
        if warning_preset_id:
            payload["warning_preset_id"] = warning_preset_id
        self._post_action(account_id, payload, rule_id=rule_id, evidence=evidence)

    def suspend_account(
        self,
        account_id: str,
        *,
        text: str | None = None,
        warning_preset_id: str | None = None,
        rule_id: int | None = None,
        evidence: dict[str, Any] | None = None,
    ) -> None:
        """Suspend an account."""
        payload: dict[str, Any] = {"type": "suspend"}
        if text:
            payload["text"] = text
        if warning_preset_id:
            payload["warning_preset_id"] = warning_preset_id
        self._post_action(account_id, payload, rule_id=rule_id, evidence=evidence)

    def unsilence_account(
        self,
        account_id: str,
        *,
        rule_id: int | None = None,
        evidence: dict[str, Any] | None = None,
    ) -> None:
        """Lift a previously applied silence."""
        if settings.DRY_RUN:
            logger.info("DRY RUN: unsilence %s", account_id)
            self._log_action(
                action_type="unsilence",
                account_id=account_id,
                rule_id=rule_id,
                evidence=evidence,
                api_response={"dry_run": True},
            )
            return
        path = f"/api/v1/admin/accounts/{account_id}/unsilence"
        resp = self.mastodon_client._make_request("POST", path)
        self._log_action(
            action_type="unsilence",
            account_id=account_id,
            rule_id=rule_id,
            evidence=evidence,
            api_response=resp.json(),
        )

    def unsuspend_account(
        self,
        account_id: str,
        *,
        rule_id: int | None = None,
        evidence: dict[str, Any] | None = None,
    ) -> None:
        """Lift a previously applied suspension."""
        if settings.DRY_RUN:
            logger.info("DRY RUN: unsuspend %s", account_id)
            self._log_action(
                action_type="unsuspend",
                account_id=account_id,
                rule_id=rule_id,
                evidence=evidence,
                api_response={"dry_run": True},
            )
            return
        path = f"/api/v1/admin/accounts/{account_id}/unsuspend"
        resp = self.mastodon_client._make_request("POST", path)
        self._log_action(
            action_type="unsuspend",
            account_id=account_id,
            rule_id=rule_id,
            evidence=evidence,
            api_response=resp.json(),
        )
