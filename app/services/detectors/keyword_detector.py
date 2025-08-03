from typing import List, Dict, Any

from app.services.detectors.base import BaseDetector
from app.schemas import Violation, Evidence
from app.models import Rule


class KeywordDetector(BaseDetector):
    def evaluate(self, rule: Rule, account_data: Dict[str, Any], statuses: List[Dict[str, Any]]) -> List[Violation]:
        violations: List[Violation] = []

        terms = [term.strip() for term in rule.pattern.split(",")]
        u = account_data.get("username") or (account_data.get("acct", "").split("@")[0]) or ""
        dn = account_data.get("display_name") or ""

        # Check username for keywords
        matched_terms_username = []
        for term in terms:
            if term.lower() in u.lower():
                matched_terms_username.append(term)
        
        if matched_terms_username:
            violations.append(
                Violation(
                    rule_name=rule.name,
                    score=rule.weight,
                    evidence=Evidence(
                        matched_terms=matched_terms_username,
                        matched_status_ids=[],
                        metrics={"username": u}
                    )
                )
            )

        # Check display name for keywords
        matched_terms_display = []
        for term in terms:
            if term.lower() in dn.lower():
                matched_terms_display.append(term)
        
        if matched_terms_display:
            violations.append(
                Violation(
                    rule_name=rule.name,
                    score=rule.weight,
                    evidence=Evidence(
                        matched_terms=matched_terms_display,
                        matched_status_ids=[],
                        metrics={"display_name": dn}
                    )
                )
            )

        # Check content for keywords
        for s in statuses or []:
            content = s.get("content", "")
            matched_terms_content = []
            for term in terms:
                if term.lower() in content.lower():
                    matched_terms_content.append(term)
            
            if matched_terms_content:
                violations.append(
                    Violation(
                        rule_name=rule.name,
                        score=rule.weight,
                        evidence=Evidence(
                            matched_terms=matched_terms_content,
                            matched_status_ids=[s.get("id")],
                            metrics={"content": content}
                        )
                    )
                )

        return violations
