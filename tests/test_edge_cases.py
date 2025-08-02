import hashlib
import hmac
import json
import os
import sys
import unittest
from pathlib import Path
from unittest.mock import MagicMock, Mock, patch

# Set test environment before any imports
os.environ.update(
    {
        "SKIP_STARTUP_VALIDATION": "1",
        "INSTANCE_BASE": "https://test.mastodon.social",
        "ADMIN_TOKEN": "test_admin_token_123456789",
        "BOT_TOKEN": "test_bot_token_123456789",
        "DATABASE_URL": "postgresql+psycopg://test:test@localhost:5433/mastowatch_test",
        "REDIS_URL": "redis://localhost:6380/1",
        "DRY_RUN": "true",
        "MAX_PAGES_PER_POLL": "1",
        "MAX_STATUSES_TO_FETCH": "10",
        "BATCH_SIZE": "5",
        "API_KEY": "test_api_key_123",
        "WEBHOOK_SECRET": "test_webhook_secret_123",
        "PANIC_STOP": "false",
    }
)

# Add the app directory to the path so we can import the app modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from fastapi.testclient import TestClient


class TestEdgeCasesAndErrorHandling(unittest.TestCase):
    def setUp(self):
        # Mock all external dependencies before importing main
        self.redis_patcher = patch("redis.from_url")
        self.mock_redis = self.redis_patcher.start()
        self.mock_redis_instance = MagicMock()
        self.mock_redis.return_value = self.mock_redis_instance
        self.mock_redis_instance.ping.return_value = True
        self.mock_redis_instance.get.return_value = None
        self.mock_redis_instance.setex.return_value = True

        self.db_patcher = patch("app.main.SessionLocal")
        self.mock_db = self.db_patcher.start()
        self.mock_db_session = MagicMock()
        self.mock_db.return_value.__enter__.return_value = self.mock_db_session
        self.mock_db_session.execute.return_value.scalar.return_value = 1
        self.mock_db_session.query.return_value.scalar.return_value = 0
        self.mock_db_session.merge.return_value = None
        self.mock_db_session.commit.return_value = None

        # Mock celery task
        self.celery_patcher = patch("app.main.analyze_and_maybe_report")
        self.mock_celery_task = self.celery_patcher.start()
        self.mock_task = MagicMock()
        self.mock_task.id = "test_task_123"
        self.mock_celery_task.delay.return_value = self.mock_task

        # Import app after setting up mocks
        from app.main import app

        self.app = app
        self.client = TestClient(app)

    def tearDown(self):
        self.redis_patcher.stop()
        self.db_patcher.stop()
        self.celery_patcher.stop()

    def test_health_check_database_failure(self):
        """Test health check when database is down"""
        self.mock_db_session.execute.side_effect = Exception("Database connection failed")

        response = self.client.get("/healthz")
        self.assertEqual(response.status_code, 503)
        data = response.json()
        # When health check fails, FastAPI returns the detail in the response
        if "detail" in data:
            health_data = data["detail"]
            self.assertFalse(health_data["ok"])
            self.assertFalse(health_data["db_ok"])
            self.assertIn("response_time_ms", health_data)
        else:
            self.assertFalse(data["ok"])
            self.assertFalse(data["db_ok"])
            self.assertIn("response_time_ms", data)

    def test_health_check_redis_failure(self):
        """Test health check when Redis is down"""
        self.mock_redis_instance.ping.side_effect = Exception("Redis connection failed")

        response = self.client.get("/healthz")
        self.assertEqual(response.status_code, 503)
        data = response.json()
        # When health check fails, FastAPI returns the detail in the response
        if "detail" in data:
            health_data = data["detail"]
            self.assertFalse(health_data["ok"])
            self.assertFalse(health_data["redis_ok"])
        else:
            self.assertFalse(data["ok"])
            self.assertFalse(data["redis_ok"])

    def test_webhook_no_secret_configured(self):
        """Test webhook when WEBHOOK_SECRET is not configured"""
        with patch("app.main.settings") as mock_settings:
            mock_settings.WEBHOOK_SECRET = None

            response = self.client.post(
                "/webhooks/status",
                json={"account": {"id": "123"}, "statuses": []},
                headers={"X-Hub-Signature-256": "sha256=invalid"},
            )
            self.assertEqual(response.status_code, 503)
            data = response.json()
            self.assertEqual(data["detail"]["error"], "webhook_not_configured")

    def test_webhook_invalid_signature_format(self):
        """Test webhook with invalid signature format"""
        response = self.client.post(
            "/webhooks/status",
            json={"account": {"id": "123"}, "statuses": []},
            headers={"X-Hub-Signature-256": "invalid_format"},
        )
        self.assertEqual(response.status_code, 401)
        data = response.json()
        self.assertEqual(data["detail"]["error"], "invalid_signature_format")

    def test_webhook_signature_mismatch(self):
        """Test webhook with incorrect signature"""
        response = self.client.post(
            "/webhooks/status",
            json={"account": {"id": "123"}, "statuses": []},
            headers={"X-Hub-Signature-256": "sha256=wrong_signature"},
        )
        self.assertEqual(response.status_code, 401)
        data = response.json()
        self.assertEqual(data["detail"]["error"], "signature_mismatch")

    def test_webhook_valid_signature(self):
        """Test webhook with valid signature"""
        payload = json.dumps({"account": {"id": "123", "acct": "test@example.com"}, "statuses": []})
        signature = hmac.new("test_webhook_secret_123".encode(), payload.encode(), hashlib.sha256).hexdigest()

        response = self.client.post(
            "/webhooks/status",
            content=payload,
            headers={"X-Hub-Signature-256": f"sha256={signature}", "Content-Type": "application/json"},
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["ok"])
        self.assertTrue(data["enqueued"])

    def test_webhook_missing_account(self):
        """Test webhook with missing account data"""
        payload = json.dumps({"statuses": []})
        signature = hmac.new("test_webhook_secret_123".encode(), payload.encode(), hashlib.sha256).hexdigest()

        response = self.client.post(
            "/webhooks/status",
            content=payload,
            headers={"X-Hub-Signature-256": f"sha256={signature}", "Content-Type": "application/json"},
        )
        self.assertEqual(response.status_code, 400)
        data = response.json()
        self.assertEqual(data["detail"]["error"], "missing_account_data")

    def test_webhook_invalid_json(self):
        """Test webhook with invalid JSON payload"""
        payload = "invalid json {"
        signature = hmac.new("test_webhook_secret_123".encode(), payload.encode(), hashlib.sha256).hexdigest()

        response = self.client.post(
            "/webhooks/status",
            content=payload,
            headers={"X-Hub-Signature-256": f"sha256={signature}", "Content-Type": "application/json"},
        )
        self.assertEqual(response.status_code, 400)
        data = response.json()
        self.assertEqual(data["detail"]["error"], "invalid_json_payload")

    def test_webhook_deduplication(self):
        """Test webhook deduplication functionality"""
        self.mock_redis_instance.get.return_value = "1"  # Simulate duplicate

        payload = json.dumps({"account": {"id": "123", "acct": "test@example.com"}, "statuses": []})
        signature = hmac.new("test_webhook_secret_123".encode(), payload.encode(), hashlib.sha256).hexdigest()

        response = self.client.post(
            "/webhooks/status",
            content=payload,
            headers={"X-Hub-Signature-256": f"sha256={signature}", "Content-Type": "application/json"},
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["ok"])
        self.assertFalse(data["enqueued"])
        self.assertEqual(data["reason"], "duplicate")

    def test_webhook_celery_task_failure(self):
        """Test webhook when Celery task enqueueing fails"""
        self.mock_celery_task.delay.side_effect = Exception("Celery broker unavailable")

        payload = json.dumps({"account": {"id": "123", "acct": "test@example.com"}, "statuses": []})
        signature = hmac.new("test_webhook_secret_123".encode(), payload.encode(), hashlib.sha256).hexdigest()

        response = self.client.post(
            "/webhooks/status",
            content=payload,
            headers={"X-Hub-Signature-256": f"sha256={signature}", "Content-Type": "application/json"},
        )
        self.assertEqual(response.status_code, 500)
        data = response.json()
        self.assertEqual(data["detail"]["error"], "task_enqueue_failed")

    def test_config_dry_run_null_value(self):
        """Test dry run config with null value"""
        response = self.client.post(
            "/config/dry_run", json={"dry_run": None, "updated_by": "test_user"}, headers={"X-API-Key": "test_api_key_123"}
        )
        self.assertEqual(response.status_code, 422)
        data = response.json()
        self.assertIn("detail", data)
        # FastAPI validation error for null boolean

    def test_config_dry_run_database_failure(self):
        """Test dry run config when database update fails"""
        self.mock_db_session.merge.side_effect = Exception("Database error")

        response = self.client.post(
            "/config/dry_run", json={"dry_run": False, "updated_by": "test_user"}, headers={"X-API-Key": "test_api_key_123"}
        )
        self.assertEqual(response.status_code, 500)
        data = response.json()
        self.assertEqual(data["detail"]["error"], "database_update_failed")

    def test_config_panic_stop_database_failure(self):
        """Test panic stop config when database update fails"""
        self.mock_db_session.merge.side_effect = Exception("Database error")

        response = self.client.post(
            "/config/panic_stop",
            json={"panic_stop": True, "updated_by": "test_user"},
            headers={"X-API-Key": "test_api_key_123"},
        )
        self.assertEqual(response.status_code, 500)
        data = response.json()
        self.assertEqual(data["detail"]["error"], "database_update_failed")

    def test_rules_reload_file_not_found(self):
        """Test rules reload when rules.yml is missing"""
        with patch("app.main.Rules.from_yaml") as mock_rules:
            mock_rules.side_effect = FileNotFoundError("rules.yml not found")

            response = self.client.post("/config/rules/reload", headers={"X-API-Key": "test_api_key_123"})
            self.assertEqual(response.status_code, 404)
            data = response.json()
            self.assertEqual(data["detail"]["error"], "rules_file_not_found")

    def test_rules_reload_parse_error(self):
        """Test rules reload when rules.yml has invalid syntax"""
        with patch("app.main.Rules.from_yaml") as mock_rules:
            mock_rules.side_effect = Exception("Invalid YAML syntax")

            response = self.client.post("/config/rules/reload", headers={"X-API-Key": "test_api_key_123"})
            self.assertEqual(response.status_code, 400)
            data = response.json()
            self.assertEqual(data["detail"]["error"], "rules_parse_failed")

    def test_analytics_overview_database_error(self):
        """Test analytics overview when database query fails"""
        self.mock_db_session.query.side_effect = Exception("Database query failed")

        response = self.client.get("/analytics/overview")
        self.assertEqual(response.status_code, 500)
        data = response.json()
        self.assertEqual(data["detail"]["error"], "analytics_fetch_failed")

    def test_analytics_timeline_invalid_days(self):
        """Test analytics timeline with invalid days parameter"""
        response = self.client.get("/analytics/timeline?days=400")
        self.assertEqual(response.status_code, 400)
        data = response.json()
        self.assertEqual(data["detail"]["error"], "invalid_days_parameter")

    def test_analytics_timeline_zero_days(self):
        """Test analytics timeline with zero days"""
        response = self.client.get("/analytics/timeline?days=0")
        self.assertEqual(response.status_code, 400)
        data = response.json()
        self.assertEqual(data["detail"]["error"], "invalid_days_parameter")

    def test_dryrun_evaluate_empty_payload(self):
        """Test dry run evaluation with empty payload"""
        response = self.client.post("/dryrun/evaluate", json={})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("score", data)
        self.assertIn("hits", data)

    def test_dryrun_evaluate_minimal_account(self):
        """Test dry run evaluation with minimal account data"""
        payload = {"account": {"id": "123"}, "statuses": []}

        response = self.client.post("/dryrun/evaluate", json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("score", data)
        self.assertIn("hits", data)

    def test_zero_statuses_edge_case(self):
        """Test webhook handling with zero statuses"""
        payload = json.dumps({"account": {"id": "123", "acct": "test@example.com"}, "statuses": []})
        signature = hmac.new("test_webhook_secret_123".encode(), payload.encode(), hashlib.sha256).hexdigest()

        response = self.client.post(
            "/webhooks/status",
            content=payload,
            headers={"X-Hub-Signature-256": f"sha256={signature}", "Content-Type": "application/json"},
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["ok"])
        self.assertEqual(data["status_count"], 0)

    def test_large_payload_webhook(self):
        """Test webhook with large payload"""
        large_statuses = [{"id": str(i), "content": "x" * 1000} for i in range(100)]
        payload = json.dumps({"account": {"id": "123", "acct": "test@example.com"}, "statuses": large_statuses})
        signature = hmac.new("test_webhook_secret_123".encode(), payload.encode(), hashlib.sha256).hexdigest()

        response = self.client.post(
            "/webhooks/status",
            content=payload,
            headers={"X-Hub-Signature-256": f"sha256={signature}", "Content-Type": "application/json"},
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status_count"], 100)
        self.assertIn("processing_time_ms", data)


if __name__ == "__main__":
    unittest.main()
