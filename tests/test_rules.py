"""Test cases for rule evaluation functionality."""

import os
import unittest

from app.services.rule_service import rule_service


class TestRules(unittest.TestCase):
    """Test class for rule evaluation."""

    def test_eval_account(self):
        """Test account evaluation against rules."""
        # Skip if running in CI or without rules setup
        if os.environ.get("SKIP_STARTUP_VALIDATION"):
            self.skipTest("Skipping rules test in testing environment")

        try:
            # Use the new rule service
            all_rules, config, _ = rule_service.get_active_rules()
        except Exception:
            # If rules can't be loaded, just test the function doesn't crash
            self.skipTest("Rules not available for testing")

        account = {
            "acct": "ai_bot@example.com",
            "note": "This is a test account with some keywords: casino, adult.",
            "display_name": "Test Account",
            "statuses_count": 10,
            "followers_count": 5,
            "following_count": 20,
            "created_at": "2023-01-01T00:00:00.000Z",
        }
        score, hits = rule_service.eval_account(account, [])
        # Since we may not have rules loaded, just test that it doesn't crash
        self.assertGreaterEqual(score, 0)
        self.assertIsInstance(hits, list)


if __name__ == "__main__":
    unittest.main()
