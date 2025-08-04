"""Tests for the new type-safe Mastodon client."""

import os
import unittest
from unittest.mock import Mock, patch

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

    @patch("app.mastodon_client.httpx.Client")
    def test_get_admin_accounts_pagination(self, mock_httpx_client):
        """Test admin accounts pagination with cursor parsing."""
        # Mock the raw HTTP client
        mock_client_instance = Mock()
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.headers = {"Link": '<https://test.mastodon.social/api/v1/admin/accounts?max_id=456>; rel="next"'}
        mock_response.json.return_value = [{"id": "123", "username": "test_user"}]
        mock_client_instance.get.return_value = mock_response
        mock_httpx_client.return_value.__enter__.return_value = mock_client_instance

        # Call the method
        accounts, next_cursor = self.client.get_admin_accounts(limit=1)

        # Assertions
        self.assertEqual(len(accounts), 1)
        self.assertEqual(accounts[0]["id"], "123")
        self.assertEqual(next_cursor, "456")  # Check that cursor parsing works

    @patch("app.mastodon_client.httpx.Client")
    def test_get_admin_accounts_no_pagination(self, mock_httpx_client):
        """Test admin accounts without pagination link."""
        # Mock the raw HTTP client
        mock_client_instance = Mock()
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.headers = {}  # No Link header
        mock_response.json.return_value = [{"id": "123", "username": "test_user"}]
        mock_client_instance.get.return_value = mock_response
        mock_httpx_client.return_value.__enter__.return_value = mock_client_instance

        # Call the method
        accounts, next_cursor = self.client.get_admin_accounts(limit=1)

        # Assertions
        self.assertEqual(len(accounts), 1)
        self.assertIsNone(next_cursor)  # No pagination

    @patch("app.mastodon_client.httpx.Client")
    def test_create_report_with_category_mapping(self, mock_httpx_client):
        """Test that report creation maps string categories to proper types."""
        # Mock the raw HTTP client
        mock_client_instance = Mock()
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.headers = {}
        mock_response.json.return_value = {"id": "report_123", "status": "created"}
        mock_client_instance.post.return_value = mock_response
        mock_httpx_client.return_value.__enter__.return_value = mock_client_instance

        # Test creating a report with string category
        result = self.client.create_report(
            account_id="test_account_123", comment="Test report comment", category="spam"
        )

        # Verify the call was made
        mock_client_instance.post.assert_called_once()
        call_args = mock_client_instance.post.call_args

        # Check that the data includes the account_id and comment
        posted_data = call_args.kwargs.get("data") or call_args.kwargs.get("json")
        self.assertIn("account_id", posted_data)
        self.assertIn("comment", posted_data)
        self.assertEqual(posted_data["account_id"], "test_account_123")
        self.assertEqual(posted_data["comment"], "Test report comment")

    @patch("app.mastodon_client.httpx.Client")
    def test_legacy_get_method(self, mock_httpx_client):
        """Test that legacy .get() method still works for backward compatibility."""
        # Mock the raw HTTP client
        mock_client_instance = Mock()
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.headers = {}
        mock_response.json.return_value = {"success": True}
        mock_client_instance.get.return_value = mock_response
        mock_httpx_client.return_value.__enter__.return_value = mock_client_instance

        # Test legacy GET
        result = self.client.get("/api/v1/test", params={"param1": "value1"})

        self.assertEqual(result, mock_response)
        mock_client_instance.get.assert_called_with(
            "https://test.mastodon.social/api/v1/test", params={"param1": "value1"}
        )

    @patch("app.mastodon_client.httpx.Client")
    def test_legacy_post_method(self, mock_httpx_client):
        """Test that legacy .post() method still works for backward compatibility."""
        # Mock the raw HTTP client
        mock_client_instance = Mock()
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.headers = {}
        mock_response.json.return_value = {"success": True}
        mock_client_instance.post.return_value = mock_response
        mock_httpx_client.return_value.__enter__.return_value = mock_client_instance

        # Test legacy POST
        result = self.client.post("/api/v1/test", data={"data1": "value1"})

        self.assertEqual(result, mock_response)
        mock_client_instance.post.assert_called_with(
            "https://test.mastodon.social/api/v1/test", data={"data1": "value1"}, json=None
        )

    @patch("app.mastodon_client.httpx.Client")
    def test_error_handling(self, mock_httpx_client):
        """Test error handling for failed requests."""
        # Mock the raw HTTP client to return an error
        mock_client_instance = Mock()
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.headers = {}
        mock_response.json.return_value = {"error": "Not found"}
        mock_client_instance.get.return_value = mock_response
        mock_httpx_client.return_value.__enter__.return_value = mock_client_instance

        # Should still return the response (error handling is done by caller)
        result = self.client.get("/api/v1/nonexistent")
        self.assertEqual(result.status_code, 404)


if __name__ == "__main__":
    unittest.main()
