import hashlib
import re
from typing import Any, Dict, List, Tuple, Optional

import yaml
from sqlalchemy.orm import Session

from app.db import engine
from app.models import Rule


class Rules:
    def __init__(self, config: Dict[str, Any], ruleset_sha256: str, db_rules: Optional[List[Rule]] = None):
        self.cfg = config
        self.ruleset_sha256 = ruleset_sha256
        self.db_rules = db_rules or []

    @staticmethod
    def from_yaml(path="rules.yml"):
        with open(path, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f) or {}
        with open(path, "rb") as f:
            ruleset_sha256 = hashlib.sha256(f.read()).hexdigest()
        
        # Load database rules
        with Session(engine) as session:
            db_rules = session.query(Rule).all()
        
        return Rules(config, ruleset_sha256, db_rules)

    def get_all_rules(self) -> Dict[str, List[Dict[str, Any]]]:
        """Get combined rules from file and database"""
        all_rules = {
            "username_regex": [],
            "display_name_regex": [],
            "content_regex": []
        }
        
        # Add file-based rules (marked as default)
        for rule_type in all_rules.keys():
            if rule_type in self.cfg:
                for rule in self.cfg[rule_type]:
                    all_rules[rule_type].append({
                        **rule,
                        "enabled": True,
                        "is_default": True,
                        "id": None
                    })
        
        # Add database rules
        for rule in self.db_rules:
            if rule.enabled and rule.rule_type in all_rules:
                all_rules[rule.rule_type].append({
                    "name": rule.name,
                    "pattern": rule.pattern,
                    "weight": float(rule.weight),
                    "enabled": rule.enabled,
                    "is_default": rule.is_default,
                    "id": rule.id
                })
        
        return all_rules

    def eval_account(
        self, acct: Dict[str, Any], statuses: List[Dict[str, Any]]
    ) -> Tuple[float, List[Tuple[str, float, dict]]]:
        hits, score = [], 0.0
        u = acct.get("username") or (acct.get("acct", "").split("@")[0]) or ""
        dn = acct.get("display_name") or ""
        
        all_rules = self.get_all_rules()
        
        for rule in all_rules.get("username_regex", []):
            if rule["enabled"] and re.search(rule["pattern"], u, re.I):
                hits.append((f"username_regex/{rule['name']}", float(rule["weight"]), {"username": u}))
                score += float(rule["weight"])
                
        for rule in all_rules.get("display_name_regex", []):
            if rule["enabled"] and re.search(rule["pattern"], dn, re.I):
                hits.append((f"display_name_regex/{rule['name']}", float(rule["weight"]), {"display_name": dn}))
                score += float(rule["weight"])
                
        for s in statuses or []:
            content = s.get("content", "")
            for rule in all_rules.get("content_regex", []):
                if rule["enabled"] and re.search(rule["pattern"], content, re.I):
                    hits.append((f"content_regex/{rule['name']}", float(rule["weight"]), {"status_id": s.get("id")}))
                    score += float(rule["weight"])
                    
        return score, hits
