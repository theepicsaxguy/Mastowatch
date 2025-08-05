import os
import sys
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

# Set test environment before any imports
os.environ.update(
    {
        "SKIP_STARTUP_VALIDATION": "1",
        "INSTANCE_BASE": "https://test.mastodon.social",
        "ADMIN_TOKEN": "test_admin_token_123",
        "BOT_TOKEN": "test_bot_token_123",
        "DATABASE_URL": "postgresql+psycopg://test:test@localhost:5433/test",
        "REDIS_URL": "redis://localhost:6380/1",
        "API_KEY": "test_api_key_123",
        "WEBHOOK_SECRET": "test_webhook_secret",
    }
)

# Add the app directory to the path so we can import the app modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from fastapi.testclient import TestClient

from app.oauth import User


def create_mock_admin_user():
    """Create a mock admin user for testing"""
    return User(
        id="test_user_123",
        username="testadmin",
        acct="testadmin@test.example",
        display_name="Test Admin",
        is_admin=True,
        avatar=None,
    )


class TestAPIEndpoints(unittest.TestCase):
    def setUp(self):
        # Mock external dependencies at import time
        with patch("redis.from_url") as mock_redis, patch("app.db.SessionLocal") as mock_db:
            mock_redis_instance = MagicMock()
            mock_redis.return_value = mock_redis_instance
            mock_redis_instance.ping.return_value = True

            mock_session = MagicMock()
            mock_db.return_value.__enter__.return_value = mock_session
            mock_session.execute.return_value = None

            # Import app after setting up mocks
            from app.main import app

            self.app = app
            self.client = TestClient(app)

        # Continue mocking for test execution
        self.redis_patcher = patch("redis.from_url")
        self.mock_redis = self.redis_patcher.start()
        self.mock_redis_instance = MagicMock()
        self.mock_redis.return_value = self.mock_redis_instance
        self.mock_redis_instance.ping.return_value = True

        self.db_patcher = patch("app.main.SessionLocal")
        self.mock_db = self.db_patcher.start()
        self.mock_session = MagicMock()
        self.mock_db.return_value.__enter__.return_value = self.mock_session
        self.mock_session.execute.return_value = None

    def tearDown(self):
        self.redis_patcher.stop()
        self.db_patcher.stop()

    def test_healthz_endpoint(self):
        """Test that the health check endpoint returns proper status"""
        response = self.client.get("/healthz")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("ok", data)
        self.assertIn("db_ok", data)
        self.assertIn("redis_ok", data)
        self.assertIn("dry_run", data)
        self.assertIn("panic_stop", data)

    def test_metrics_endpoint(self):
        """Test that metrics endpoint returns Prometheus format"""
        response = self.client.get("/metrics")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers["content-type"], "text/plain; charset=utf-8")

    # NEW API ROUTER TESTS

    @patch("app.api.config.require_admin_hybrid")
    def test_dry_run_toggle_new_endpoint(self, mock_auth):
        """Test dry run configuration endpoint with new API structure"""
        mock_auth.return_value = create_mock_admin_user()

        response = self.client.post("/config/dry_run", json={"dry_run": False, "updated_by": "test_user"})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("dry_run", data)

    @patch("app.api.config.require_admin_hybrid")
    def test_panic_stop_toggle_new_endpoint(self, mock_auth):
        """Test panic stop configuration endpoint with new API structure"""
        mock_auth.return_value = create_mock_admin_user()

        response = self.client.post("/config/panic_stop", json={"panic_stop": True, "updated_by": "test_user"})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("panic_stop", data)

    @patch("app.api.analytics.require_admin_hybrid")
    def test_analytics_overview_new_endpoint(self, mock_auth):
        """Test analytics overview endpoint with new API structure"""
        mock_auth.return_value = create_mock_admin_user()

        response = self.client.get("/analytics/overview")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("totals", data)
        self.assertIn("recent_24h", data)

    @patch("app.api.analytics.require_admin_hybrid")
    def test_analytics_timeline_new_endpoint(self, mock_auth):
        """Test analytics timeline endpoint with new API structure"""
        mock_auth.return_value = create_mock_admin_user()

        response = self.client.get("/analytics/timeline?days=7")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("analyses", data)
        self.assertIn("reports", data)

    @patch("app.api.rules.require_admin_hybrid")
    def test_get_current_rules_new_endpoint(self, mock_auth):
        """Test current rules endpoint with new API structure"""
        mock_auth.return_value = create_mock_admin_user()

        with patch("app.api.rules.rule_service") as mock_rule_service:
            mock_rule_service.get_active_rules.return_value = ([], {"report_threshold": 1.0}, "test_sha")

            response = self.client.get("/rules/")
            self.assertEqual(response.status_code, 200)
            data = response.json()
            self.assertIn("rules", data)
            self.assertIn("report_threshold", data)

    @patch("app.api.rules.require_admin_hybrid")
    def test_create_rule_new_endpoint(self, mock_auth):
        """Test creating a new rule via API"""
        mock_auth.return_value = create_mock_admin_user()

        with patch("app.api.rules.rule_service") as mock_rule_service:
            # Mock rule creation
            mock_rule = MagicMock()
            mock_rule.id = 1
            mock_rule.name = "test_rule"
            mock_rule.detector_type = "regex"
            mock_rule_service.create_rule.return_value = mock_rule

            rule_data = {
                "name": "test_rule",
                "detector_type": "regex",
                "pattern": "test_pattern",
                "weight": 1.0,
                "action_type": "report",
                "trigger_threshold": 1.0,
            }

            response = self.client.post("/rules/", json=rule_data)
            self.assertEqual(response.status_code, 200)

            # Verify rule service was called
            mock_rule_service.create_rule.assert_called_once()

    @patch("app.api.rules.require_admin_hybrid")
    def test_update_rule_new_endpoint(self, mock_auth):
        """Test updating a rule via API"""
        mock_auth.return_value = create_mock_admin_user()

        with patch("app.api.rules.rule_service") as mock_rule_service:
            # Mock rule update
            mock_rule = MagicMock()
            mock_rule.id = 1
            mock_rule.weight = 2.0
            mock_rule_service.update_rule.return_value = mock_rule

            update_data = {"weight": 2.0}

            response = self.client.put("/rules/1", json=update_data)
            self.assertEqual(response.status_code, 200)

            # Verify rule service was called
            mock_rule_service.update_rule.assert_called_once_with(1, **update_data)

    @patch("app.api.rules.require_admin_hybrid")
    def test_delete_rule_new_endpoint(self, mock_auth):
        """Test deleting a rule via API"""
        mock_auth.return_value = create_mock_admin_user()

        with patch("app.api.rules.rule_service") as mock_rule_service:
            mock_rule_service.delete_rule.return_value = True

            response = self.client.delete("/rules/1")
            self.assertEqual(response.status_code, 200)

            # Verify rule service was called
            mock_rule_service.delete_rule.assert_called_once_with(1)

    @patch("app.api.scanning.require_api_key")
    def test_get_next_accounts_to_scan_endpoint(self, mock_api_key):
        mock_api_key.return_value = True
        with patch("app.api.scanning.EnhancedScanningSystem") as mock_scanner:
            instance = mock_scanner.return_value
            instance.get_next_accounts_to_scan.return_value = ([{"id": "1"}], "next123")
            response = self.client.get("/scan/accounts?session_type=remote&limit=1")
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json(), {"accounts": [{"id": "1"}], "next_cursor": "next123"})

    # NEW WEBHOOK TESTS

    @patch("app.main.process_new_report")
    def test_webhook_report_created(self, mock_process_report):
        """Test webhook handling for report.created events"""
        mock_process_report.delay.return_value = MagicMock(id="task_123")

        payload = {"id": "report_123", "account": {"id": "account_123"}, "target_account": {"id": "target_account_123"}}

        # Calculate proper HMAC signature
        import hashlib
        import hmac

        webhook_secret = os.environ["WEBHOOK_SECRET"]
        body = str(payload).encode("utf-8")
        signature = "sha256=" + hmac.new(webhook_secret.encode("utf-8"), body, hashlib.sha256).hexdigest()

        response = self.client.post(
            "/webhooks/mastodon_events",
            json=payload,
            headers={"X-Hub-Signature-256": signature, "X-Mastodon-Event": "report.created"},
        )

        # Should process the webhook
        self.assertEqual(response.status_code, 200)

    @patch("app.main.process_new_status")
    def test_webhook_status_created(self, mock_process_status):
        """Test webhook handling for status.created events"""
        mock_process_status.delay.return_value = MagicMock(id="task_456")

        payload = {"id": "status_123", "account": {"id": "account_123"}, "content": "test status content"}

        # Calculate proper HMAC signature
        import hashlib
        import hmac
        import json

        webhook_secret = os.environ["WEBHOOK_SECRET"]
        body = json.dumps(payload).encode("utf-8")
        signature = "sha256=" + hmac.new(webhook_secret.encode("utf-8"), body, hashlib.sha256).hexdigest()

        response = self.client.post(
            "/webhooks/mastodon_events",
            json=payload,
            headers={"X-Hub-Signature-256": signature, "X-Mastodon-Event": "status.created"},
        )

        # Should process the webhook
        self.assertEqual(response.status_code, 200)

    def test_unauthorized_analytics(self):
        """Test that analytics endpoints require authentication"""
        response = self.client.get("/analytics/overview")
        self.assertEqual(response.status_code, 401)

        response = self.client.get("/analytics/timeline")
        self.assertEqual(response.status_code, 401)

    def test_unauthorized_rules_endpoints(self):
        """Test that rules endpoints require authentication"""
        response = self.client.get("/rules/")
        self.assertEqual(response.status_code, 401)

        response = self.client.post("/rules/", json={"name": "test"})
        self.assertEqual(response.status_code, 401)

    def test_unauthorized_config_endpoints(self):
        """Test that config endpoints require authentication"""
        response = self.client.post("/config/dry_run", json={"dry_run": False})
        self.assertEqual(response.status_code, 401)

        response = self.client.post("/config/panic_stop", json={"panic_stop": True})
        self.assertEqual(response.status_code, 401)

    def test_unauthorized_webhook(self):
        """Test that webhook rejects requests without proper signature"""
        response = self.client.post(
            "/webhooks/mastodon_events",
            json={"account": {"id": "123"}, "statuses": []},
            headers={"X-Hub-Signature-256": "invalid"},
        )
        # Should return 401 for invalid signature
        self.assertEqual(response.status_code, 401)


if __name__ == "__main__":
    unittest.main()
