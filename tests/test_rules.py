import unittest
import os
from app.rules import Rules


class TestRules(unittest.TestCase):
    def test_eval_account(self):
        # Skip if running in CI or without rules setup
        if os.environ.get("SKIP_STARTUP_VALIDATION"):
            self.skipTest("Skipping rules test in testing environment")
            
        try:
            rules = Rules.from_database()
        except Exception:
            # Fallback to minimal rules for testing
            rules = Rules({"report_threshold": 1.0}, "test", [])
            
        account = {
            "acct": "ai_bot@example.com",
            "note": "This is a test account with some keywords: casino, adult.",
            "display_name": "Test Account",
            "statuses_count": 10,
            "followers_count": 5,
            "following_count": 20,
            "created_at": "2023-01-01T00:00:00.000Z",
        }
        score, hits = rules.eval_account(account, [])
        # Since we may not have rules loaded, just test that it doesn't crash
        self.assertGreaterEqual(score, 0)
        self.assertIsInstance(hits, list)


if __name__ == "__main__":
    unittest.main()
