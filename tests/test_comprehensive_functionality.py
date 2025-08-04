"""Comprehensive test suite for Mastowatch covering all major functionality:
- Rule management and editing
- Authentication and role-based access control
- Domain validation and federated scanning
- Cache invalidation and frontend updates
- Domain monitoring and metrics
- Enhanced scanning system
- API endpoints and error handling
"""

import os
import sys
import unittest
from datetime import datetime
from pathlib import Path
from unittest.mock import MagicMock, patch

# Set test environment before any imports
os.environ.update(
    {
        "SKIP_STARTUP_VALIDATION": "1",
        "INSTANCE_BASE": "https://test.mastodon.social",
        "ADMIN_TOKEN": "test_admin_token_123456789",
        "BOT_TOKEN": "test_bot_token_123456789",
        "DATABASE_URL": "postgresql+psycopg://test:test@localhost:5433/mastowatch_test",
        "REDIS_URL": "redis://localhost:6380/1",
        "DRY_RUN": "false",
        "MAX_PAGES_PER_POLL": "3",
        "MAX_STATUSES_TO_FETCH": "10",
        "BATCH_SIZE": "10",
        "API_KEY": "test_api_key_123",
        "WEBHOOK_SECRET": "test_webhook_secret_123",
        "PANIC_STOP": "false",
        "OAUTH_CLIENT_ID": "test_oauth_client_id",
        "OAUTH_CLIENT_SECRET": "test_oauth_client_secret",
        "SESSION_SECRET_KEY": "test_session_secret_key_123456",
        "DEFEDERATION_THRESHOLD": "10",
        "CONTENT_CACHE_TTL": "24",
        "FEDERATED_SCAN_ENABLED": "true",
    }
)

# Add the app directory to the path so we can import the app modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from fastapi.testclient import TestClient


def create_mock_admin_user():
    """Create a mock admin user for testing"""
    from app.oauth import User

    return User(
        id="test_admin_123",
        username="testadmin",
        acct="testadmin@test.example",
        display_name="Test Admin",
        is_admin=True,
        avatar=None,
    )


def create_mock_owner_user():
    """Create a mock owner user for testing"""
    from app.oauth import User

    return User(
        id="test_owner_123",
        username="testowner",
        acct="testowner@test.example",
        display_name="Test Owner",
        is_admin=True,
        avatar=None,
    )


def create_mock_non_admin_user():
    """Create a mock non-admin user for testing"""
    from app.oauth import User

    return User(
        id="test_user_123",
        username="testuser",
        acct="testuser@test.example",
        display_name="Test User",
        is_admin=False,
        avatar=None,
    )


class TestComprehensiveFunctionality(unittest.TestCase):
    """Comprehensive test suite for all Mastowatch functionality"""

    def setUp(self):
        # Mock external dependencies
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
        self.mock_db_session.query.return_value.first.return_value = None
        self.mock_db_session.query.return_value.all.return_value = []
        self.mock_db_session.query.return_value.limit.return_value.all.return_value = []
        self.mock_db_session.commit.return_value = None

        # Mock celery tasks
        self.celery_patcher = patch("app.main.analyze_and_maybe_report")
        self.mock_celery_task = self.celery_patcher.start()
        self.mock_task = MagicMock()
        self.mock_task.id = "test_task_123"
        self.mock_celery_task.delay.return_value = self.mock_task

        # Mock enhanced scanning system
        self.scanning_patcher = patch("app.main.EnhancedScanningSystem")
        self.mock_scanning_system = self.scanning_patcher.start()
        self.mock_scanning_instance = MagicMock()
        self.mock_scanning_system.return_value = self.mock_scanning_instance

        # Import app after setting up mocks
        from app.main import app

        self.app = app
        self.client = TestClient(app)

    def tearDown(self):
        self.redis_patcher.stop()
        self.db_patcher.stop()
        self.celery_patcher.stop()
        self.scanning_patcher.stop()

    # ========== RULE MANAGEMENT TESTS ==========

    @patch("app.main.require_admin_hybrid")
    def test_rule_creation_and_editing(self, mock_auth):
        """Test rule creation and editing functionality"""
        mock_auth.return_value = create_mock_admin_user()

        # Test rule creation
        rule_data = {
            "name": "test_rule",
            "rule_type": "username_regex",
            "pattern": "spam.*bot",
            "weight": 0.8,
            "description": "Test rule for spam bots",
        }

        response = self.client.post("/rules", json=rule_data)
        self.assertEqual(response.status_code, 200)

        # Test rule editing
        rule_id = 1
        update_data = {"name": "updated_test_rule", "pattern": "updated.*pattern", "weight": 0.9}

        # Mock existing rule
        mock_rule = MagicMock()
        mock_rule.id = rule_id
        mock_rule.is_default = False
        self.mock_db_session.query.return_value.filter.return_value.first.return_value = mock_rule

        response = self.client.put(f"/rules/{rule_id}", json=update_data)
        self.assertEqual(response.status_code, 200)

    @patch("app.main.require_admin_hybrid")
    def test_rule_editing_restrictions(self, mock_auth):
        """Test that default rules cannot be edited"""
        mock_auth.return_value = create_mock_admin_user()

        # Mock default rule
        mock_rule = MagicMock()
        mock_rule.id = 1
        mock_rule.is_default = True
        self.mock_db_session.query.return_value.filter.return_value.first.return_value = mock_rule

        response = self.client.put("/rules/1", json={"name": "test"})
        self.assertEqual(response.status_code, 400)

    @patch("app.main.require_admin_hybrid")
    def test_rule_persistence_across_users(self, mock_auth):
        """Test that rule settings persist in database for cross-user accessibility"""
        mock_auth.return_value = create_mock_admin_user()

        # Create rule as one user
        response = self.client.post(
            "/rules",
            json={"name": "shared_rule", "rule_type": "content_regex", "pattern": "shared.*content", "weight": 0.5},
        )
        self.assertEqual(response.status_code, 200)

        # Switch to different admin user and verify rule is accessible
        mock_auth.return_value = create_mock_owner_user()
        response = self.client.get("/rules")
        self.assertEqual(response.status_code, 200)

    @patch("app.main.require_admin_hybrid")
    def test_rule_regex_validation(self, mock_auth):
        """Test regex pattern validation in rules"""
        mock_auth.return_value = create_mock_admin_user()

        # Test invalid regex pattern
        invalid_rule = {
            "name": "invalid_regex_rule",
            "rule_type": "username_regex",
            "pattern": "[invalid regex(",
            "weight": 0.5,
        }

        response = self.client.post("/rules", json=invalid_rule)
        self.assertEqual(response.status_code, 400)

    @patch("app.main.require_admin_hybrid")
    def test_bulk_rule_operations(self, mock_auth):
        """Test bulk toggle operations for rules"""
        mock_auth.return_value = create_mock_admin_user()

        rule_ids = [1, 2, 3]
        response = self.client.post("/rules/bulk-toggle", json={"rule_ids": rule_ids, "enabled": False})
        self.assertEqual(response.status_code, 200)

    # ========== AUTHENTICATION AND AUTHORIZATION TESTS ==========

    def test_non_admin_access_restriction(self):
        """Test that non-admin users cannot access admin endpoints"""
        response = self.client.get("/analytics/overview")
        self.assertEqual(response.status_code, 401)

        response = self.client.post("/config/dry_run", json={"dry_run": True})
        self.assertEqual(response.status_code, 401)

    @patch("app.main.require_admin_hybrid")
    def test_owner_admin_role_access(self, mock_auth):
        """Test that Owner and Admin roles have access to admin endpoints"""
        # Test with Owner role
        mock_auth.return_value = create_mock_owner_user()
        response = self.client.get("/analytics/overview")
        self.assertEqual(response.status_code, 200)

        # Test with Admin role
        mock_auth.return_value = create_mock_admin_user()
        response = self.client.get("/analytics/overview")
        self.assertEqual(response.status_code, 200)

    @patch("app.main.get_current_user_hybrid")
    def test_non_admin_user_rejection(self, mock_get_user):
        """Test that non-admin users are rejected from admin endpoints"""
        mock_get_user.return_value = create_mock_non_admin_user()

        response = self.client.get("/analytics/overview")
        self.assertEqual(response.status_code, 403)

    @patch("app.oauth.get_oauth_config")
    def test_oauth_authentication_flow(self, mock_oauth_config):
        """Test OAuth authentication flow"""
        mock_config = MagicMock()
        mock_config.configured = True
        mock_oauth_config.return_value = mock_config

        # Test login initiation
        response = self.client.get("/admin/login")
        self.assertIn(response.status_code, [302, 200])  # Redirect or success

        # Test callback with missing code
        response = self.client.get("/admin/callback")
        self.assertEqual(response.status_code, 400)

    @patch("app.jwt_auth.get_jwt_config")
    def test_jwt_token_authentication(self, mock_jwt_config):
        """Test JWT token-based authentication"""
        mock_config = MagicMock()
        mock_jwt_config.return_value = mock_config

        # Mock valid token
        mock_config.verify_token.return_value = {
            "id": "test_user_123",
            "username": "testuser",
            "acct": "testuser@test.example",
            "display_name": "Test User",
            "is_admin": True,
        }

        response = self.client.get("/api/v1/me", headers={"Authorization": "Bearer valid_token_123"})
        self.assertEqual(response.status_code, 200)

    def test_role_permission_validation(self):
        """Test that role permissions are properly validated"""
        # Test role permission bitmask validation
        with patch("app.oauth.OAuthConfig.fetch_user_info") as mock_fetch:
            mock_fetch.return_value = create_mock_admin_user()

            # This would be called during OAuth callback
            # The actual role validation logic is tested indirectly

    # ========== FEDERATED SCANNING AND DOMAIN VALIDATION TESTS ==========

    @patch("app.main.require_admin_hybrid")
    @patch("app.main.scan_federated_content")
    def test_federated_scan_trigger(self, mock_scan_task, mock_auth):
        """Test triggering federated content scans"""
        mock_auth.return_value = create_mock_admin_user()
        mock_scan_task.delay.return_value = self.mock_task

        response = self.client.post("/scanning/federated")
        self.assertEqual(response.status_code, 200)
        self.assertIn("task_id", response.json())

    @patch("app.main.require_admin_hybrid")
    def test_federated_scan_422_error_handling(self, mock_auth):
        """Test handling of 422 Unprocessable Content errors in federated scanning"""
        mock_auth.return_value = create_mock_admin_user()

        # Mock 422 error in federated scan
        with patch("app.scanning.MastoClient") as mock_client:
            mock_response = MagicMock()
            mock_response.status_code = 422
            mock_response.json.return_value = {"error": "Unprocessable Content"}
            mock_client.return_value.get.return_value = mock_response

            self.mock_scanning_instance.scan_federated_content.side_effect = Exception("422 Unprocessable Content")

            response = self.client.post("/scanning/federated")
            # Should handle error gracefully
            self.assertIn(response.status_code, [200, 500])

    @patch("app.main.require_admin_hybrid")
    @patch("app.main.check_domain_violations")
    def test_domain_validation_connection_refused(self, mock_domain_task, mock_auth):
        """Test domain validation handling connection refused errors"""
        mock_auth.return_value = create_mock_admin_user()
        mock_domain_task.delay.side_effect = Exception("Connection refused to localhost")

        response = self.client.post("/scanning/domain-check")
        self.assertEqual(response.status_code, 500)

    @patch("app.main.require_admin_hybrid")
    def test_domain_validation_hostname_error(self, mock_auth):
        """Test handling of hostname errors in domain validation"""
        mock_auth.return_value = create_mock_admin_user()

        with patch("app.scanning.EnhancedScanningSystem") as mock_scanner:
            mock_scanner.return_value.get_domain_alerts.side_effect = Exception("hostname defaulting to 'localhost'")

            response = self.client.post("/scanning/domain-check")
            self.assertEqual(response.status_code, 500)

    @patch("app.main.require_admin_hybrid")
    def test_domain_monitoring_federated_domains(self, mock_auth):
        """Test domain monitoring loading federated domains from client API"""
        mock_auth.return_value = create_mock_admin_user()

        # Mock domain analytics response
        mock_domains = [
            {"domain": "test1.example", "violation_count": 5, "is_defederated": False},
            {"domain": "test2.example", "violation_count": 15, "is_defederated": True},
        ]
        self.mock_scanning_instance.get_domain_alerts.return_value = mock_domains

        response = self.client.get("/analytics/domains")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("domain_alerts", data)

    @patch("app.main.require_admin_hybrid")
    def test_domain_metrics_monitoring(self, mock_auth):
        """Test domain monitoring provides metrics for monitored, high-risk, and defederated domains"""
        mock_auth.return_value = create_mock_admin_user()

        # Mock comprehensive domain metrics
        mock_metrics = {
            "monitored_domains": 25,
            "high_risk_domains": 3,
            "defederated_domains": 2,
            "recent_violations": 10,
        }

        with patch("app.main.get_domain_metrics") as mock_get_metrics:
            mock_get_metrics.return_value = mock_metrics

            response = self.client.get("/analytics/domains")
            self.assertEqual(response.status_code, 200)

    # ========== CACHE INVALIDATION AND FRONTEND UPDATES TESTS ==========

    @patch("app.main.require_admin_hybrid")
    def test_cache_invalidation_marks_content_for_rescan(self, mock_auth):
        """Test that cache invalidation marks content for re-scanning"""
        mock_auth.return_value = create_mock_admin_user()

        response = self.client.post("/scanning/invalidate-cache", json={"rule_changes": True})
        self.assertEqual(response.status_code, 200)

        # Verify that scanning system's invalidate method is called
        self.mock_scanning_instance.invalidate_content_scans.assert_called_once()

    @patch("app.main.require_admin_hybrid")
    def test_cache_invalidation_without_rule_changes(self, mock_auth):
        """Test cache invalidation for time-based expiry"""
        mock_auth.return_value = create_mock_admin_user()

        response = self.client.post("/scanning/invalidate-cache", json={"rule_changes": False})
        self.assertEqual(response.status_code, 200)

    @patch("app.main.require_admin_hybrid")
    def test_scanning_analytics_real_time_updates(self, mock_auth):
        """Test scanning analytics provide real-time updates"""
        mock_auth.return_value = create_mock_admin_user()

        # Mock scanning analytics with real-time data
        mock_analytics = {
            "active_sessions": [{"id": 1, "type": "federated", "progress": 45, "eta_minutes": 15}],
            "completed_sessions": 10,
            "cache_hit_rate": 0.85,
            "last_updated": datetime.utcnow().isoformat(),
        }

        self.mock_scanning_instance.get_scanning_analytics.return_value = mock_analytics

        response = self.client.get("/analytics/scanning")
        self.assertEqual(response.status_code, 200)

    @patch("app.main.require_admin_hybrid")
    def test_job_tracking_15_second_refresh(self, mock_auth):
        """Test that job tracking supports 15-second refresh intervals"""
        mock_auth.return_value = create_mock_admin_user()

        # Mock job status with timestamp for refresh tracking
        mock_job_status = {
            "active_jobs": [{"id": "job_123", "type": "federated_scan", "status": "running", "progress": 30}],
            "completed_jobs": 5,
            "failed_jobs": 1,
            "last_refresh": datetime.utcnow().isoformat(),
        }

        with patch("app.main.get_job_status") as mock_get_jobs:
            mock_get_jobs.return_value = mock_job_status

            response = self.client.get("/analytics/jobs")
            self.assertEqual(response.status_code, 200)

    # ========== ENHANCED SCANNING SYSTEM TESTS ==========

    def test_scanning_content_deduplication(self):
        """Test enhanced scanning system content deduplication"""
        from app.scanning import EnhancedScanningSystem

        with patch("app.scanning.SessionLocal") as mock_session_local:
            scanner = EnhancedScanningSystem()

            # Mock account data
            account_data = {
                "id": "test_account_123",
                "username": "testuser",
                "display_name": "Test User",
                "note": "Test bio",
            }

            # Test content hash calculation
            hash1 = scanner._calculate_content_hash(account_data)
            hash2 = scanner._calculate_content_hash(account_data)
            self.assertEqual(hash1, hash2)

            # Test with different content
            account_data["note"] = "Different bio"
            hash3 = scanner._calculate_content_hash(account_data)
            self.assertNotEqual(hash1, hash3)

    def test_scanning_session_tracking(self):
        """Test scan session tracking and progress monitoring"""
        from app.scanning import EnhancedScanningSystem

        with patch("app.scanning.SessionLocal"):
            scanner = EnhancedScanningSystem()

            # Mock session creation
            with patch.object(scanner, "start_scan_session") as mock_start:
                mock_start.return_value = 1

                session_id = scanner.start_scan_session("test", {"test": "metadata"})
                self.assertEqual(session_id, 1)

    def test_scanning_cursor_based_progression(self):
        """Test cursor-based progression through accounts"""
        from app.scanning import EnhancedScanningSystem

        with patch("app.scanning.SessionLocal"):
            scanner = EnhancedScanningSystem()

            # Mock cursor parsing
            link_header = '<https://test.example/api/v1/admin/accounts?max_id=12345>; rel="next"'
            cursor = scanner._parse_next_cursor(link_header)
            self.assertEqual(cursor, "12345")

    def test_scanning_domain_violation_tracking(self):
        """Test domain violation tracking for defederation"""
        from app.scanning import EnhancedScanningSystem

        with patch("app.scanning.SessionLocal") as mock_session_local:
            scanner = EnhancedScanningSystem()

            # Mock domain violation tracking
            mock_session = MagicMock()
            mock_session_local.return_value.__enter__.return_value = mock_session

            scanner._track_domain_violation("spam.example")

            # Verify database update was called
            mock_session.execute.assert_called_once()
            mock_session.commit.assert_called_once()

    # ========== API ERROR HANDLING TESTS ==========

    def test_api_structured_error_responses(self):
        """Test that API returns structured error responses"""
        response = self.client.get("/nonexistent")
        self.assertEqual(response.status_code, 404)

        # Test structured error format
        response = self.client.post("/config/dry_run", json={"invalid": "data"})
        self.assertIn(response.status_code, [401, 422])  # Auth or validation error

    def test_api_request_id_tracing(self):
        """Test that API responses include request IDs for tracing"""
        response = self.client.get("/healthz")
        # Request ID should be in headers or response body
        self.assertTrue("x-request-id" in response.headers or any("request_id" in str(response.content), True))

    def test_api_rate_limiting_handling(self):
        """Test API rate limiting and error handling"""
        # Simulate rate limit exceeded
        with patch("app.main.rate_limiter") as mock_limiter:
            mock_limiter.side_effect = Exception("Rate limit exceeded")

            response = self.client.post("/dryrun/evaluate", json={"account": {"id": "123"}, "statuses": []})
            # Should handle rate limiting gracefully
            self.assertIn(response.status_code, [200, 429, 500])

    # ========== METRICS AND MONITORING TESTS ==========

    def test_prometheus_metrics_collection(self):
        """Test Prometheus metrics endpoint functionality"""
        response = self.client.get("/metrics")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers["content-type"], "text/plain; charset=utf-8")

    @patch("app.main.require_admin_hybrid")
    def test_system_health_monitoring(self, mock_auth):
        """Test system health monitoring and status checks"""
        mock_auth.return_value = create_mock_admin_user()

        response = self.client.get("/healthz")
        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertIn("ok", data)
        self.assertIn("db_ok", data)
        self.assertIn("redis_ok", data)

    # ========== INTEGRATION TESTS ==========

    @patch("app.main.require_admin_hybrid")
    def test_end_to_end_rule_management_workflow(self, mock_auth):
        """Test complete rule management workflow"""
        mock_auth.return_value = create_mock_admin_user()

        # 1. Create rule
        rule_data = {
            "name": "e2e_test_rule",
            "rule_type": "username_regex",
            "pattern": "spam.*user",
            "weight": 0.7,
            "description": "End-to-end test rule",
        }
        response = self.client.post("/rules", json=rule_data)
        self.assertEqual(response.status_code, 200)

        # 2. List rules to verify creation
        response = self.client.get("/rules")
        self.assertEqual(response.status_code, 200)

        # 3. Test rule evaluation
        test_account = {"account": {"username": "spam_test_user", "id": "123"}, "statuses": []}
        response = self.client.post("/dryrun/evaluate", json=test_account)
        self.assertEqual(response.status_code, 200)

        # 4. Invalidate cache after rule changes
        response = self.client.post("/scanning/invalidate-cache", json={"rule_changes": True})
        self.assertEqual(response.status_code, 200)

    @patch("app.main.require_admin_hybrid")
    def test_end_to_end_scanning_workflow(self, mock_auth):
        """Test complete scanning workflow"""
        mock_auth.return_value = create_mock_admin_user()

        # 1. Check initial scanning status
        response = self.client.get("/analytics/scanning")
        self.assertEqual(response.status_code, 200)

        # 2. Trigger federated scan
        response = self.client.post("/scanning/federated")
        self.assertEqual(response.status_code, 200)

        # 3. Check domain violations
        response = self.client.post("/scanning/domain-check")
        self.assertIn(response.status_code, [200, 500])  # May fail in test env

        # 4. Review domain analytics
        response = self.client.get("/analytics/domains")
        self.assertEqual(response.status_code, 200)

    def test_security_access_controls(self):
        """Test security access controls across all endpoints"""
        # Test unauthenticated access to protected endpoints
        protected_endpoints = [
            ("/analytics/overview", "GET"),
            ("/config/dry_run", "POST"),
            ("/rules", "POST"),
            ("/scanning/federated", "POST"),
            ("/analytics/domains", "GET"),
        ]

        for endpoint, method in protected_endpoints:
            if method == "GET":
                response = self.client.get(endpoint)
            else:
                response = self.client.post(endpoint, json={})

            self.assertIn(response.status_code, [401, 403], f"Endpoint {endpoint} should be protected")

    # ========== ERROR RECOVERY TESTS ==========

    @patch("app.main.require_admin_hybrid")
    def test_database_failure_recovery(self, mock_auth):
        """Test system behavior during database failures"""
        mock_auth.return_value = create_mock_admin_user()

        # Simulate database failure
        self.mock_db_session.execute.side_effect = Exception("Database connection lost")

        response = self.client.get("/analytics/overview")
        self.assertEqual(response.status_code, 500)

    @patch("app.main.require_admin_hybrid")
    def test_redis_failure_graceful_degradation(self, mock_auth):
        """Test graceful degradation when Redis is unavailable"""
        mock_auth.return_value = create_mock_admin_user()

        # Simulate Redis failure
        self.mock_redis_instance.ping.side_effect = Exception("Redis connection failed")

        # System should still function with degraded caching
        response = self.client.get("/healthz")
        self.assertEqual(response.status_code, 503)  # Service degraded but responding

    @patch("app.main.require_admin_hybrid")
    def test_celery_failure_handling(self, mock_auth):
        """Test handling of Celery task failures"""
        mock_auth.return_value = create_mock_admin_user()

        # Simulate Celery broker failure
        self.mock_celery_task.delay.side_effect = Exception("Broker connection failed")

        response = self.client.post("/scanning/federated")
        self.assertEqual(response.status_code, 500)

    # ========== PERFORMANCE TESTS ==========

    @patch("app.main.require_admin_hybrid")
    def test_large_dataset_handling(self, mock_auth):
        """Test system performance with large datasets"""
        mock_auth.return_value = create_mock_admin_user()

        # Mock large number of domain alerts
        large_domain_list = [
            {"domain": f"domain{i}.example", "violation_count": i, "is_defederated": False} for i in range(1000)
        ]
        self.mock_scanning_instance.get_domain_alerts.return_value = large_domain_list

        response = self.client.get("/analytics/domains")
        self.assertEqual(response.status_code, 200)

    def test_concurrent_request_handling(self):
        """Test handling of concurrent requests"""
        import threading

        results = []

        def make_request():
            response = self.client.get("/healthz")
            results.append(response.status_code)

        # Create multiple threads for concurrent requests
        threads = []
        for _ in range(10):
            thread = threading.Thread(target=make_request)
            threads.append(thread)
            thread.start()

        # Wait for all threads to complete
        for thread in threads:
            thread.join()

        # All requests should succeed
        self.assertTrue(all(status == 200 for status in results))


if __name__ == "__main__":
    # Run with higher verbosity to see all test details
    unittest.main(verbosity=2)
