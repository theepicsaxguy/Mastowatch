import re
from typing import List, Dict, Any

from app.services.detectors.base import BaseDetector
from app.schemas import Violation, Evidence


class RegexDetector(BaseDetector):
    def evaluate(self, account_data: Dict[str, Any], statuses: List[Dict[str, Any]]) -> List[Violation]:
        violations: List[Violation] = []
        
        # For simplicity, assume rules are passed in or fetched internally for now.
        # In a later step, RuleService will pass the relevant rule.
        # For now, we'll simulate a rule structure.
        
        # Example rule structure (will come from DB in RuleService)
        # rule = {
        #     "name": "Example Regex Rule",
        #     "pattern": ".*test.*",
        #     "detector_type": "regex",
        #     "trigger_threshold": 0.5
        # }

        # Placeholder for actual rule fetching/passing
        # For now, we'll just use the logic from the old rules.py
        # This will be refactored in Task 2.3

        # Extract relevant data from account_data and statuses
        u = account_data.get("username") or (account_data.get("acct", "").split("@")[0]) or ""
        dn = account_data.get("display_name") or ""

        # Simulate fetching rules for this detector type
        # In a real scenario, RuleService would provide the specific rule to evaluate
        # For now, we'll hardcode some example patterns based on the old rules.py
        example_rules = [
            {"name": "Username Spam", "pattern": ".*bot.*\\d{3,}$",