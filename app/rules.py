import hashlib
import re
from typing import Any, Dict, List, Tuple, Optional
from datetime import datetime

from sqlalchemy.orm import Session
from sqlalchemy import func, text

from app.db import engine
from app.models import Rule


class Rules:
    def __init__(self, config: Dict[str, Any], ruleset_sha256: str, db_rules: Optional[List[Rule]] = None):
        self.cfg = config
        self.ruleset_sha256 = ruleset_sha256
        self.db_rules = db_rules or []

    @staticmethod
    def from_database():
        """Load rules from database only"""
        with Session(engine) as session:
            db_rules = session.query(Rule).all()
            
            # Create a hash from all the rule data for versioning
            rule_data = []
            for rule in db_rules:
                rule_data.append(f"{rule.id}:{rule.pattern}:{rule.weight}:{rule.enabled}")
            
            ruleset_content = "|".join(sorted(rule_data))
            ruleset_sha256 = hashlib.sha256(ruleset_content.encode()).hexdigest()
            
            # Get report threshold from database config or use default
            config_row = session.execute(
                text("SELECT value FROM config WHERE key='report_threshold'")
            ).scalar()
            
            if config_row and isinstance(config_row, dict):
                report_threshold = config_row.get("threshold", 1.0)
            else:
                report_threshold = 1.0
            
            config = {"report_threshold": report_threshold}
        
        return Rules(config, ruleset_sha256, db_rules)

    def get_all_rules(self) -> Dict[str, List[Dict[str, Any]]]:
        """Get rules from database only with enhanced metadata"""
        all_rules = {
            "username_regex": [],
            "display_name_regex": [],
            "content_regex": []
        }
        
        # Add database rules with enhanced metadata
        for rule in self.db_rules:
            if rule.rule_type in all_rules:
                all_rules[rule.rule_type].append({
                    "name": rule.name,
                    "pattern": rule.pattern,
                    "weight": float(rule.weight),
                    "enabled": rule.enabled,
                    "is_default": rule.is_default,
                    "id": rule.id,
                    "trigger_count": rule.trigger_count or 0,
                    "last_triggered_at": rule.last_triggered_at.isoformat() if rule.last_triggered_at else None,
                    "last_triggered_content": rule.last_triggered_content,
                    "created_by": rule.created_by,
                    "updated_by": rule.updated_by,
                    "description": rule.description,
                    "created_at": rule.created_at.isoformat() if rule.created_at else None,
                    "updated_at": rule.updated_at.isoformat() if rule.updated_at else None
                })
        
        return all_rules

    def eval_account(
        self, acct: Dict[str, Any], statuses: List[Dict[str, Any]]
    ) -> Tuple[float, List[Tuple[str, float, dict]]]:
        """Enhanced account evaluation with rule tracking"""
        hits, score = [], 0.0
        u = acct.get("username") or (acct.get("acct", "").split("@")[0]) or ""
        dn = acct.get("display_name") or ""
        
        all_rules = self.get_all_rules()
        triggered_rules = []  # Track which rules were triggered for analytics
        
        for rule in all_rules.get("username_regex", []):
            if rule["enabled"] and re.search(rule["pattern"], u, re.I):
                hit_data = (f"username_regex/{rule['name']}", float(rule["weight"]), {"username": u})
                hits.append(hit_data)
                score += float(rule["weight"])
                triggered_rules.append({
                    "rule_id": rule.get("id"),
                    "rule_name": rule["name"],
                    "rule_type": "username_regex",
                    "matched_content": u
                })
                
        for rule in all_rules.get("display_name_regex", []):
            if rule["enabled"] and re.search(rule["pattern"], dn, re.I):
                hit_data = (f"display_name_regex/{rule['name']}", float(rule["weight"]), {"display_name": dn})
                hits.append(hit_data)
                score += float(rule["weight"])
                triggered_rules.append({
                    "rule_id": rule.get("id"),
                    "rule_name": rule["name"],
                    "rule_type": "display_name_regex",
                    "matched_content": dn
                })
                
        for s in statuses or []:
            content = s.get("content", "")
            for rule in all_rules.get("content_regex", []):
                if rule["enabled"] and re.search(rule["pattern"], content, re.I):
                    hit_data = (f"content_regex/{rule['name']}", float(rule["weight"]), {"status_id": s.get("id")})
                    hits.append(hit_data)
                    score += float(rule["weight"])
                    triggered_rules.append({
                        "rule_id": rule.get("id"),
                        "rule_name": rule["name"],
                        "rule_type": "content_regex",
                        "matched_content": content[:200],  # Truncate long content
                        "status_id": s.get("id")
                    })
        
        # Update rule statistics in database if rules were triggered
        if triggered_rules:
            self._update_rule_statistics(triggered_rules)
                    
        return score, hits

    def _update_rule_statistics(self, triggered_rules: List[Dict[str, Any]]):
        """Update rule trigger statistics in database"""
        try:
            with Session(engine) as session:
                now = datetime.utcnow()
                for rule_trigger in triggered_rules:
                    rule_id = rule_trigger.get("rule_id")
                    if rule_id:  # Only update DB rules, not file-based ones
                        rule = session.query(Rule).filter(Rule.id == rule_id).first()
                        if rule:
                            rule.trigger_count = (rule.trigger_count or 0) + 1
                            rule.last_triggered_at = now
                            rule.last_triggered_content = {
                                "matched_content": rule_trigger.get("matched_content"),
                                "status_id": rule_trigger.get("status_id"),
                                "triggered_at": now.isoformat()
                            }
                session.commit()
        except Exception as e:
            # Log error but don't fail the entire evaluation
            import logging
            logging.error(f"Failed to update rule statistics: {e}")

    def get_rule_statistics(self) -> Dict[str, Any]:
        """Get comprehensive rule statistics"""
        with Session(engine) as session:
            # Get overall stats
            total_rules = session.query(func.count(Rule.id)).scalar() or 0
            enabled_rules = session.query(func.count(Rule.id)).filter(Rule.enabled == True).scalar() or 0
            custom_rules = session.query(func.count(Rule.id)).filter(Rule.is_default == False).scalar() or 0
            
            # Get most triggered rules
            top_rules = (
                session.query(Rule.name, Rule.trigger_count, Rule.rule_type, Rule.last_triggered_at)
                .filter(Rule.trigger_count > 0)
                .order_by(Rule.trigger_count.desc())
                .limit(10)
                .all()
            )
            
            # Get recent activity
            recent_activity = (
                session.query(Rule.name, Rule.last_triggered_at, Rule.rule_type)
                .filter(Rule.last_triggered_at.isnot(None))
                .order_by(Rule.last_triggered_at.desc())
                .limit(5)
                .all()
            )
            
            return {
                "total_rules": total_rules,
                "enabled_rules": enabled_rules,
                "custom_rules": custom_rules,
                "file_rules": total_rules - custom_rules,
                "top_triggered_rules": [
                    {
                        "name": rule.name,
                        "trigger_count": rule.trigger_count,
                        "rule_type": rule.rule_type,
                        "last_triggered_at": rule.last_triggered_at.isoformat() if rule.last_triggered_at else None
                    }
                    for rule in top_rules
                ],
                "recent_activity": [
                    {
                        "name": rule.name,
                        "rule_type": rule.rule_type,
                        "last_triggered_at": rule.last_triggered_at.isoformat() if rule.last_triggered_at else None
                    }
                    for rule in recent_activity
                ]
            }
