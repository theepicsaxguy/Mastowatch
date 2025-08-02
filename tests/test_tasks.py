import sys
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

# Add the app directory to the path so we can import the app modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.tasks.jobs import analyze_and_maybe_report


class TestCeleryTasks(unittest.TestCase):

    @patch("app.tasks.jobs.SessionLocal")
    @patch("app.tasks.jobs.rules")
    @patch("app.tasks.jobs.get_settings")
    def test_analyze_and_maybe_report_dry_run(self, mock_settings, mock_rules, mock_db):
        """Test analyze_and_maybe_report in dry run mode"""
        # Setup mocks
        mock_settings.return_value.DRY_RUN = True
        mock_settings.return_value.PANIC_STOP = False
        mock_rules.eval_account.return_value = (0.8, ["rule1", "rule2"])

        mock_db_session = MagicMock()
        mock_db.return_value.__enter__.return_value = mock_db_session

        # Test data
        payload = {
            "account": {"id": "123456", "acct": "suspicious@example.com", "domain": "example.com"},
            "statuses": [{"id": "status1", "content": "spam content"}],
        }

        # Call the function
        result = analyze_and_maybe_report(payload)

        # Assertions
        self.assertIsNotNone(result)
        mock_rules.eval_account.assert_called_once()

        # Verify that account and analysis records would be created/updated
        self.assertTrue(mock_db_session.merge.called)

        # In dry run mode, should not actually submit reports
        # (This would require mocking the Mastodon client as well)

    @patch("app.tasks.jobs.SessionLocal")
    @patch("app.tasks.jobs.rules")
    @patch("app.tasks.jobs.get_settings")
    def test_analyze_and_maybe_report_panic_stop(self, mock_settings, mock_rules, mock_db):
        """Test that panic stop prevents execution"""
        # Setup mocks
        mock_settings.return_value.PANIC_STOP = True

        # Test data
        payload = {"account": {"id": "123456"}, "statuses": []}

        # Call the function
        result = analyze_and_maybe_report(payload)

        # Should exit early due to panic stop
        mock_rules.eval_account.assert_not_called()
        mock_db.assert_not_called()

    def test_analyze_and_maybe_report_invalid_payload(self):
        """Test handling of invalid payload"""
        # Test with missing account
        result = analyze_and_maybe_report({})

        # Should handle gracefully
        self.assertIsNone(result)

        # Test with invalid account data
        result = analyze_and_maybe_report({"account": None})
        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()
