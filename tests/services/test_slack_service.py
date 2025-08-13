"""Tests for Slack service."""

from unittest.mock import patch

from app.services.slack_service import SlackService


def test_posts_configured_event():
    """Send payload when event is configured."""
    svc = SlackService({"rule": "http://example.com"})
    with patch("httpx.post") as post:
        svc.post_event("rule", "hi")
        post.assert_called_once_with("http://example.com", json={"text": "hi"}, timeout=10)


def test_ignores_unconfigured_event():
    """Skip posting when event has no webhook."""
    svc = SlackService({})
    with patch("httpx.post") as post:
        svc.post_event("rule", "hi")
        post.assert_not_called()
