"""
Test utilities for MastoWatch testing
"""

from unittest.mock import patch

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


def create_mock_regular_user():
    """Create a mock regular user for testing"""
    return User(
        id="test_user_456",
        username="testuser",
        acct="testuser@test.example",
        display_name="Test User",
        is_admin=False,
        avatar=None,
    )


def mock_require_admin(admin_user=None):
    """
    Context manager to mock require_admin dependency
    Usage:
        with mock_require_admin():
            # admin_user is mocked as authenticated admin
    """
    if admin_user is None:
        admin_user = create_mock_admin_user()
    return patch("app.main.require_admin", return_value=admin_user)


def mock_get_current_user(user=None):
    """
    Context manager to mock get_current_user dependency
    Usage:
        with mock_get_current_user():
            # user is mocked as authenticated
    """
    if user is None:
        user = create_mock_admin_user()
    return patch("app.main.get_current_user", return_value=user)
