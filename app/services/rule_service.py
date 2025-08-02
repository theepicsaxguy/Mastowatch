"""
Centralized RuleService for database-driven rule management.

This service encapsulates all database interactions for rules and provides
caching to avoid hitting the database on every scan operation.
"""

import hashlib
import logging
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass

from sqlalchemy import text
from sqlalchemy.orm import Session

from app.db import SessionLocal, engine
from app.models import Rule


logger = logging.getLogger(__name__)


@dataclass
class RuleCache:
    """In-memory cache for rules to avoid frequent database hits"""
    rules: List[Rule]
    config: Dict[str, Any]
    ruleset_sha256: str
    cached_at: datetime
    ttl_seconds: int = 60  # Cache for 60 seconds

    def is_expired(self) -> bool:
        """Check if the cache has expired"""
        return datetime.utcnow() - self.cached_at > timedelta(seconds=self.ttl_seconds)


class RuleService:
    """
    Centralized service for rule management and database operations.
    
    This service provides:
    - Database-only rule loading (no file dependencies)
    - Caching to reduce database load during scanning
    - CRUD operations for rule management
    - Rule statistics and metadata tracking
    """
    
    def __init__(self, cache_ttl_seconds: int = 60):
        self._cache: Optional[RuleCache] = None
        self._cache_ttl = cache_ttl_seconds
    
    def get_active_rules(self, force_refresh: bool = False) -> Tuple[List[Rule], Dict[str, Any], str]:
        """
        Get active rules from database with caching.
        
        Args:
            force_refresh: If True, bypass cache and reload from database
            
        Returns:
            Tuple of (rules_list, config_dict, ruleset_sha256)
        """
        if not force_refresh and self._cache and not self._cache.is_expired():
            return self._cache.rules, self._cache.config, self._cache.ruleset_sha256
        
        return self._load_rules_from_database()
    
    def _load_rules_from_database(self) -> Tuple[List[Rule], Dict[str, Any], str]:
        """Load rules from database and update cache"""
        with SessionLocal() as session:
            # Get all enabled rules
            db_rules = session.query(Rule).filter(Rule.enabled == True).all()
            
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
            
            # Update cache
            self._cache = RuleCache(
                rules=db_rules,
                config=config,
                ruleset_sha256=ruleset_sha256,
                cached_at=datetime.utcnow(),
                ttl_seconds=self._cache_ttl
            )
            
            logger.debug(f"Loaded {len(db_rules)} rules from database, SHA: {ruleset_sha256[:8]}")
            
            return db_rules, config, ruleset_sha256
    
    def create_rule(self, 
                   name: str,
                   rule_type: str,
                   pattern: str,
                   weight: float,
                   enabled: bool = True,
                   description: Optional[str] = None,
                   created_by: str = "system") -> Rule:
        """
        Create a new rule in the database.
        
        Args:
            name: Human-readable name for the rule
            rule_type: Type of rule (username_regex, content_regex, etc.)
            pattern: Regex pattern for the rule
            weight: Weight/score assigned when rule matches
            enabled: Whether the rule is active
            description: Optional description of the rule
            created_by: User/system that created the rule
            
        Returns:
            The created Rule object
        """
        with SessionLocal() as session:
            rule = Rule(
                name=name,
                rule_type=rule_type,
                pattern=pattern,
                weight=weight,
                enabled=enabled,
                description=description,
                created_by=created_by,
                created_at=datetime.utcnow()
            )
            
            session.add(rule)
            session.commit()
            session.refresh(rule)
            
            # Invalidate cache since rules changed
            self._invalidate_cache()
            
            logger.info(f"Created new rule: {name} (type: {rule_type}, weight: {weight})")
            return rule
    
    def update_rule(self, rule_id: int, **updates) -> Optional[Rule]:
        """
        Update an existing rule.
        
        Args:
            rule_id: ID of the rule to update
            **updates: Dictionary of fields to update
            
        Returns:
            Updated Rule object or None if not found
        """
        with SessionLocal() as session:
            rule = session.query(Rule).filter(Rule.id == rule_id).first()
            if not rule:
                return None
            
            # Update provided fields
            for field, value in updates.items():
                if hasattr(rule, field):
                    setattr(rule, field, value)
            
            rule.updated_at = datetime.utcnow()
            session.commit()
            session.refresh(rule)
            
            # Invalidate cache since rules changed
            self._invalidate_cache()
            
            logger.info(f"Updated rule {rule_id}: {list(updates.keys())}")
            return rule
    
    def delete_rule(self, rule_id: int) -> bool:
        """
        Delete a rule from the database.
        
        Args:
            rule_id: ID of the rule to delete
            
        Returns:
            True if rule was deleted, False if not found
        """
        with SessionLocal() as session:
            rule = session.query(Rule).filter(Rule.id == rule_id).first()
            if not rule:
                return False
            
            session.delete(rule)
            session.commit()
            
            # Invalidate cache since rules changed
            self._invalidate_cache()
            
            logger.info(f"Deleted rule {rule_id}: {rule.name}")
            return True
    
    def toggle_rule(self, rule_id: int, enabled: bool) -> Optional[Rule]:
        """
        Enable or disable a rule.
        
        Args:
            rule_id: ID of the rule to toggle
            enabled: New enabled state
            
        Returns:
            Updated Rule object or None if not found
        """
        return self.update_rule(rule_id, enabled=enabled)
    
    def bulk_toggle_rules(self, rule_ids: List[int], enabled: bool) -> List[Rule]:
        """
        Enable or disable multiple rules at once.
        
        Args:
            rule_ids: List of rule IDs to toggle
            enabled: New enabled state for all rules
            
        Returns:
            List of updated Rule objects
        """
        updated_rules = []
        with SessionLocal() as session:
            rules = session.query(Rule).filter(Rule.id.in_(rule_ids)).all()
            
            for rule in rules:
                rule.enabled = enabled
                rule.updated_at = datetime.utcnow()
                updated_rules.append(rule)
            
            session.commit()
            
            # Invalidate cache since rules changed
            self._invalidate_cache()
            
            logger.info(f"Bulk toggled {len(updated_rules)} rules to enabled={enabled}")
            return updated_rules
    
    def get_rule_statistics(self) -> Dict[str, Any]:
        """
        Get comprehensive rule statistics.
        
        Returns:
            Dictionary containing rule performance metrics
        """
        with SessionLocal() as session:
            rules = session.query(Rule).all()
            
            total_rules = len(rules)
            enabled_rules = len([r for r in rules if r.enabled])
            disabled_rules = total_rules - enabled_rules
            
            # Calculate trigger statistics
            triggered_rules = [r for r in rules if r.trigger_count and r.trigger_count > 0]
            total_triggers = sum(r.trigger_count or 0 for r in rules)
            
            # Get rules by type
            rules_by_type = {}
            for rule in rules:
                rule_type = rule.rule_type
                if rule_type not in rules_by_type:
                    rules_by_type[rule_type] = {"total": 0, "enabled": 0}
                rules_by_type[rule_type]["total"] += 1
                if rule.enabled:
                    rules_by_type[rule_type]["enabled"] += 1
            
            # Get most triggered rules
            most_triggered = sorted(
                [r for r in rules if r.trigger_count],
                key=lambda x: x.trigger_count,
                reverse=True
            )[:10]
            
            return {
                "total_rules": total_rules,
                "enabled_rules": enabled_rules,
                "disabled_rules": disabled_rules,
                "triggered_rules_count": len(triggered_rules),
                "total_triggers": total_triggers,
                "rules_by_type": rules_by_type,
                "most_triggered": [
                    {
                        "id": r.id,
                        "name": r.name,
                        "rule_type": r.rule_type,
                        "trigger_count": r.trigger_count,
                        "last_triggered_at": r.last_triggered_at.isoformat() if r.last_triggered_at else None
                    }
                    for r in most_triggered
                ],
                "cache_status": {
                    "cached": self._cache is not None,
                    "expired": self._cache.is_expired() if self._cache else True,
                    "cached_at": self._cache.cached_at.isoformat() if self._cache else None,
                    "ttl_seconds": self._cache_ttl
                }
            }
    
    def update_rule_trigger_stats(self, rule_id: int, triggered_content: Optional[Dict] = None):
        """
        Update rule trigger statistics when a rule matches content.
        
        Args:
            rule_id: ID of the rule that was triggered
            triggered_content: Optional content that triggered the rule
        """
        with SessionLocal() as session:
            rule = session.query(Rule).filter(Rule.id == rule_id).first()
            if rule:
                rule.trigger_count = (rule.trigger_count or 0) + 1
                rule.last_triggered_at = datetime.utcnow()
                if triggered_content:
                    rule.last_triggered_content = triggered_content
                session.commit()
    
    def invalidate_cache(self):
        """Force cache invalidation to refresh rules on next access"""
        self._invalidate_cache()
    
    def _invalidate_cache(self):
        """Internal method to invalidate the cache"""
        self._cache = None
        logger.debug("Rule cache invalidated")
    
    def get_cache_status(self) -> Dict[str, Any]:
        """
        Get current cache status information.
        
        Returns:
            Dictionary with cache status details
        """
        if not self._cache:
            return {
                "cached": False,
                "expired": True,
                "cached_at": None,
                "ttl_seconds": self._cache_ttl,
                "rules_count": 0
            }
        
        return {
            "cached": True,
            "expired": self._cache.is_expired(),
            "cached_at": self._cache.cached_at.isoformat(),
            "ttl_seconds": self._cache_ttl,
            "rules_count": len(self._cache.rules),
            "ruleset_sha256": self._cache.ruleset_sha256[:8]
        }


# Global instance for use throughout the application
rule_service = RuleService()
