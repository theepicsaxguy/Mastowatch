import re, yaml, hashlib
from typing import Dict, Any, List, Tuple
from threading import RLock

class Rules:
    def __init__(self, path="rules.yml"):
        self.path = path
        self.lock = RLock()
        self._load()

    def _load(self):
        with open(self.path, "r", encoding="utf-8") as f:
            self.cfg = yaml.safe_load(f) or {}
        with open(self.path, "rb") as f:
            self.ruleset_sha256 = hashlib.sha256(f.read()).hexdigest()

    def reload(self):
        with self.lock:
            self._load()

    def eval_account(self, acct: Dict[str, Any], statuses: List[Dict[str,Any]]) -> Tuple[float, List[Tuple[str,float,dict]]]:
        hits, score = [], 0.0
        u = (acct.get("username") or "")
        dn = (acct.get("display_name") or "")
        for rule in self.cfg.get("username_regex", []):
            if re.search(rule["pattern"], u, re.I):
                hits.append((f"username_regex/{rule['name']}", float(rule["weight"]), {"username":u}))
                score += float(rule["weight"])
        for rule in self.cfg.get("display_name_regex", []):
            if re.search(rule["pattern"], dn, re.I):
                hits.append((f"display_name_regex/{rule['name']}", float(rule["weight"]), {"display_name":dn}))
                score += float(rule["weight"])
        for s in statuses or []:
            content = s.get("content","")
            for rule in self.cfg.get("content_regex", []):
                if re.search(rule["pattern"], content, re.I):
                    hits.append((f"content_regex/{rule['name']}", float(rule["weight"]), {"status_id":s.get("id")}))
                    score += float(rule["weight"])
        return score, hits
