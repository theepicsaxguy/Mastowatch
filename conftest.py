"""
CI/CD-friendly test configuration for Mastowatch
Uses SQLite in-memory database and bypasses authentication
"""

import os
import tempfile
import pytest
from unittest.mock import patch, MagicMock
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

# Set test environment variables before any app imports
os.environ.update({
    "SKIP_STARTUP_VALIDATION": "1", 
    "INSTANCE_BASE": "https://test.mastodon.social",
    "ADMIN_TOKEN": "test_admin_token",
    "BOT_TOKEN": "test_bot_token", 
    "REDIS_URL": "redis://localhost:6380/1",
    "DEFEDERATION_THRESHOLD": "10",
    "CONTENT_CACHE_TTL": "24",
    "FEDERATED_SCAN_ENABLED": "true",
    "DRY_RUN": "true",
    "OAUTH_CLIENT_ID": "test_client_id",
    "OAUTH_CLIENT_SECRET": "test_client_secret",
    "SESSION_SECRET_KEY": "test_session_key"
})

# Create temporary SQLite database for testing
test_db_file = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
test_db_path = f"sqlite:///{test_db_file.name}"
os.environ["DATABASE_URL"] = test_db_path

@pytest.fixture(scope="session")
def test_engine():
    """Create test database engine"""
    engine = create_engine(test_db_path, echo=False)
    return engine

@pytest.fixture(scope="session") 
def test_session_factory(test_engine):
    """Create test database session factory"""
    return sessionmaker(bind=test_engine)

@pytest.fixture(scope="function")
def test_db_session(test_session_factory):
    """Create test database session"""
    session = test_session_factory()
    try:
        yield session
    finally:
        session.close()

@pytest.fixture(scope="session")
def mock_redis():
    """Mock Redis for testing"""
    mock_redis = MagicMock()
    mock_redis.ping.return_value = True
    mock_redis.get.return_value = None
    mock_redis.setex.return_value = True
    return mock_redis

@pytest.fixture(scope="session")
def bypass_auth():
    """Bypass authentication for testing"""
    def mock_require_admin_hybrid():
        from app.oauth import User
        return User(
            id="test_admin",
            username="test_admin", 
            acct="test_admin@test.com",
            display_name="Test Admin",
            is_admin=True,
            avatar=None
        )
    
    with patch("app.main.require_admin_hybrid", side_effect=mock_require_admin_hybrid):
        yield

@pytest.fixture(scope="session")
def test_app():
    """Create test FastAPI app with mocked dependencies"""
    
    # Mock external dependencies before importing app
    with patch("redis.from_url") as mock_redis_factory:
        mock_redis_instance = MagicMock()
        mock_redis_instance.ping.return_value = True
        mock_redis_factory.return_value = mock_redis_instance
        
        with patch("app.main.SessionLocal") as mock_session_local:
            mock_session = MagicMock()
            mock_session_local.return_value.__enter__.return_value = mock_session
            
            # Mock Celery tasks
            with patch("app.main.scan_federated_content") as mock_federated:
                mock_federated.delay.return_value = MagicMock(id="test_task_123")
                
                with patch("app.main.check_domain_violations") as mock_domain_check:
                    mock_domain_check.delay.return_value = MagicMock(id="test_domain_task_123")
                    
                    # Mock enhanced scanning system
                    with patch("app.main.EnhancedScanningSystem") as mock_scanner_class:
                        mock_scanner = MagicMock()
                        mock_scanner.get_domain_alerts.return_value = []
                        mock_scanner.invalidate_content_scans.return_value = True
                        mock_scanner_class.return_value = mock_scanner
                        
                        # Import and create app after mocking
                        from app.main import app
                        yield app

@pytest.fixture(scope="session")
def test_client(test_app, bypass_auth):
    """Create test client with bypassed authentication"""
    return TestClient(test_app)

def pytest_configure(config):
    """Configure pytest"""
    # Add custom markers
    config.addinivalue_line("markers", "unit: mark test as unit test")
    config.addinivalue_line("markers", "integration: mark test as integration test")
    config.addinivalue_line("markers", "slow: mark test as slow running")

def pytest_unconfigure(config):
    """Cleanup after testing"""
    # Clean up test database file
    if os.path.exists(test_db_file.name):
        os.unlink(test_db_file.name)
