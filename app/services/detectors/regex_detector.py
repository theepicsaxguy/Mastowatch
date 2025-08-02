import re
from typing import List, Dict, Any

from app.services.detectors.base import BaseDetector
from app.schemas import Violation, Evidence
from app.models import Rule


class RegexDetector(BaseDetector):
    def evaluate(self, rule: Rule, account_data: Dict[str, Any], statuses: List[Dict[str, Any]]) -> List[Violation]:
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
