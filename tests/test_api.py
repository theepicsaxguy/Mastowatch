import os
import sys
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

# Add the app directory to the path so we can import the app modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from fastapi.testclient import TestClient

from app.config import get_settings
from app.main import app


class TestAPIEndpoints(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)
        # Mock Redis and DB for tests
        self.redis_patcher = patch("redis.from_url")
        self.mock_redis = self.redis_patcher.start()
        self.mock_redis.return_value.ping.return_value = True

        self.db_patcher = patch("app.main.SessionLocal")
        self.mock_db = self.db_patcher.start()
        self.mock_db.return_value.__enter__.return_value.execute.return_value = None

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

    @patch("app.main.require_api_key")
    def test_dry_run_toggle(self, mock_auth):
        """Test dry run configuration endpoint"""
        mock_auth.return_value = True

        response = self.client.post("/config/dry_run", json={"dry_run": False, "updated_by": "test_user"})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("dry_run", data)
        self.assertIn("persisted", data)

    @patch("app.main.require_api_key")
    def test_panic_stop_toggle(self, mock_auth):
        """Test panic stop configuration endpoint"""
        mock_auth.return_value = True

        response = self.client.post("/config/panic_stop", json={"panic_stop": True, "updated_by": "test_user"})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("panic_stop", data)
        self.assertIn("persisted", data)

    @patch("app.main.require_api_key")
    def test_rules_reload(self, mock_auth):
        """Test rules reload endpoint"""
        mock_auth.return_value = True

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

    def test_analytics_overview(self):
        """Test analytics overview endpoint"""
        response = self.client.get("/analytics/overview")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("totals", data)
        self.assertIn("recent_24h", data)
        self.assertIn("rules", data)
        self.assertIn("top_domains", data)

    def test_analytics_timeline(self):
        """Test analytics timeline endpoint"""
        response = self.client.get("/analytics/timeline?days=7")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("analyses", data)
        self.assertIn("reports", data)

    def test_get_current_rules(self):
        """Test current rules endpoint"""
        response = self.client.get("/rules/current")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("rules", data)
        self.assertIn("report_threshold", data)

    def test_unauthorized_webhook(self):
        """Test that webhook rejects requests without proper signature"""
        response = self.client.post(
            "/webhooks/status", json={"account": {"id": "123"}, "statuses": []}, headers={"X-Hub-Signature-256": "invalid"}
        )
        # Should return 503 if no webhook secret is configured, or 401 if configured but wrong signature
        self.assertIn(response.status_code, [401, 503])


if __name__ == "__main__":
    unittest.main()
