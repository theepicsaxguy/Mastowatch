"""Tests for the type-safe Mastodon client using current methods."""

import os
import sys
import types
import unittest
from unittest.mock import Mock, patch

import httpx

mastodon_pkg = types.ModuleType("app.clients.mastodon")
mastodon_pkg.__path__ = []

client_mod = types.ModuleType("app.clients.mastodon.client")


class AuthenticatedClient:  # noqa: D401
    def __init__(self, *_, **__):
        pass


class Client:  # noqa: D401
    def __init__(self, *_, **__):
        pass


client_mod.AuthenticatedClient = AuthenticatedClient
client_mod.Client = Client

accounts_pkg = types.ModuleType("app.clients.mastodon.accounts")
accounts_pkg.__path__ = []

get_account_mod = types.ModuleType("app.clients.mastodon.accounts.get_account")


def _get_account_sync(*_, **__):
    return None


get_account_mod.sync = _get_account_sync

get_account_statuses_mod = types.ModuleType("app.clients.mastodon.accounts.get_account_statuses")


def _get_account_statuses_sync(*_, **__):
    return []


get_account_statuses_mod.sync = _get_account_statuses_sync

models_pkg = types.ModuleType("app.clients.mastodon.models")
models_pkg.__path__ = []

create_report_body_mod = types.ModuleType("app.clients.mastodon.models.create_report_body")


class CreateReportBody:  # noqa: D401
    def __init__(self, account_id, comment, category, forward, status_ids, rule_ids):
        self.account_id = account_id
        self.comment = comment
        self.category = category
        self.forward = forward
        self.status_ids = status_ids
        self.rule_ids = rule_ids

    def to_dict(self):
        return {
            "account_id": self.account_id,
            "comment": self.comment,
            "category": self.category,
            "forward": self.forward,
            "status_ids": self.status_ids,
            "rule_ids": self.rule_ids,
        }


create_report_body_mod.CreateReportBody = CreateReportBody

reports_pkg = types.ModuleType("app.clients.mastodon.reports")
reports_pkg.__path__ = []

create_report_mod = types.ModuleType("app.clients.mastodon.reports.create_report")


def _create_report_sync(*_, **__):
    return None


create_report_mod.sync = _create_report_sync

sys.modules.update(
    {
        "app.clients.mastodon": mastodon_pkg,
        "app.clients.mastodon.client": client_mod,
        "app.clients.mastodon.accounts": accounts_pkg,
        "app.clients.mastodon.accounts.get_account": get_account_mod,
        "app.clients.mastodon.accounts.get_account_statuses": get_account_statuses_mod,
        "app.clients.mastodon.models": models_pkg,
        "app.clients.mastodon.models.create_report_body": create_report_body_mod,
        "app.clients.mastodon.reports": reports_pkg,
        "app.clients.mastodon.reports.create_report": create_report_mod,
    }
)

from app.mastodon_client import MastoClient


class TestMastoClient(unittest.TestCase):
    def setUp(self):
        with patch.dict(
            os.environ,
            {
                "INSTANCE_BASE": "https://test.mastodon.social",
                "ADMIN_TOKEN": "test_admin_token",
                "BOT_TOKEN": "test_bot_token",
            },
        ):
            self.client = MastoClient("test_token")

    @patch("app.mastodon_client.httpx.request")
    def test_get_admin_accounts_pagination(self, mock_request):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.headers = {"Link": '<https://test.mastodon.social/api/v1/admin/accounts?max_id=456>; rel="next"'}
        mock_response.json.return_value = [{"id": "123", "username": "test_user"}]
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        accounts, next_cursor = self.client.get_admin_accounts(limit=1)
        self.assertEqual(len(accounts), 1)
        self.assertEqual(accounts[0]["id"], "123")
        self.assertEqual(next_cursor, "456")

    @patch("app.mastodon_client.httpx.request")
    def test_get_admin_accounts_no_pagination(self, mock_request):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.headers = {}
        mock_response.json.return_value = [{"id": "123", "username": "test_user"}]
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        accounts, next_cursor = self.client.get_admin_accounts(limit=1)
        self.assertEqual(len(accounts), 1)
        self.assertIsNone(next_cursor)

    @patch("app.mastodon_client.create_report_sync")
    def test_create_report_with_category_mapping(self, mock_create_report):
        mock_report = Mock()
        mock_report.to_dict.return_value = {"id": "report_123", "status": "created"}
        mock_create_report.return_value = mock_report

        result = self.client.create_report(
            account_id="test_account_123",
            comment="Test report comment",
            category="spam",
        )

        self.assertEqual(result["id"], "report_123")
        self.assertEqual(result["status"], "created")
        args, kwargs = mock_create_report.call_args
        body = kwargs["body"]
        self.assertEqual(body.account_id, "test_account_123")
        self.assertEqual(body.comment, "Test report comment")

    @patch("app.mastodon_client.httpx.request")
    def test_error_handling(self, mock_request):
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.headers = {}
        mock_response.json.return_value = {"error": "Not found"}
        mock_response.raise_for_status.side_effect = httpx.HTTPStatusError(
            "Not found", request=Mock(), response=mock_response
        )
        mock_request.return_value = mock_response

        with self.assertRaises(httpx.HTTPStatusError):
            self.client.get_admin_accounts()
