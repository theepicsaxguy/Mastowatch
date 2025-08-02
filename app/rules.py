import hashlib
import re
from typing import Any, Dict, List, Tuple

import yaml


class Rules:
    def __init__(self, config: Dict[str, Any], ruleset_sha256: str):
        self.cfg = config
        self.ruleset_sha256 = ruleset_sha256

    @staticmethod
    def from_yaml(path="rules.yml"):
        with open(path, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f) or {}
        with open(path, "rb") as f:
            ruleset_sha256 = hashlib.sha256(f.read()).hexdigest()
        return Rules(config, ruleset_sha256)

    def eval_account(
        self, acct: Dict[str, Any], statuses: List[Dict[str, Any]]
    ) -> Tuple[float, List[Tuple[str, float, dict]]]:
        hits, score = [], 0.0
        u = acct.get("username") or (acct.get("acct", "").split("@")[0]) or ""
        dn = acct.get("display_name") or ""
        for rule in self.cfg.get("username_regex", []):
            if re.search(rule["pattern"], u, re.I):
                hits.append((f"username_regex/{rule['name']}", float(rule["weight"]), {"username": u}))
                score += float(rule["weight"])
        for rule in self.cfg.get("display_name_regex", []):
            if re.search(rule["pattern"], dn, re.I):
                hits.append((f"display_name_regex/{rule['name']}", float(rule["weight"]), {"display_name": dn}))
                score += float(rule["weight"])
        for s in statuses or []:
            content = s.get("content", "")
            for rule in self.cfg.get("content_regex", []):
                if re.search(rule["pattern"], content, re.I):
                    hits.append((f"content_regex/{rule['name']}", float(rule["weight"]), {"status_id": s.get("id")}))
                    score += float(rule["weight"])
        return score, hits
