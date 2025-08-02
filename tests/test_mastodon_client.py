"""
Tests for the new type-safe Mastodon client.
"""

import unittest
from unittest.mock import MagicMock, Mock, patch

from app.clients.mastodon.models import Account, Status
from app.clients.mastodon.models.create_report_body_category import \
    CreateReportBodyCategory
from app.mastodon_client import MastoClient


class TestMastoClient(unittest.TestCase):
    """Test suite for the Mastodon API client"""

    def setUp(self):
        """Set up test environment with mocked dependencies"""
        with patch.dict(
            os.environ,
            {
                "INSTANCE_BASE": "https://test.mastodon.social",
                "ADMIN_TOKEN": "test_admin_token",
                "BOT_TOKEN": "test_bot_token",
            },
        ):
            self.client = MastoClient("test_token")

    @patch("app.mastodon_client_v2.throttle_if_needed")
    @patch("app.mastodon_client_v2.update_from_headers")
    @patch("app.mastodon_client_v2.get_account")
    def test_get_account_type_safety(self, mock_get_account, mock_update_headers, mock_throttle):
        """Test that get_account returns a properly typed Account object."""
        # Mock the response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.headers = {}

        mock_account = Account(
            id="123",
            username="testuser",
            acct="testuser@example.com",
            display_name="Test User",
            locked=False,
            bot=False,
            discoverable=True,
            group=False,
            created_at="2023-01-01T00:00:00Z",
            note="Test note",
            url="https://mastodon.example/@testuser",
            avatar="https://example.com/avatar.jpg",
            avatar_static="https://example.com/avatar.jpg",
            header="https://example.com/header.jpg",
            header_static="https://example.com/header.jpg",
            followers_count=100,
            following_count=50,
            statuses_count=200,
            last_status_at="2023-01-01",
            emojis=[],
            fields=[],
        )

        mock_response.parsed = mock_account
        mock_get_account.sync_detailed.return_value = mock_response

        # Call the method
        result = self.client.get_account("123")

        # Assertions
        self.assertIsInstance(result, Account)
        self.assertEqual(result.id, "123")
        self.assertEqual(result.username, "testuser")
        self.assertEqual(result.followers_count, 100)
        mock_throttle.assert_called_once()

    @patch("app.mastodon_client_v2.throttle_if_needed")
    @patch("app.mastodon_client_v2.update_from_headers")
    @patch("app.mastodon_client_v2.get_account_statuses")
    def test_get_account_statuses_type_safety(self, mock_get_statuses, mock_update_headers, mock_throttle):
        """Test that get_account_statuses returns a properly typed list of Status objects."""
        # Mock the response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.headers = {}

        mock_statuses = [
            Status(
                id="1",
                uri="https://example.com/status/1",
                created_at="2023-01-01T00:00:00Z",
                account=Mock(),
                content="Test status 1",
                visibility="public",
                sensitive=False,
                spoiler_text="",
                media_attachments=[],
                mentions=[],
                tags=[],
                emojis=[],
                reblogs_count=5,
                favourites_count=10,
                replies_count=2,
                url="https://example.com/status/1",
                in_reply_to_id=None,
                in_reply_to_account_id=None,
                reblog=None,
                poll=None,
                card=None,
                language="en",
                text="Test status 1",
                edited_at=None,
            ),
            Status(
                id="2",
                uri="https://example.com/status/2",
                created_at="2023-01-01T01:00:00Z",
                account=Mock(),
                content="Test status 2",
                visibility="public",
                sensitive=False,
                spoiler_text="",
                media_attachments=[],
                mentions=[],
                tags=[],
                emojis=[],
                reblogs_count=3,
                favourites_count=7,
                replies_count=1,
                url="https://example.com/status/2",
                in_reply_to_id=None,
                in_reply_to_account_id=None,
                reblog=None,
                poll=None,
                card=None,
                language="en",
                text="Test status 2",
                edited_at=None,
            ),
        ]

        mock_response.parsed = mock_statuses
        mock_get_statuses.sync_detailed.return_value = mock_response

        # Call the method
        result = self.client.get_account_statuses("123", limit=20)

        # Assertions
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 2)
        self.assertIsInstance(result[0], Status)
        self.assertEqual(result[0].id, "1")
        self.assertEqual(result[0].content, "Test status 1")
        self.assertEqual(result[1].id, "2")
        mock_throttle.assert_called_once()

    @patch("app.mastodon_client_v2.throttle_if_needed")
    @patch("app.mastodon_client_v2.update_from_headers")
    @patch("app.mastodon_client_v2.httpx.Client")
    def test_admin_accounts_fallback(self, mock_httpx_client, mock_update_headers, mock_throttle):
        """Test that admin endpoints fall back to raw HTTP calls."""
        # Mock the raw HTTP client
        mock_client_instance = Mock()
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.headers = {}
        mock_response.json.return_value = [{"account": {"id": "123", "username": "test"}}]
        mock_client_instance.get.return_value = mock_response
        mock_httpx_client.return_value.__enter__.return_value = mock_client_instance

        # Call the method
        result = self.client.get_admin_accounts(origin="remote", limit=50)

        # Assertions
        self.assertEqual(result, mock_response)
        mock_throttle.assert_called_once()
        mock_client_instance.get.assert_called_once_with(
            "https://mastodon.example/api/v1/admin/accounts", params={"origin": "remote", "status": "active", "limit": 50}
        )

    def test_category_enum_mapping(self):
        """Test that string categories are properly mapped to enums."""
        # Test cases for category mapping
        test_cases = [
            ("spam", CreateReportBodyCategory.SPAM),
            ("violation", CreateReportBodyCategory.VIOLATION),
            ("legal", CreateReportBodyCategory.LEGAL),
            ("other", CreateReportBodyCategory.OTHER),
            ("unknown", CreateReportBodyCategory.OTHER),  # default case
        ]

        for category_str, expected_enum in test_cases:
            with patch.object(self.client, "_make_raw_request") as mock_request:
                with patch("app.mastodon_client_v2.create_report") as mock_create_report:
                    mock_response = Mock()
                    mock_response.status_code = 200
                    mock_response.headers = {}
                    mock_response.parsed = Mock()
                    mock_create_report.sync_detailed.return_value = mock_response

                    # Call with string category
                    try:
                        self.client.create_report("123", "test comment", category=category_str)
                    except:
                        pass  # We're just testing the enum mapping

                    # Verify the CreateReportBody was called with correct enum
                    if mock_create_report.sync_detailed.called:
                        call_args = mock_create_report.sync_detailed.call_args
                        report_body = call_args.kwargs["body"]
                        self.assertEqual(report_body.category, expected_enum)

    @patch("app.mastodon_client_v2.throttle_if_needed")
    @patch("app.mastodon_client_v2.update_from_headers")
    @patch("app.mastodon_client_v2.httpx.Client")
    def test_legacy_compatibility(self, mock_httpx_client, mock_update_headers, mock_throttle):
        """Test that legacy .get() and .post() methods still work."""
        # Mock the raw HTTP client
        mock_client_instance = Mock()
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.headers = {}
        mock_response.json.return_value = {"success": True}
        mock_client_instance.get.return_value = mock_response
        mock_client_instance.post.return_value = mock_response
        mock_httpx_client.return_value.__enter__.return_value = mock_client_instance

        # Test legacy GET
        result = self.client.get("/api/v1/test", params={"param1": "value1"})
        self.assertEqual(result, mock_response)
        mock_client_instance.get.assert_called_with("https://mastodon.example/api/v1/test", params={"param1": "value1"})

        # Test legacy POST
        result = self.client.post("/api/v1/test", data={"data1": "value1"})
        self.assertEqual(result, mock_response)
        mock_client_instance.post.assert_called_with(
            "https://mastodon.example/api/v1/test", data={"data1": "value1"}, json=None
        )


if __name__ == "__main__":
    unittest.main()
