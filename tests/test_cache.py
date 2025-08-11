from datetime import datetime
from unittest.mock import MagicMock, patch

from fastapi.testclient import TestClient

from app.auth import require_api_key
from app.config import get_settings
from app.main import app
from app.oauth import require_admin_hybrid


def get_test_settings():
    settings = get_settings()
    settings.API_KEY = "test-api-key"
    return settings


app.dependency_overrides[get_settings] = get_test_settings

client = TestClient(app)


def mock_require_admin_hybrid():
    return type("User", (), {"username": "test_admin", "is_admin": True})()


app.dependency_overrides[require_admin_hybrid] = mock_require_admin_hybrid
app.dependency_overrides[require_api_key] = lambda: True


def test_invalidate_scan_cache_and_status():
    with patch("app.api.scanning.EnhancedScanningSystem") as MockScanner, patch(
        "app.api.scanning.SessionLocal"
    ) as MockSessionLocal:
        scanner_instance = MockScanner.return_value

        mock_db = MagicMock()
        query_total = MagicMock()
        query_total.scalar.return_value = 10
        query_needs = MagicMock()
        query_needs.filter.return_value.scalar.return_value = 2
        query_last = MagicMock()
        query_last.scalar.return_value = datetime(2024, 1, 1)
        mock_db.query.side_effect = [query_total, query_needs, query_last]

        session_context = MagicMock()
        session_context.__enter__.return_value = mock_db
        session_context.__exit__.return_value = None
        MockSessionLocal.return_value = session_context

        response = client.post(
            "/scanning/invalidate-cache",
            headers={"X-API-Key": "test-api-key", "Authorization": "Bearer test-admin-token"},
            params={"rule_changes": True},
        )
        assert response.status_code == 200
        assert response.json()["message"] == "Content cache invalidated"
        assert response.json()["rule_changes"] is True
        scanner_instance.invalidate_content_scans.assert_called_once_with(rule_changes=True, time_based=False)

        response = client.get(
            "/scanning/cache-status",
            headers={"X-API-Key": "test-api-key", "Authorization": "Bearer test-admin-token"},
        )
        data = response.json()
        assert response.status_code == 200
        assert data["total_cached_scans"] == 10
        assert data["needs_rescan"] == 2
        assert data["cache_hit_rate"] == 0.8
        assert data["last_scan"] == datetime(2024, 1, 1).isoformat()
