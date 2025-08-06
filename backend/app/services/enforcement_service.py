"""Helpers for applying and reverting moderation actions."""

import logging
from typing import Any

from app.config import get_settings
from app.mastodon_client import MastoClient

logger = logging.getLogger(__name__)
settings = get_settings()


class EnforcementService:
    """Wrap Mastodon admin endpoints used for moderation."""

    def __init__(self, mastodon_client: MastoClient):
        self.mastodon_client = mastodon_client

    def _post_action(self, account_id: str, payload: dict[str, Any]) -> None:
        if settings.DRY_RUN:
            logger.info("DRY RUN: %s %s", account_id, payload.get("type"))
            return
        path = f"/api/v1/admin/accounts/{account_id}/action"
        self.mastodon_client._make_request("POST", path, json=payload)

    def warn_account(
        self,
        account_id: str,
        *,
        text: str | None = None,
        warning_preset_id: str | None = None,
    ) -> None:
        """Send an admin warning."""
        payload: dict[str, Any] = {"type": "none"}
        if text:
            payload["text"] = text
        if warning_preset_id:
            payload["warning_preset_id"] = warning_preset_id
        self._post_action(account_id, payload)

    def silence_account(
        self,
        account_id: str,
        *,
        text: str | None = None,
        warning_preset_id: str | None = None,
    ) -> None:
        """Silence an account."""
        payload: dict[str, Any] = {"type": "silence"}
        if text:
            payload["text"] = text
        if warning_preset_id:
            payload["warning_preset_id"] = warning_preset_id
        self._post_action(account_id, payload)

    def suspend_account(
        self,
        account_id: str,
        *,
        text: str | None = None,
        warning_preset_id: str | None = None,
    ) -> None:
        """Suspend an account."""
        payload: dict[str, Any] = {"type": "suspend"}
        if text:
            payload["text"] = text
        if warning_preset_id:
            payload["warning_preset_id"] = warning_preset_id
        self._post_action(account_id, payload)

    def unsilence_account(self, account_id: str) -> None:
        """Lift a previously applied silence."""
        if settings.DRY_RUN:
            logger.info("DRY RUN: unsilence %s", account_id)
            return
        path = f"/api/v1/admin/accounts/{account_id}/unsilence"
        self.mastodon_client._make_request("POST", path)

    def unsuspend_account(self, account_id: str) -> None:
        """Lift a previously applied suspension."""
        if settings.DRY_RUN:
            logger.info("DRY RUN: unsuspend %s", account_id)
            return
        path = f"/api/v1/admin/accounts/{account_id}/unsuspend"
        self.mastodon_client._make_request("POST", path)
