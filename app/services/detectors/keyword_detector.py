from typing import List, Dict, Any

from app.services.detectors.base import BaseDetector
from app.schemas import Violation, Evidence


class KeywordDetector(BaseDetector):
    def evaluate(self, rule: Any, account_data: Dict[str, Any], statuses: List[Dict[str, Any]]) -> List[Violation]:
        violations: List[Violation] = []

        terms = [term.strip() for term in rule.pattern.split(",")]
        matched_terms = []
            
        u = account_data.get("username") or (account_data.get("acct", "").split("@")[0]) or ""
        dn = account_data.get("display_name") or ""

        target_text = ""
        if rule.target_field == "username":
            target_text = u
        elif rule.target_field == "display_name":
            target_text = dn
        elif rule.target_field == "content":
            # For content, we iterate through statuses
            pass

        if target_text:
            for term in terms:
                if term.lower() in target_text.lower():
                    matched_terms.append(term)
            
            if matched_terms:
                violations.append(
                    Violation(
                        rule_name=rule.name,
                        score=rule.weight,
                        evidence=Evidence(
                            matched_terms=matched_terms,
                            matched_status_ids=[],
                            metrics={f"{rule.target_field}": target_text}
                        )
                    )
                )

        if rule.target_field == "content":
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
