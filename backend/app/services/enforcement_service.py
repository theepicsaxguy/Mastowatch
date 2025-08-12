"""Helpers for applying and reverting moderation actions."""

import logging
from collections.abc import Callable
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

    def _execute(
        self,
        label: str,
        func: Callable[..., dict[str, Any]],
        account_id: str,
        *,
        rule_id: int | None = None,
        evidence: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> None:
        if settings.DRY_RUN:
            logger.info("DRY RUN: %s %s", account_id, label)
            self._log_action(
                action_type=label,
                account_id=account_id,
                rule_id=rule_id,
                evidence=evidence,
                api_response={"dry_run": True},
            )
            return
        api_response = func(account_id, **kwargs)
        self._log_action(
            action_type=label,
            account_id=account_id,
            rule_id=rule_id,
            evidence=evidence,
            api_response=api_response,
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
        self._execute(
            "warn",
            self.mastodon_client.warn_account,
            account_id,
            rule_id=rule_id,
            evidence=evidence,
            text=text,
            warning_preset_id=warning_preset_id,
        )

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
        self._execute(
            "silence",
            self.mastodon_client.silence_account,
            account_id,
            rule_id=rule_id,
            evidence=evidence,
            text=text,
            warning_preset_id=warning_preset_id,
        )

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
        self._execute(
            "suspend",
            self.mastodon_client.suspend_account,
            account_id,
            rule_id=rule_id,
            evidence=evidence,
            text=text,
            warning_preset_id=warning_preset_id,
        )

    def unsilence_account(
        self,
        account_id: str,
        *,
        rule_id: int | None = None,
        evidence: dict[str, Any] | None = None,
    ) -> None:
        """Lift a previously applied silence."""
        self._execute(
            "unsilence",
            self.mastodon_client.unsilence_account,
            account_id,
            rule_id=rule_id,
            evidence=evidence,
        )

    def unsuspend_account(
        self,
        account_id: str,
        *,
        rule_id: int | None = None,
        evidence: dict[str, Any] | None = None,
    ) -> None:
        """Lift a previously applied suspension."""
        self._execute(
            "unsuspend",
            self.mastodon_client.unsuspend_account,
            account_id,
            rule_id=rule_id,
            evidence=evidence,
        )
