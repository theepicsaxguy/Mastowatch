import unittest
from app.rules import Rules

class TestRules(unittest.TestCase):
    def test_eval_account(self):
        rules = Rules.from_yaml("rules.yml")
        account = {
            "acct": "ai_bot@example.com",
            "note": "This is a test account with some keywords: casino, adult.",
            "display_name": "Test Account",
            "statuses_count": 10,
            "followers_count": 5,
            "following_count": 20,
            "created_at": "2023-01-01T00:00:00.000Z"
        }
        score, hits = rules.eval_account(account, [])
        self.assertGreater(score, 0)
        self.assertGreater(len(hits), 0)
        self.assertTrue(any(h[0].endswith("/crypto1") for h in hits))

if __name__ == '__main__':
    unittest.main()
