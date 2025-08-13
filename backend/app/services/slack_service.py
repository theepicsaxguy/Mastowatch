"""Slack integration helpers."""

from collections.abc import Mapping

import httpx
from app.config import get_settings


class SlackService:
    """Post Slack messages for configured events."""

    def __init__(self, webhook_map: Mapping[str, str]):
        self._webhook_map = dict(webhook_map)

    def post_event(self, event: str, text: str) -> None:
        """Send message for event if mapped."""
        url = self._webhook_map.get(event)
        if not url:
            return
        httpx.post(url, json={"text": text}, timeout=10)


slack_service = SlackService(get_settings().SLACK_WEBHOOKS)


def get_slack_service() -> SlackService:
    """Return SlackService instance."""
    return slack_service
