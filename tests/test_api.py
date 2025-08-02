import os
import sys
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

# Set test environment before any imports
os.environ.update({
    "SKIP_STARTUP_VALIDATION": "1",
    "INSTANCE_BASE": "https://test.mastodon.social",
    "ADMIN_TOKEN": "test_admin_token_123",
    "BOT_TOKEN": "test_bot_token_123", 
    "DATABASE_URL": "postgresql+psycopg://test:test@localhost:5433/test",
    "REDIS_URL": "redis://localhost:6380/1",
    "API_KEY": "test_api_key_123",
    "WEBHOOK_SECRET": "test_webhook_secret",
})

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
        avatar=None
    )


class TestAPIEndpoints(unittest.TestCase):
    def setUp(self):
        # Mock external dependencies at import time
        with patch("redis.from_url") as mock_redis, \
             patch("app.db.SessionLocal") as mock_db:
            
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

    @patch("app.main.require_admin")
    def test_dry_run_toggle(self, mock_auth):
        """Test dry run configuration endpoint"""
        mock_auth.return_value = create_mock_admin_user()

        response = self.client.post("/config/dry_run", json={"dry_run": False, "updated_by": "test_user"})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("dry_run", data)
        self.assertIn("persisted", data)

    @patch("app.main.require_admin")
    def test_panic_stop_toggle(self, mock_auth):
        """Test panic stop configuration endpoint"""
        mock_auth.return_value = create_mock_admin_user()

        response = self.client.post("/config/panic_stop", json={"panic_stop": True, "updated_by": "test_user"})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("panic_stop", data)
        self.assertIn("persisted", data)

    @patch("app.main.require_admin")
    def test_rules_reload(self, mock_auth):
        """Test rules reload endpoint"""
        mock_auth.return_value = create_mock_admin_user()

        response = self.client.post("/config/rules/reload")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("reloaded", data)
        self.assertIn("ruleset_sha256", data)

    def test_dryrun_evaluate(self):
        """Test the dry run evaluation endpoint"""
        payload = {"account": {"id": "123", "acct": "test@example.com"}, "statuses": [{"content": "test status"}]}

        response = self.client.post("/dryrun/evaluate", json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("score", data)
        self.assertIn("hits", data)

    @patch("app.main.require_admin")
    def test_analytics_overview(self, mock_auth):
        """Test analytics overview endpoint"""
        mock_auth.return_value = create_mock_admin_user()
        
        response = self.client.get("/analytics/overview")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("totals", data)
        self.assertIn("recent_24h", data)
        self.assertIn("rules", data)
        self.assertIn("top_domains", data)

    @patch("app.main.require_admin")
    def test_analytics_timeline(self, mock_auth):
        """Test analytics timeline endpoint"""
        mock_auth.return_value = create_mock_admin_user()
        
        response = self.client.get("/analytics/timeline?days=7")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("analyses", data)
        self.assertIn("reports", data)

    @patch("app.main.require_admin")
    def test_get_current_rules(self, mock_auth):
        """Test current rules endpoint"""
        mock_auth.return_value = create_mock_admin_user()
        
        response = self.client.get("/rules/current")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("rules", data)
        self.assertIn("report_threshold", data)

    def test_unauthorized_analytics(self):
        """Test that analytics endpoints require authentication"""
        response = self.client.get("/analytics/overview")
        self.assertEqual(response.status_code, 401)
        
        response = self.client.get("/analytics/timeline")
        self.assertEqual(response.status_code, 401)
        
        response = self.client.get("/rules/current")
        self.assertEqual(response.status_code, 401)

    def test_unauthorized_config_endpoints(self):
        """Test that config endpoints require authentication"""
        response = self.client.post("/config/dry_run", json={"dry_run": False})
        self.assertEqual(response.status_code, 401)
        
        response = self.client.post("/config/panic_stop", json={"panic_stop": True})
        self.assertEqual(response.status_code, 401)
        
        response = self.client.post("/config/rules/reload")
        self.assertEqual(response.status_code, 401)

    def test_unauthorized_webhook(self):
        """Test that webhook rejects requests without proper signature"""
        response = self.client.post(
            "/webhooks/status", json={"account": {"id": "123"}, "statuses": []}, headers={"X-Hub-Signature-256": "invalid"}
        )
        # Should return 503 if no webhook secret is configured, or 401 if configured but wrong signature
        self.assertIn(response.status_code, [401, 503])


if __name__ == "__main__":
    unittest.main()
