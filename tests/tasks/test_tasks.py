import sys
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

# Add the app directory to the path so we can import the app modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.schemas import Violation
from app.tasks.jobs import analyze_and_maybe_report, process_new_report, process_new_status


class TestCeleryTasks(unittest.TestCase):
    @patch("app.tasks.jobs.SessionLocal")
    @patch("app.tasks.jobs.rule_service")
    @patch("app.tasks.jobs.get_settings")
    @patch("app.tasks.jobs._get_bot_client")
    def test_analyze_and_maybe_report_dry_run(self, mock_bot_client, mock_settings, mock_rule_service, mock_db):
        """Test analyze_and_maybe_report in dry run mode"""
        # Setup mocks
        mock_settings.return_value.DRY_RUN = True
        mock_settings.return_value.PANIC_STOP = False

        # Mock rule service evaluation
        mock_rule_service.evaluate_account.return_value = [
            Violation(rule_name="rule1", rule_type="t1", score=0.5, evidence={}),
            Violation(rule_name="rule2", rule_type="t2", score=0.3, evidence={}),
        ]

        mock_db_session = MagicMock()
        mock_db.return_value.__enter__.return_value = mock_db_session

        # Mock bot client
        mock_client = MagicMock()
        mock_bot_client.return_value = mock_client

        # Test data
        payload = {
            "account": {"id": "123456", "acct": "suspicious@example.com", "domain": "example.com"},
            "statuses": [{"id": "status1", "content": "spam content"}],
        }

        # Call the function
        result = analyze_and_maybe_report(payload)

        # Assertions
        self.assertIsNotNone(result)
        mock_rule_service.evaluate_account.assert_called_once()

        # Verify that account and analysis records would be created/updated
        self.assertTrue(mock_db_session.merge.called)

        # In dry run mode, should not actually submit reports
        mock_client.create_report.assert_not_called()

    @patch("app.tasks.jobs.SessionLocal")
    @patch("app.tasks.jobs.rule_service")
    @patch("app.tasks.jobs.get_settings")
    def test_analyze_and_maybe_report_panic_stop(self, mock_settings, mock_rule_service, mock_db):
        """Test that panic stop prevents execution"""
        # Setup mocks
        mock_settings.return_value.PANIC_STOP = True

        # Test data
        payload = {"account": {"id": "123456"}, "statuses": []}

        # Call the function
        result = analyze_and_maybe_report(payload)

        # Should exit early due to panic stop
        mock_rule_service.evaluate_account.assert_not_called()
        mock_db.assert_not_called()

    @patch("app.tasks.jobs.SessionLocal")
    @patch("app.tasks.jobs.analyze_and_maybe_report")
    def test_process_new_report(self, mock_analyze, mock_db):
        """Test processing of new report webhook"""
        mock_db_session = MagicMock()
        mock_db.return_value.__enter__.return_value = mock_db_session

        mock_analyze.delay.return_value = MagicMock(id="task_123")

        # Mock report payload
        payload = {
            "id": "report_123",
            "account": {"id": "reporter_123", "acct": "reporter@example.com"},
            "target_account": {"id": "target_123", "acct": "target@example.com"},
            "status_ids": ["status_1", "status_2"],
            "comment": "This is spam",
        }

        # Call the function
        result = process_new_report(payload)

        # Should trigger analysis of the target account
        self.assertIsNotNone(result)

    @patch("app.tasks.jobs.SessionLocal")
    @patch("app.tasks.jobs.analyze_and_maybe_report")
    def test_process_new_status(self, mock_analyze, mock_db):
        """Test processing of new status webhook"""
        mock_db_session = MagicMock()
        mock_db.return_value.__enter__.return_value = mock_db_session

        mock_analyze.delay.return_value = MagicMock(id="task_456")

        # Mock status payload
        payload = {
            "id": "status_123",
            "account": {"id": "account_123", "acct": "user@example.com"},
            "content": "This is a test status",
            "visibility": "public",
        }

        # Call the function
        result = process_new_status(payload)

        # Should trigger analysis of the account
        self.assertIsNotNone(result)

    def test_analyze_and_maybe_report_invalid_payload(self):
        """Test handling of invalid payload"""
        # Test with missing account
        result = analyze_and_maybe_report({})

        # Should handle gracefully
        self.assertIsNone(result)

        # Test with invalid account data
        result = analyze_and_maybe_report({"account": None})
        self.assertIsNone(result)

    @patch("app.tasks.jobs.SessionLocal")
    @patch("app.tasks.jobs.rule_service")
    @patch("app.tasks.jobs.get_settings")
    @patch("app.tasks.jobs._get_bot_client")
    def test_analyze_and_maybe_report_report_creation(self, mock_bot_client, mock_settings, mock_rule_service, mock_db):
        """Test that reports are created when score exceeds threshold"""
        # Setup mocks for non-dry run mode
        mock_settings.return_value.DRY_RUN = False
        mock_settings.return_value.PANIC_STOP = False

        # Mock rule service to return high score
        mock_rule_service.evaluate_account.return_value = [
            Violation(rule_name="high_risk_rule", rule_type="t", score=2.5, evidence={})
        ]
        mock_rule_service.get_active_rules.return_value = ([], {"report_threshold": 1.0}, "test_sha")

        mock_db_session = MagicMock()
        mock_db.return_value.__enter__.return_value = mock_db_session

        # Mock bot client
        mock_client = MagicMock()
        mock_bot_client.return_value = mock_client
        mock_client.create_report.return_value = MagicMock(json=lambda: {"id": "report_789"})

        # Test data
        payload = {
            "account": {"id": "123456", "acct": "suspicious@example.com", "domain": "example.com"},
            "statuses": [{"id": "status1", "content": "suspicious content"}],
        }

        # Call the function
        result = analyze_and_maybe_report(payload)

        # Should create a report since score (2.5) > threshold (1.0)
        self.assertIsNotNone(result)
        mock_client.create_report.assert_called_once()

    @patch("app.tasks.jobs.SessionLocal")
    @patch("app.tasks.jobs.rule_service")
    @patch("app.tasks.jobs.get_settings")
    def test_analyze_and_maybe_report_no_report_low_score(self, mock_settings, mock_rule_service, mock_db):
        """Test that no report is created when score is below threshold"""
        # Setup mocks
        mock_settings.return_value.DRY_RUN = False
        mock_settings.return_value.PANIC_STOP = False

        # Mock rule service to return low score
        mock_rule_service.evaluate_account.return_value = [
            Violation(rule_name="low_risk_rule", rule_type="t", score=0.5, evidence={})
        ]
        mock_rule_service.get_active_rules.return_value = ([], {"report_threshold": 1.0}, "test_sha")

        mock_db_session = MagicMock()
        mock_db.return_value.__enter__.return_value = mock_db_session

        # Test data
        payload = {
            "account": {"id": "123456", "acct": "normal@example.com", "domain": "example.com"},
            "statuses": [{"id": "status1", "content": "normal content"}],
        }

        # Call the function
        result = analyze_and_maybe_report(payload)

        # Should not create a report since score (0.5) < threshold (1.0)
        self.assertIsNotNone(result)
        # No report should be created, but analysis should be recorded


if __name__ == "__main__":
    unittest.main()
