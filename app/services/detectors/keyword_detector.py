from typing import List, Dict, Any

from app.services.detectors.base import BaseDetector
from app.schemas import Violation, Evidence


class KeywordDetector(BaseDetector):
    def evaluate(self, account_data: Dict[str, Any], statuses: List[Dict[str, Any]]) -> List[Violation]:
        violations: List[Violation] = []

        # In a real scenario, RuleService would provide the specific rule to evaluate
        # For now, we'll hardcode some example patterns
        example_rules = [
            {"name": "Keyword Spam", "pattern": "buy now,free money", "target_field": "content"},
            {"name": "Keyword Username", "pattern": "admin,support", "target_field": "username"},
        ]

        u = account_data.get("username") or (account_data.get("acct", "").split("@")[0]) or ""
        dn = account_data.get("display_name") or ""

        for rule in example_rules:
            terms = [term.strip() for term in rule["pattern"].split(",")]
            matched_terms = []
            
            if rule["target_field"] == "username":
                target_text = u
            elif rule["target_field"] == "display_name":
                target_text = dn
            else: # Default to content
                target_text = ""

            if target_text:
                for term in terms:
                    if term.lower() in target_text.lower():
                        matched_terms.append(term)
            
            if matched_terms:
                violations.append(
                    Violation(
                        rule_name=rule["name"],
                        score=1.0, # Placeholder score
                        evidence=Evidence(
                            matched_terms=matched_terms,
                            matched_status_ids=[],
                            metrics={f"{rule["target_field"]}": target_text}
                        )
                    )
                )

        for s in statuses or []:
            content = s.get("content", "")
            for rule in example_rules:
                if rule["target_field"] == "content":
                    terms = [term.strip() for term in rule["pattern"].split(",")]
                    matched_terms = []
                    for term in terms:
                        if term.lower() in content.lower():
                            matched_terms.append(term)
                    
                    if matched_terms:
                        violations.append(
                            Violation(
                                rule_name=rule["name"],
                                score=1.0, # Placeholder score
                                evidence=Evidence(
                                    matched_terms=matched_terms,
                                    matched_status_ids=[s.get("id")],
                                    metrics={"content": content}
                                )
                            )
                        )

        return violations
