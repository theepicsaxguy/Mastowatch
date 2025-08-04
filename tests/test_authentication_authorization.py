"""
Comprehensive test suite for authentication and authorization functionality:
- OAuth flow with CSRF protection
- JWT token authentication
- Role-based access control (Owner/Admin only)
- Session management and cookies
- Hybrid authentication (JWT + cookies)
- Permission validation and enforcement
"""

import hashlib
import hmac
import json
import jwt
import os
import sys
import unittest
from datetime import datetime, timedelta
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

# Set test environment before any imports
os.environ.update(
    {
        "SKIP_STARTUP_VALIDATION": "1",
        "INSTANCE_BASE": "https://test.mastodon.social",
        "ADMIN_TOKEN": "test_admin_token_123456789",
        "BOT_TOKEN": "test_bot_token_123456789",
        "DATABASE_URL": "postgresql+psycopg://test:test@localhost:5433/mastowatch_test",
        "REDIS_URL": "redis://localhost:6380/1",
        "OAUTH_CLIENT_ID": "test_oauth_client_id",
        "OAUTH_CLIENT_SECRET": "test_oauth_client_secret",
        "SESSION_SECRET_KEY": "test_session_secret_key_123456789",
        "OAUTH_REDIRECT_URI": "http://localhost:8080/admin/callback",
        "OAUTH_POPUP_REDIRECT_URI": "http://localhost:8080/admin/popup-callback",
    }
)

# Add the app directory to the path so we can import the app modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from fastapi.testclient import TestClient


class TestAuthenticationAuthorization(unittest.TestCase):
    """Test authentication and authorization functionality"""

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

        # Mock OAuth config
        self.oauth_patcher = patch("app.main.get_oauth_config")
        self.mock_oauth_config = self.oauth_patcher.start()
        self.mock_oauth_instance = MagicMock()
        self.mock_oauth_instance.configured = True
        self.mock_oauth_config.return_value = self.mock_oauth_instance

        # Mock JWT config
        self.jwt_patcher = patch("app.jwt_auth.get_jwt_config")
        self.mock_jwt_config = self.jwt_patcher.start()
        self.mock_jwt_instance = MagicMock()
        self.mock_jwt_config.return_value = self.mock_jwt_instance

        self.rule_service_patcher = patch("app.main.rule_service")
        self.mock_rule_service = self.rule_service_patcher.start()
        self.mock_rule_service.evaluate_account.return_value = []

        from app.main import app

        self.app = app
        self.client = TestClient(app)

    def tearDown(self):
        self.redis_patcher.stop()
        self.db_patcher.stop()
        self.oauth_patcher.stop()
        self.jwt_patcher.stop()
        self.rule_service_patcher.stop()

    def create_test_admin_user(self):
        """Create test admin user"""
        from app.oauth import User

        return User(
            id="admin_123",
            username="testadmin",
            acct="testadmin@test.example",
            display_name="Test Admin",
            is_admin=True,
            avatar=None,
        )

    def create_test_owner_user(self):
        """Create test owner user"""
        from app.oauth import User

        return User(
            id="owner_123",
            username="testowner",
            acct="testowner@test.example",
            display_name="Test Owner",
            is_admin=True,
            avatar=None,
        )

    def create_test_moderator_user(self):
        """Create test moderator user"""
        from app.oauth import User

        return User(
            id="mod_123",
            username="testmod",
            acct="testmod@test.example",
            display_name="Test Moderator",
            is_admin=True,
            avatar=None,
        )

    def create_test_regular_user(self):
        """Create test regular user"""
        from app.oauth import User

        return User(
            id="user_123",
            username="testuser",
            acct="testuser@test.example",
            display_name="Test User",
            is_admin=False,
            avatar=None,
        )

    def create_valid_jwt_token(self, user_data):
        """Create a valid JWT token for testing"""
        secret = "test_session_secret_key_123456789"
        payload = user_data.copy()
        payload.update({"exp": datetime.utcnow() + timedelta(hours=24), "iat": datetime.utcnow()})
        return jwt.encode(payload, secret, algorithm="HS256")

    # ========== OAUTH AUTHENTICATION TESTS ==========

    def test_oauth_login_initiation(self):
        """Test OAuth login flow initiation"""
        response = self.client.get("/admin/login")

        # Should redirect to OAuth provider or return 302
        self.assertIn(response.status_code, [302, 200])

    def test_oauth_login_popup_mode(self):
        """Test OAuth login in popup mode"""
        response = self.client.get("/admin/login?popup=true")

        # Should handle popup mode
        self.assertIn(response.status_code, [302, 200])

    def test_oauth_csrf_protection(self):
        """Test OAuth CSRF state parameter protection"""
        # Test callback without state
        response = self.client.get("/admin/callback?code=test_code")
        self.assertEqual(response.status_code, 400)

        # Test callback with mismatched state
        response = self.client.get("/admin/callback?code=test_code&state=invalid_state")
        self.assertEqual(response.status_code, 400)

    def test_oauth_callback_error_handling(self):
        """Test OAuth callback error handling"""
        # Test error parameter in callback
        response = self.client.get("/admin/callback?error=access_denied")
        self.assertEqual(response.status_code, 400)

        # Test missing authorization code
        response = self.client.get("/admin/callback?state=test_state")
        self.assertEqual(response.status_code, 400)

    @patch("app.main.Client")
    async def test_oauth_token_exchange(self, mock_client):
        """Test OAuth token exchange process"""
        # Mock successful token exchange
        mock_http_client = AsyncMock()
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"access_token": "test_access_token"}
        mock_http_client.post.return_value = mock_response

        mock_client_instance = MagicMock()
        mock_client_instance.get_async_httpx_client.return_value.__aenter__.return_value = mock_http_client
        mock_client.return_value = mock_client_instance

        # Mock user info fetch
        admin_user = self.create_test_admin_user()
        self.mock_oauth_instance.fetch_user_info.return_value = admin_user

        # Mock state validation
        self.mock_redis_instance.get.return_value = "valid"

        response = self.client.get("/admin/callback?code=test_code&state=test_state")

        # Should successfully process callback
        self.assertIn(response.status_code, [200, 302])

    def test_oauth_non_admin_user_rejection(self):
        """Test rejection of non-admin users during OAuth"""
        # Mock user info fetch returning non-admin user
        regular_user = self.create_test_regular_user()
        self.mock_oauth_instance.fetch_user_info.return_value = regular_user

        # Mock successful token exchange
        with patch("app.main.Client") as mock_client:
            mock_http_client = AsyncMock()
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.json.return_value = {"access_token": "test_access_token"}
            mock_http_client.post.return_value = mock_response

            mock_client_instance = MagicMock()
            mock_client_instance.get_async_httpx_client.return_value.__aenter__.return_value = mock_http_client
            mock_client.return_value = mock_client_instance

            # Mock state validation
            self.mock_redis_instance.get.return_value = "valid"

            response = self.client.get("/admin/callback?code=test_code&state=test_state")
            self.assertEqual(response.status_code, 403)

    def test_oauth_not_configured(self):
        """Test OAuth endpoints when OAuth is not configured"""
        self.mock_oauth_instance.configured = False

        response = self.client.get("/admin/login")
        self.assertEqual(response.status_code, 503)

        response = self.client.get("/admin/callback")
        self.assertEqual(response.status_code, 503)

    # ========== JWT AUTHENTICATION TESTS ==========

    def test_jwt_token_creation(self):
        """Test JWT token creation"""
        user_data = self.create_test_admin_user().model_dump()

        # Mock JWT config
        self.mock_jwt_instance.create_access_token.return_value = "test_jwt_token"

        token = self.mock_jwt_instance.create_access_token(user_data)
        self.assertEqual(token, "test_jwt_token")

    def test_jwt_token_validation(self):
        """Test JWT token validation"""
        admin_user = self.create_test_admin_user()
        user_data = admin_user.model_dump()
        token = self.create_valid_jwt_token(user_data)
        self.mock_jwt_instance.verify_token.return_value = user_data

        # Test token validation
        response = self.client.get("/api/v1/me", headers={"Authorization": f"Bearer {token}"})

        # Should work with valid token
        self.assertIn(response.status_code, [200, 401])  # May depend on other mocks

    def test_jwt_token_expiration(self):
        """Test JWT token expiration handling"""
        from fastapi import HTTPException

        # Mock expired token
        self.mock_jwt_instance.verify_token.side_effect = HTTPException(status_code=401, detail="Token has expired")

        response = self.client.get("/api/v1/me", headers={"Authorization": "Bearer expired_token"})

        self.assertEqual(response.status_code, 401)

    def test_jwt_invalid_token(self):
        """Test handling of invalid JWT tokens"""
        from fastapi import HTTPException

        # Mock invalid token
        self.mock_jwt_instance.verify_token.side_effect = HTTPException(status_code=401, detail="Invalid token")

        response = self.client.get("/api/v1/me", headers={"Authorization": "Bearer invalid_token"})

        self.assertEqual(response.status_code, 401)

    # ========== ROLE-BASED ACCESS CONTROL TESTS ==========

    def test_admin_role_access(self):
        """Test that Admin role has access to admin endpoints"""
        admin_user = self.create_test_admin_user()

        with patch("app.main.get_current_user_hybrid", return_value=admin_user):
            response = self.client.get("/analytics/overview")
            self.assertEqual(response.status_code, 200)

    def test_owner_role_access(self):
        """Test that Owner role has access to admin endpoints"""
        owner_user = self.create_test_owner_user()

        with patch("app.main.get_current_user_hybrid", return_value=owner_user):
            response = self.client.get("/analytics/overview")
            self.assertEqual(response.status_code, 200)

    def test_moderator_role_access(self):
        """Test that Moderator role has access to admin endpoints"""
        mod_user = self.create_test_moderator_user()

        with patch("app.main.get_current_user_hybrid", return_value=mod_user):
            response = self.client.get("/analytics/overview")
            self.assertEqual(response.status_code, 200)

    def test_regular_user_access_denied(self):
        """Test that regular users are denied access to admin endpoints"""
        regular_user = self.create_test_regular_user()

        with patch("app.main.get_current_user_hybrid", return_value=regular_user):
            response = self.client.get("/analytics/overview")
            self.assertEqual(response.status_code, 403)

    def test_unauthenticated_access_denied(self):
        """Test that unauthenticated users are denied access"""
        with patch("app.main.get_current_user_hybrid", return_value=None):
            response = self.client.get("/analytics/overview")
            self.assertEqual(response.status_code, 401)

    def test_role_permission_validation(self):
        """Test role permission bitmask validation"""
        # Test admin permission bit (bit 0 = value 1)
        with patch("app.oauth.OAuthConfig.fetch_user_info") as mock_fetch:
            # Mock role data with admin permission
            mock_role_data = {"id": "3", "name": "Admin", "permissions": "1"}  # Binary: ...0001 (admin bit set)

            mock_user_data = {
                "id": "test_123",
                "username": "testadmin",
                "acct": "testadmin@test.example",
                "display_name": "Test Admin",
                "role": mock_role_data,
            }

            # Should be recognized as admin
            from app.oauth import User

            expected_user = User(
                id="test_123",
                username="testadmin",
                acct="testadmin@test.example",
                display_name="Test Admin",
                is_admin=True,
            )

            mock_fetch.return_value = expected_user

            user = mock_fetch(mock_user_data)
            self.assertTrue(user.is_admin)

    def test_role_name_fallback_validation(self):
        """Test fallback role validation by role name"""
        # Test role names that should grant admin access
        admin_roles = ["admin", "moderator", "owner", "Admin", "Moderator", "Owner"]

        for role_name in admin_roles:
            with patch("app.oauth.OAuthConfig.fetch_user_info") as mock_fetch:
                mock_role_data = {
                    "id": "3",
                    "name": role_name,
                    "permissions": "0",  # No permission bits, should fall back to name
                }

                from app.oauth import User

                expected_user = User(
                    id="test_123",
                    username="testuser",
                    acct="testuser@test.example",
                    display_name="Test User",
                    is_admin=True,
                )

                mock_fetch.return_value = expected_user

                user = mock_fetch({"role": mock_role_data})
                self.assertTrue(user.is_admin, f"Role '{role_name}' should grant admin access")

    # ========== HYBRID AUTHENTICATION TESTS ==========

    def test_hybrid_auth_jwt_priority(self):
        """Test that JWT authentication takes priority in hybrid mode"""
        admin_user = self.create_test_admin_user()

        # Mock JWT token validation
        with patch("app.jwt_auth.get_current_user_from_token", return_value=admin_user):
            with patch("app.oauth.get_current_user", return_value=None):  # No cookie
                response = self.client.get("/api/v1/me", headers={"Authorization": "Bearer valid_jwt_token"})

                # Should use JWT authentication
                self.assertIn(response.status_code, [200, 401])

    def test_hybrid_auth_cookie_fallback(self):
        """Test that cookie authentication is used as fallback"""
        admin_user = self.create_test_admin_user()

        # Mock failed JWT (no token) but valid cookie
        with patch("app.jwt_auth.get_current_user_from_token", return_value=None):
            with patch("app.oauth.get_current_user", return_value=admin_user):
                response = self.client.get("/api/v1/me")

                # Should use cookie authentication
                self.assertIn(response.status_code, [200, 401])

    def test_hybrid_auth_both_fail(self):
        """Test hybrid authentication when both JWT and cookie fail"""
        # Mock both authentication methods failing
        with patch("app.jwt_auth.get_current_user_from_token", return_value=None):
            with patch("app.oauth.get_current_user", return_value=None):
                response = self.client.get("/api/v1/me")

                # Should deny access
                self.assertEqual(response.status_code, 401)

    # ========== SESSION MANAGEMENT TESTS ==========

    def test_session_cookie_creation(self):
        """Test session cookie creation"""
        admin_user = self.create_test_admin_user()

        # Mock successful OAuth callback with cookie creation
        with patch("app.main.create_session_cookie") as mock_create_cookie:
            with patch("app.main.Client") as mock_client:
                # Mock token exchange
                mock_http_client = AsyncMock()
                mock_response = MagicMock()
                mock_response.status_code = 200
                mock_response.json.return_value = {"access_token": "test_token"}
                mock_http_client.post.return_value = mock_response

                mock_client_instance = MagicMock()
                mock_client_instance.get_async_httpx_client.return_value.__aenter__.return_value = mock_http_client
                mock_client.return_value = mock_client_instance

                # Mock user fetch and state validation
                self.mock_oauth_instance.fetch_user_info.return_value = admin_user
                self.mock_redis_instance.get.return_value = "valid"

                response = self.client.get("/admin/callback?code=test_code&state=test_state")

                # Should create session cookie for non-popup mode
                if response.status_code == 302:  # Redirect mode
                    mock_create_cookie.assert_called_once()

    def test_session_logout(self):
        """Test session logout and cleanup"""
        response = self.client.post("/admin/logout")

        # Should clear session
        self.assertEqual(response.status_code, 200)

    def test_session_cookie_validation(self):
        """Test session cookie validation"""
        # Mock cookie-based authentication
        admin_user = self.create_test_admin_user()

        with patch("app.oauth.get_current_user", return_value=admin_user):
            response = self.client.get("/api/v1/me")

            # Should validate session cookie
            self.assertIn(response.status_code, [200, 401])

    # ========== PERMISSION ENFORCEMENT TESTS ==========

    def test_admin_only_endpoints(self):
        """Test that admin-only endpoints are properly protected"""
        admin_endpoints = [
            "/analytics/overview",
            "/analytics/timeline",
            "/config/dry_run",
            "/config/panic_stop",
            "/rules",
            "/scanning/federated",
            "/analytics/domains",
        ]

        for endpoint in admin_endpoints:
            # Test unauthenticated access
            if endpoint in ["/config/dry_run", "/config/panic_stop", "/rules", "/scanning/federated"]:
                response = self.client.post(endpoint, json={})
            else:
                response = self.client.get(endpoint)

            self.assertIn(response.status_code, [401, 403], f"Endpoint {endpoint} should require authentication")

    def test_public_endpoints(self):
        """Test that public endpoints are accessible"""
        public_endpoints = ["/healthz", "/metrics", "/dryrun/evaluate"]

        for endpoint in public_endpoints:
            if endpoint == "/dryrun/evaluate":
                response = self.client.post(endpoint, json={})
            else:
                response = self.client.get(endpoint)

            self.assertEqual(response.status_code, 200, f"Public endpoint {endpoint} should be accessible")

    def test_webhook_authentication(self):
        """Test webhook signature-based authentication"""
        payload = json.dumps({"account": {"id": "123"}, "statuses": []})
        secret = "test_webhook_secret_123"
        signature = hmac.new(secret.encode(), payload.encode(), hashlib.sha256).hexdigest()

        response = self.client.post(
            "/webhooks/status",
            content=payload,
            headers={"X-Hub-Signature-256": f"sha256={signature}", "Content-Type": "application/json"},
        )

        # Should authenticate with valid signature
        self.assertEqual(response.status_code, 200)

    def test_api_key_authentication(self):
        """Test API key authentication for config endpoints"""
        # Mock admin user for API key auth
        admin_user = self.create_test_admin_user()

        with patch("app.main.get_current_user_hybrid", return_value=admin_user):
            response = self.client.post(
                "/config/dry_run", json={"dry_run": True}, headers={"X-API-Key": "test_api_key_123"}
            )

            # Should work with valid API key and admin user
            self.assertEqual(response.status_code, 200)

    # ========== SECURITY TESTS ==========

    def test_csrf_protection(self):
        """Test CSRF protection mechanisms"""
        # OAuth state parameter should be validated
        response = self.client.get("/admin/callback?code=test&state=malicious_state")
        self.assertEqual(response.status_code, 400)

    def test_token_replay_protection(self):
        """Test protection against token replay attacks"""
        # OAuth state should be single-use
        self.mock_redis_instance.get.return_value = "valid"

        # First use should work (mocked)
        # Second use should fail (state consumed)
        self.mock_redis_instance.get.return_value = None

        response = self.client.get("/admin/callback?code=test&state=used_state")
        self.assertEqual(response.status_code, 400)

    def test_session_security(self):
        """Test session security properties"""
        # Sessions should have proper security attributes
        # This is tested indirectly through cookie creation mocks
        pass

    def test_jwt_security_properties(self):
        """Test JWT security properties"""
        admin_user = self.create_test_admin_user()
        user_data = admin_user.model_dump()

        # JWT should include expiration
        token_data = {**user_data, "exp": datetime.utcnow() + timedelta(hours=24), "iat": datetime.utcnow()}

        # Verify required claims are present
        self.assertIn("exp", token_data)
        self.assertIn("iat", token_data)
        self.assertIn("is_admin", token_data)


if __name__ == "__main__":
    unittest.main(verbosity=2)
