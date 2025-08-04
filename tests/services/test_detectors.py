"""Test cases for detector modules."""

import unittest
from unittest.mock import Mock

from app.schemas import Violation
from app.services.detectors.behavioral_detector import BehavioralDetector
from app.services.detectors.keyword_detector import KeywordDetector
from app.services.detectors.regex_detector import RegexDetector


class TestRegexDetector(unittest.TestCase):
    """Test suite for RegexDetector."""

    def setUp(self):
        """Set up test environment."""
        self.detector = RegexDetector()

    def test_evaluate_username_match(self):
        """Test regex matching in username field."""
        rule = Mock()
        rule.pattern = r"crypto|bitcoin|nft"
        rule.trigger_threshold = 1.0
        rule.name = "crypto_username_rule"
        rule.detector_type = "regex"
        rule.weight = 1.5

        account_data = {
            "username": "crypto_trader",
            "acct": "crypto_trader@example.com",
            "note": "Regular trading account",
        }
        statuses = []

        violations = self.detector.evaluate(rule, account_data, statuses)

        self.assertEqual(len(violations), 1)
        self.assertIsInstance(violations[0], Violation)
        self.assertEqual(violations[0].rule_name, "crypto_username_rule")
        self.assertEqual(violations[0].score, 1.5)
        self.assertIn("matched_pattern", violations[0].evidence)

    def test_evaluate_bio_match(self):
        """Test regex matching in bio/note field."""
        rule = Mock()
        rule.pattern = r"casino|gambling|poker"
        rule.trigger_threshold = 1.0
        rule.name = "gambling_bio_rule"
        rule.detector_type = "regex"
        rule.weight = 2.0

        account_data = {
            "username": "normal_user",
            "acct": "normal_user@example.com",
            "note": "I love playing poker and casino games!",
        }
        statuses = []

        violations = self.detector.evaluate(rule, account_data, statuses)

        self.assertEqual(len(violations), 1)
        self.assertEqual(violations[0].score, 2.0)
        self.assertIn("casino", violations[0].evidence["matched_pattern"])

    def test_evaluate_status_content_match(self):
        """Test regex matching in status content."""
        rule = Mock()
        rule.pattern = r"buy now|limited time|act fast"
        rule.trigger_threshold = 1.0
        rule.name = "spam_content_rule"
        rule.detector_type = "regex"
        rule.weight = 1.0

        account_data = {"username": "user", "note": "Normal bio"}
        statuses = [
            {"content": "Check out this amazing deal - buy now!", "id": "1"},
            {"content": "Regular post about daily life", "id": "2"},
            {"content": "Limited time offer - act fast!", "id": "3"},
        ]

        violations = self.detector.evaluate(rule, account_data, statuses)

        # Should find 2 matches
        self.assertEqual(len(violations), 2)
        for violation in violations:
            self.assertEqual(violation.score, 1.0)

    def test_evaluate_no_match(self):
        """Test when regex pattern doesn't match anything."""
        rule = Mock()
        rule.pattern = r"nonexistent_pattern_xyz"
        rule.trigger_threshold = 1.0
        rule.name = "no_match_rule"
        rule.detector_type = "regex"
        rule.weight = 1.0

        account_data = {"username": "user", "note": "Normal content"}
        statuses = [{"content": "Regular status", "id": "1"}]

        violations = self.detector.evaluate(rule, account_data, statuses)

        self.assertEqual(len(violations), 0)

    def test_evaluate_case_insensitive(self):
        """Test that regex matching is case-insensitive."""
        rule = Mock()
        rule.pattern = r"URGENT|urgent|Urgent"
        rule.trigger_threshold = 1.0
        rule.name = "case_test_rule"
        rule.detector_type = "regex"
        rule.weight = 1.0

        account_data = {"username": "user", "note": "This is URGENT business"}
        statuses = [{"content": "urgent message here", "id": "1"}]

        violations = self.detector.evaluate(rule, account_data, statuses)

        # Should match both URGENT and urgent
        self.assertEqual(len(violations), 2)


class TestKeywordDetector(unittest.TestCase):
    """Test suite for KeywordDetector."""

    def setUp(self):
        """Set up test environment."""
        self.detector = KeywordDetector()

    def test_evaluate_comma_separated_keywords(self):
        """Test keyword detection with comma-separated list."""
        rule = Mock()
        rule.pattern = "casino,adult,pills,viagra"
        rule.trigger_threshold = 1.0
        rule.name = "spam_keywords_rule"
        rule.detector_type = "keyword"
        rule.weight = 2.0

        account_data = {"username": "user", "note": "Visit our casino for adult entertainment"}
        statuses = [{"content": "Get cheap viagra pills online", "id": "1"}]

        violations = self.detector.evaluate(rule, account_data, statuses)

        # Should find multiple keyword matches
        self.assertGreater(len(violations), 0)
        for violation in violations:
            self.assertEqual(violation.score, 2.0)
            self.assertIn("matched_keywords", violation.evidence)

    def test_evaluate_single_keyword(self):
        """Test keyword detection with single keyword."""
        rule = Mock()
        rule.pattern = "scam"
        rule.trigger_threshold = 1.0
        rule.name = "scam_keyword_rule"
        rule.detector_type = "keyword"
        rule.weight = 3.0

        account_data = {"username": "user", "note": "This is a scam warning"}
        statuses = []

        violations = self.detector.evaluate(rule, account_data, statuses)

        self.assertEqual(len(violations), 1)
        self.assertEqual(violations[0].score, 3.0)
        self.assertIn("scam", violations[0].evidence["matched_keywords"])

    def test_evaluate_partial_word_match(self):
        """Test that keywords match as substrings."""
        rule = Mock()
        rule.pattern = "free"
        rule.trigger_threshold = 1.0
        rule.name = "free_keyword_rule"
        rule.detector_type = "keyword"
        rule.weight = 1.0

        account_data = {"username": "user", "note": "Enjoy freedom of speech"}
        statuses = []

        violations = self.detector.evaluate(rule, account_data, statuses)

        # Should match "free" within "freedom"
        self.assertEqual(len(violations), 1)

    def test_evaluate_no_keyword_match(self):
        """Test when no keywords are found."""
        rule = Mock()
        rule.pattern = "nonexistent,impossible,notfound"
        rule.trigger_threshold = 1.0
        rule.name = "no_keywords_rule"
        rule.detector_type = "keyword"
        rule.weight = 1.0

        account_data = {"username": "user", "note": "Normal content here"}
        statuses = [{"content": "Regular status update", "id": "1"}]

        violations = self.detector.evaluate(rule, account_data, statuses)

        self.assertEqual(len(violations), 0)


class TestBehavioralDetector(unittest.TestCase):
    """Test suite for BehavioralDetector."""

    def setUp(self):
        """Set up test environment."""
        self.detector = BehavioralDetector()

    def test_evaluate_high_posting_frequency(self):
        """Test detection of accounts with high posting frequency."""
        rule = Mock()
        rule.pattern = "high_frequency"
        rule.trigger_threshold = 1.0
        rule.name = "high_frequency_rule"
        rule.detector_type = "behavioral"
        rule.weight = 1.5

        account_data = {
            "username": "spammer",
            "statuses_count": 10000,
            "created_at": "2023-12-01T00:00:00.000Z",  # Recent account
        }
        # Many recent statuses
        statuses = [{"id": str(i), "content": f"Status {i}"} for i in range(50)]

        violations = self.detector.evaluate(rule, account_data, statuses)

        if "high_frequency" in rule.pattern:
            self.assertGreater(len(violations), 0)
            self.assertEqual(violations[0].score, 1.5)

    def test_evaluate_low_follower_ratio(self):
        """Test detection of accounts with suspicious follower ratios."""
        rule = Mock()
        rule.pattern = "low_follower_ratio"
        rule.trigger_threshold = 1.0
        rule.name = "follower_ratio_rule"
        rule.detector_type = "behavioral"
        rule.weight = 1.0

        account_data = {"username": "suspicious", "followers_count": 5, "following_count": 1000, "statuses_count": 500}
        statuses = []

        violations = self.detector.evaluate(rule, account_data, statuses)

        if "low_follower_ratio" in rule.pattern:
            self.assertGreater(len(violations), 0)

    def test_evaluate_new_account_high_activity(self):
        """Test detection of new accounts with high activity."""
        rule = Mock()
        rule.pattern = "new_account_high_activity"
        rule.trigger_threshold = 1.0
        rule.name = "new_account_rule"
        rule.detector_type = "behavioral"
        rule.weight = 2.0

        account_data = {
            "username": "newspammer",
            "created_at": "2024-01-01T00:00:00.000Z",  # Very recent
            "statuses_count": 1000,
        }
        statuses = []

        violations = self.detector.evaluate(rule, account_data, statuses)

        if "new_account_high_activity" in rule.pattern:
            self.assertGreater(len(violations), 0)

    def test_evaluate_normal_behavior(self):
        """Test that normal accounts don't trigger behavioral violations."""
        rule = Mock()
        rule.pattern = "high_frequency,low_follower_ratio,new_account_high_activity"
        rule.trigger_threshold = 1.0
        rule.name = "behavioral_checks"
        rule.detector_type = "behavioral"
        rule.weight = 1.0

        # Normal, established account
        account_data = {
            "username": "normal_user",
            "created_at": "2020-01-01T00:00:00.000Z",  # Old account
            "followers_count": 500,
            "following_count": 300,
            "statuses_count": 1000,
        }
        statuses = []

        violations = self.detector.evaluate(rule, account_data, statuses)

        # Normal account should not trigger violations
        self.assertEqual(len(violations), 0)

    def test_evaluate_invalid_behavioral_pattern(self):
        """Test handling of invalid behavioral pattern."""
        rule = Mock()
        rule.pattern = "invalid_pattern"
        rule.trigger_threshold = 1.0
        rule.name = "invalid_rule"
        rule.detector_type = "behavioral"
        rule.weight = 1.0

        account_data = {"username": "user"}
        statuses = []

        violations = self.detector.evaluate(rule, account_data, statuses)

        # Invalid pattern should not cause crashes
        self.assertEqual(len(violations), 0)


if __name__ == "__main__":
    unittest.main()
