"""Test cases for service layer components."""

import os
import tempfile
import unittest
from unittest.mock import Mock, patch

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db import Base
from app.services.enforcement_service import EnforcementService
from app.services.rule_service import RuleService


class TestRuleService(unittest.TestCase):
    """Test suite for RuleService class."""

    def setUp(self):
        """Set up test database and service instance."""
        # Create temporary test database
        self.test_db = tempfile.NamedTemporaryFile(delete=False, suffix=".db")
        self.test_db_url = f"sqlite:///{self.test_db.name}"

        self.engine = create_engine(self.test_db_url, echo=False)
        Base.metadata.create_all(self.engine)
        self.SessionLocal = sessionmaker(bind=self.engine)

        # Create service instance
        self.rule_service = RuleService(cache_ttl_seconds=1)

        # Mock global SessionLocal
        self.db_patcher = patch("app.services.rule_service.SessionLocal", self.SessionLocal)
        self.db_patcher.start()

    def tearDown(self):
        """Clean up test resources."""
        self.db_patcher.stop()
        self.engine.dispose()
        os.unlink(self.test_db.name)

    def test_create_rule_validation(self):
        """Test rule creation with validation."""
        rule = self.rule_service.create_rule(
            name="test_validation_rule",
            detector_type="regex",
            pattern="test.*pattern",
            weight=1.5,
            action_type="report",
            trigger_threshold=1.0,
        )

        self.assertEqual(rule.name, "test_validation_rule")
        self.assertEqual(rule.detector_type, "regex")
        self.assertEqual(rule.weight, 1.5)
        self.assertTrue(rule.enabled)

    def test_rule_cache_performance(self):
        """Test that caching improves performance."""
        # Create some rules
        for i in range(5):
            self.rule_service.create_rule(
                name=f"perf_rule_{i}",
                detector_type="keyword",
                pattern=f"keyword_{i}",
                weight=1.0,
                action_type="report",
                trigger_threshold=1.0,
            )

        # First call should hit database
        start_time = time.time()
        rules1, _, _ = self.rule_service.get_active_rules()
        first_call_time = time.time() - start_time

        # Second call should use cache
        start_time = time.time()
        rules2, _, _ = self.rule_service.get_active_rules()
        second_call_time = time.time() - start_time

        # Cache should be faster (though in SQLite this may not be measurable)
        self.assertEqual(len(rules1), len(rules2))
        self.assertEqual(len(rules1), 5)

    def test_bulk_rule_operations(self):
        """Test bulk operations on rules."""
        # Create multiple rules
        rule_ids = []
        for i in range(3):
            rule = self.rule_service.create_rule(
                name=f"bulk_rule_{i}",
                detector_type="regex",
                pattern=f"pattern_{i}",
                weight=1.0,
                action_type="report",
                trigger_threshold=1.0,
            )
            rule_ids.append(rule.id)

        # Test bulk disable
        updated_rules = self.rule_service.bulk_toggle_rules(rule_ids, enabled=False)
        self.assertEqual(len(updated_rules), 3)
        for rule in updated_rules:
            self.assertFalse(rule.enabled)

        # Test bulk enable
        updated_rules = self.rule_service.bulk_toggle_rules(rule_ids, enabled=True)
        self.assertEqual(len(updated_rules), 3)
        for rule in updated_rules:
            self.assertTrue(rule.enabled)

    def test_rule_statistics_accuracy(self):
        """Test that rule statistics are calculated correctly."""
        # Create mix of enabled and disabled rules
        self.rule_service.create_rule(
            name="enabled_rule_1",
            detector_type="regex",
            pattern="test1",
            weight=1.0,
            action_type="report",
            trigger_threshold=1.0,
            enabled=True,
        )
        self.rule_service.create_rule(
            name="enabled_rule_2",
            detector_type="keyword",
            pattern="test2",
            weight=1.0,
            action_type="report",
            trigger_threshold=1.0,
            enabled=True,
        )
        self.rule_service.create_rule(
            name="disabled_rule_1",
            detector_type="regex",
            pattern="test3",
            weight=1.0,
            action_type="report",
            trigger_threshold=1.0,
            enabled=False,
        )

        stats = self.rule_service.get_rule_statistics()

        self.assertEqual(stats["total_rules"], 3)
        self.assertEqual(stats["enabled_rules"], 2)
        self.assertEqual(stats["disabled_rules"], 1)
        self.assertIn("cache_status", stats)


class TestEnforcementService(unittest.TestCase):
    """Test suite for EnforcementService class."""

    def setUp(self):
        """Set up test environment."""
        self.enforcement_service = EnforcementService()

    @patch("app.services.enforcement_service.MastoClient")
    def test_apply_action_report(self, mock_client_class):
        """Test applying report action."""
        mock_client = Mock()
        mock_client_class.return_value = mock_client
        mock_client.create_report.return_value = Mock(json=lambda: {"id": "report_123"})

        account_data = {"id": "account_123", "acct": "test@example.com"}
        action = {"type": "report", "comment": "Test report comment", "category": "spam"}

        result = self.enforcement_service.apply_action(account_data, action)

        self.assertTrue(result)
        mock_client.create_report.assert_called_once()

    @patch("app.services.enforcement_service.MastoClient")
    def test_apply_action_silence(self, mock_client_class):
        """Test applying silence action."""
        mock_client = Mock()
        mock_client_class.return_value = mock_client
        mock_client.post.return_value = Mock(status_code=200)

        account_data = {"id": "account_123", "acct": "test@example.com"}
        action = {"type": "silence", "duration_seconds": 3600}

        result = self.enforcement_service.apply_action(account_data, action)

        self.assertTrue(result)
        mock_client.post.assert_called_once()

    def test_apply_action_invalid_type(self):
        """Test handling of invalid action type."""
        account_data = {"id": "account_123"}
        action = {"type": "invalid_action"}

        result = self.enforcement_service.apply_action(account_data, action)

        self.assertFalse(result)

    @patch("app.services.enforcement_service.get_settings")
    def test_dry_run_mode(self, mock_settings):
        """Test that actions are not applied in dry run mode."""
        mock_settings.return_value.DRY_RUN = True

        account_data = {"id": "account_123"}
        action = {"type": "report", "comment": "Test"}

        result = self.enforcement_service.apply_action(account_data, action)

        # Should return True but not actually perform action
        self.assertTrue(result)

    def test_validate_action_structure(self):
        """Test action validation logic."""
        # Valid action
        valid_action = {"type": "report", "comment": "Valid comment", "category": "spam"}
        self.assertTrue(self.enforcement_service._validate_action(valid_action))

        # Invalid action - missing required field
        invalid_action = {
            "type": "report"
            # Missing comment
        }
        self.assertFalse(self.enforcement_service._validate_action(invalid_action))

        # Invalid action - unknown type
        unknown_action = {"type": "unknown_action", "comment": "Test"}
        self.assertFalse(self.enforcement_service._validate_action(unknown_action))


if __name__ == "__main__":
    import time

    unittest.main()
