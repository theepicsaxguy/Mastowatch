import re
from typing import List, Dict, Any

from app.services.detectors.base import BaseDetector
from app.schemas import Violation, Evidence


class RegexDetector(BaseDetector):
    def evaluate(self, rule: Any, account_data: Dict[str, Any], statuses: List[Dict[str, Any]]) -> List[Violation]:
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
            violations: List[Violation] = []

        u = account_data.get("username") or (account_data.get("acct", "").split("@")[0]) or ""
        dn = account_data.get("display_name") or ""

        # Apply regex to username
        if re.search(rule.pattern, u, re.I):
            violations.append(
                Violation(
                    rule_name=rule.name,
                    score=rule.weight,
                    evidence=Evidence(
                        matched_terms=[u],
                        matched_status_ids=[],
                        metrics={"username": u}
                    )
                )
            )

        # Apply regex to display name
        if re.search(rule.pattern, dn, re.I):
            violations.append(
                Violation(
                    rule_name=rule.name,
                    score=rule.weight,
                    evidence=Evidence(
                        matched_terms=[dn],
                        matched_status_ids=[],
                        metrics={"display_name": dn}
                    )
                )
            )
        
        # Apply regex to status content
        for s in statuses or []:
            content = s.get("content", "")
            if re.search(rule.pattern, content, re.I):
                violations.append(
                    Violation(
                        rule_name=rule.name,
                        score=rule.weight,
                        evidence=Evidence(
                            matched_terms=[content],
                            matched_status_ids=[s.get("id")],
                            metrics={"content": content}
                        )
                    )
                )

        return violations

        for rule in example_rules:
            if re.search(rule["pattern"], rule["target"], re.I):
                violations.append(
                    Violation(
                        rule_name=rule["name"],
                        score=1.0, # Placeholder score, will be based on rule.weight later
                        evidence=Evidence(
                            matched_terms=[rule["target"]],
                            matched_status_ids=[],
                            metrics={f"{rule["type"]}": rule["target"]}
                        )
                    )
                )
        
        for s in statuses or []:
            content = s.get("content", "")
            content_rule = {"name": "Content Spam", "pattern": ".*(send.*bitcoin|free.*crypto).*", "target": content, "type": "content", "status_id": s.get("id")}
            if re.search(content_rule["pattern"], content_rule["target"], re.I):
                violations.append(
                    Violation(
                        rule_name=content_rule["name"],
                        score=1.0, # Placeholder score
                        evidence=Evidence(
                            matched_terms=[content_rule["target"]],
                            matched_status_ids=[content_rule["status_id"]],
                            metrics={f"{content_rule["type"]}": content_rule["target"]}
                        )
                    )
                )

        return violations
