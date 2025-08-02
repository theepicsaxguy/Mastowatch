from datetime import datetime, timedelta
from unittest.mock import patch

from fastapi.testclient import TestClient
from freezegun import freeze_time

from app.main import app
from app.config import get_settings

# Mock settings for testing
def get_test_settings():
    settings = get_settings()
    settings.REDIS_URL = "redis://localhost:6379/9"  # Use a separate Redis DB for testing
    settings.API_KEY = "test-api-key"
    return settings

app.dependency_overrides[get_settings] = get_test_settings

client = TestClient(app)


def test_invalidate_scan_cache_and_status():
    """Test cache invalidation and status reporting"""
    # Mock Redis client
    mock_redis_client = {}  # Simulate Redis store

    class MockRedis:
        def from_url(self, url, decode_responses):
            return self

        def setex(self, key, ttl, value):
            mock_redis_client[key] = value

        def get(self, key):
            return mock_redis_client.get(key)

    with patch("app.main.redis", new=MockRedis()):
        # 1. Call invalidate-cache endpoint
        response = client.post(
            "/scanning/invalidate-cache",
            headers={
                "X-API-Key": "test-api-key",
                "Authorization": "Bearer test-admin-token" # Mock admin auth
            },
            json={"rule_changes": True}
        )
        assert response.status_code == 200
        assert response.json()["message"] == "Scan cache invalidated successfully"
        assert response.json()["rule_changes"] == True
        assert response.json()["frontend_refresh_recommended"] == True

        # 2. Call cache-status immediately and assert refresh is needed
        response = client.get(
            "/scanning/cache-status",
            headers={
                "X-API-Key": "test-api-key",
                "Authorization": "Bearer test-admin-token" # Mock admin auth
            }
        )
        assert response.status_code == 200
        assert response.json()["cache_status"] == "invalidated"
        assert response.json()["refresh_recommended"] == True
        assert response.json()["last_invalidation"]["rule_changes"] == True

        # 3. Advance time by 6 minutes (360 seconds) - cache invalidation event expires after 300 seconds
        with freeze_time(datetime.utcnow() + timedelta(minutes=6)):
            response = client.get(
                "/scanning/cache-status",
                headers={
                    "X-API-Key": "test-api-key",
                    "Authorization": "Bearer test-admin-token" # Mock admin auth
                }
            )
            assert response.status_code == 200
            assert response.json()["cache_status"] == "valid"
            assert response.json()["refresh_recommended"] == False
            assert response.json()["last_invalidation"] is None


# Mock the require_admin_hybrid dependency for testing purposes
# This allows us to bypass actual authentication for unit tests
@app.dependency_overrides.setdefault("require_admin_hybrid", lambda: None)
def mock_require_admin_hybrid():
    return type("User", (object,), {"username": "test_admin", "is_admin": True})()


# Mock the get_db_session dependency for testing purposes
@app.dependency_overrides.setdefault("get_db_session", lambda: None)
def mock_get_db_session():
    class MockSession:
        def __enter__(self):
            return self
        def __exit__(self, exc_type, exc_val, exc_tb):
            pass
        def query(self, *args, **kwargs):
            return self
        def filter(self, *args, **kwargs):
            return self
        def first(self):
            return None
        def all(self):
            return []
        def execute(self, *args, **kwargs):
            return self
        def scalar_one_or_none(self):
            return None
        def commit(self):
            pass
        def rollback(self):
            pass
        def refresh(self, *args, **kwargs):
            pass
        def add(self, *args, **kwargs):
            pass
        def update(self, *args, **kwargs):
            pass

    return MockSession()
