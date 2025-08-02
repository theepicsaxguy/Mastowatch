from typing import List, Any
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import re

from app.auth import require_admin_hybrid
from app.db import SessionLocal
from app.models import Rule
from app.schemas import User
from app.services.rule_service import rule_service
from app.enhanced_scanning import EnhancedScanningSystem

router = APIRouter()

# Database dependency
def get_db_session():
    """Dependency to get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/rules/current", tags=["rules"])
def get_current_rules(_: User = Depends(require_admin_hybrid)):
    """Get current rule configuration including database rules"""
    all_rules, config, _ = rule_service.get_active_rules()
    return {
        "rules": {
            **all_rules,
            "report_threshold": config.get("report_threshold", 1.0)
        },
        "report_threshold": config.get("report/threshold", 1.0)
    }


@router.get("/rules", tags=["rules"])
def list_rules(_: User = Depends(require_admin_hybrid)):
    """List all rules (file-based and database rules)"""    all_rules, _, _ = rule_service.get_active_rules()
    response = []
    
    # Convert to flat list for easier frontend consumption
    for rule_type, type_rules in all_rules.items():
        for rule in type_rules:
            response.append({
                **rule,
                "rule_type": rule_type
            })
    
    return {"rules": response}


@router.post("/rules", tags=["rules"])
def create_rule(
    rule_data: dict, 
    _: User = Depends(require_admin_hybrid),
    session: Session = Depends(get_db_session)
):
    """Create a new rule"""
    try:
        # Validate required fields
        required_fields = ["name", "detector_type", "pattern", "weight", "action_type", "trigger_threshold"]
        for field in required_fields:
            if field not in rule_data:
                raise HTTPException(
                    status_code=400, 
                    detail={
                        "error": f"Missing required field: {field}",
                        "required_fields": required_fields,
                        "help": "Use GET /rules/help for examples and guidance"
                    }
                )
        
        # Validate detector_type
        valid_detector_types = ["regex", "keyword", "behavioral"]
        if rule_data["detector_type"] not in valid_detector_types:
            raise HTTPException(
                status_code=400, 
                detail={
                    "error": f"Invalid detector_type: {rule_data['detector_type']}",
                    "valid_types": valid_detector_types,
                    "help": "Use GET /rules/help to see examples for each detector type"
                }
            )
        
        # Validate weight
        try:
            weight = float(rule_data["weight"])
            if weight < 0 or weight > 5.0:
                raise ValueError("Weight must be between 0 and 5.0")
        except (ValueError, TypeError) as e:
            raise HTTPException(
                status_code=400,
                detail={
                    "error": f"Invalid weight: {str(e)}",
                    "guidelines": "Weight should be 0.1-0.3 (mild), 0.4-0.6 (moderate), 0.7-0.9 (strong), 1.0+ (very strong)",
                    "help": "Use GET /rules/help for weight guidelines and examples"
                }
            )
        
        # Validate trigger_threshold
        try:
            trigger_threshold = float(rule_data["trigger_threshold"])
            if trigger_threshold < 0 or trigger_threshold > 10.0:
                raise ValueError("Trigger threshold must be between 0 and 10.0")
        except (ValueError, TypeError) as e:
            raise HTTPException(
                status_code=400,
                detail={
                    "error": f"Invalid trigger_threshold: {str(e)}",
                    "guidelines": "Trigger threshold should be 0.1-10.0",
                    "help": "Use GET /rules/help for trigger threshold guidelines and examples"
                }
            )

        # Test regex pattern if detector_type is regex
        if rule_data["detector_type"] == "regex":
            try:
                re.compile(rule_data["pattern"])
            except re.error as e:
                raise HTTPException(
                    status_code=400, 
                    detail={
                        "error": f"Invalid regex pattern: {str(e)}",
                        "pattern": rule_data["pattern"],
                        "detector_type": rule_data["detector_type"],
                        "suggestions": ["Check for unescaped special characters", "Ensure balanced parentheses and brackets", "Test on regex101.com first"]
                    }
                )
        
        # Create rule
        new_rule = rule_service.create_rule(
            name=rule_data["name"],
            detector_type=rule_data["detector_type"],
            pattern=rule_data["pattern"],
            weight=weight,
            action_type=rule_data["action_type"],
            trigger_threshold=trigger_threshold,
            action_duration_seconds=rule_data.get("action_duration_seconds"),
            action_warning_text=rule_data.get("action_warning_text"),
            warning_preset_id=rule_data.get("warning_preset_id"),
            enabled=rule_data.get("enabled", True),
            description=rule_data.get("description"),
            created_by=_.username if _ else "system"
        )
        
        return {
            "id": new_rule.id,
            "name": new_rule.name,
            "detector_type": new_rule.detector_type,
            "pattern": new_rule.pattern,
            "weight": float(new_rule.weight),
            "action_type": new_rule.action_type,
            "trigger_threshold": float(new_rule.trigger_threshold),
            "enabled": new_rule.enabled,
            "is_default": new_rule.is_default
        }
        
    except HTTPException:
        raise
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to create rule: {e}")


@router.get("/rules/help", tags=["rules"])
def get_rule_creation_help():
    """Get comprehensive help text and examples for creating rules"""
    return {
        "detector_types": {
            "regex": {
                "description": "Matches against text content using regular expressions.",
                "examples": [
                    {"name": "Spam URLs", "pattern": r"https?://[a-zA-Z0-9.-]+\\.(tk|ml|ga|cf|gq)/", "weight": 1.5, "action_type": "report", "trigger_threshold": 1.0, "description": "Matches suspicious free domain extensions often used for spam"},
                ]
            },
            "keyword": {
                "description": "Matches against text content using keywords.",
                "examples": [
                    {"name": "Crypto Keywords", "pattern": "bitcoin,ethereum,crypto", "weight": 1.2, "action_type": "silence", "trigger_threshold": 1.0, "description": "Matches common cryptocurrency terms"},
                ]
            },
            "behavioral": {
                "description": "Matches against account behavior metrics.",
                "examples": [
                    {"name": "Rapid Posting", "pattern": "posts_last_1h", "weight": 0.8, "action_type": "suspend", "trigger_threshold": 50, "description": "Matches accounts posting more than 50 times in the last hour"},
                ]
            }
        },
        "action_types": {
            "report": "Generates a report to the Mastodon instance.",
            "silence": "Silences the account on the Mastodon instance.",
            "suspend": "Suspends the account on the Mastodon instance.",
            "disable": "Disables the account on the Mastodon instance.",
            "sensitive": "Marks content as sensitive.",
            "domain_block": "Blocks the domain of the account."
        },
        "weight_guidelines": {
            "description": "Rule weight determines how much each match contributes to the final score",
            "guidelines": [
                "0.1 - 0.3: Very mild indicators (suspicious but not conclusive)",
                "0.4 - 0.6: Moderate indicators (worth noting but not alarming)",
                "0.7 - 0.9: Strong indicators (likely problematic content)",
                "1.0 - 1.5: Very strong indicators (almost certainly spam/abuse)",
                "1.6+: Extreme indicators (immediate action warranted)"
            ]
        },
        "trigger_threshold_guidelines": {
            "description": "The score an account must reach to trigger the rule's action.",
            "guidelines": [
                "For text-based detectors (regex, keyword), this is typically 1.0 or higher, meaning a single strong match can trigger.",
                "For behavioral detectors, this is the numerical threshold for the metric (e.g., 50 for 'posts_last_1h')."
            ]
        },
        "regex_tips": {
            "description": "Tips for creating effective regex patterns",
            "tips": [
                "Use ^ and $ to match the entire string (^pattern$)",
                "Use .* to match any characters before/after your pattern",
                "Use \\d for digits, \\w for word characters, \\s for spaces",
                "Use + for one or more, * for zero or more, {3,} for 3 or more",
                "Use (option1|option2) for alternatives",
                "Escape special characters with backslash: \\. \\? \\+ \\* \\(",
                "Test your patterns carefully - they affect real moderation decisions"
            ]
        },
        "testing_guidance": {
            "description": "How to test and validate your rules",
            "steps": [
                "1. Test your regex pattern with online tools first",
                "2. Start with a low weight (0.1-0.3) for new rules",
                "3. Monitor rule performance after creation",
                "4. Adjust weights based on false positive/negative rates",
                "5. Use the dry-run mode to test before applying",
                "6. Review triggered rules regularly for accuracy"
            ]
        }
    }


@router.post("/rules/validate-pattern", tags=["rules"])
def validate_rule_pattern(
    pattern_data: dict,
    _: User = Depends(require_admin_hybrid)
):
    """Validate a regex pattern and provide feedback"""
    try:
        pattern = pattern_data.get("pattern", "")
        test_strings = pattern_data.get("test_strings", [])
        
        if not pattern:
            raise HTTPException(status_code=400, detail="Pattern is required")
        
        # Test if the regex is valid
        try:
            compiled_pattern = re.compile(pattern)
        except re.error as e:
            return {
                "valid": False,
                "error": f"Invalid regex pattern: {str(e)}",
                "suggestions": [
                    "Check for unescaped special characters: . ? + * [ ] ( ) { } ^ $ |",
                    "Ensure balanced parentheses and brackets",
                    "Use raw strings (r'pattern') to avoid escape issues",
                    "Test your pattern on regex101.com first"
                ]
            }
        
        # Test against provided strings
        test_results = []
        if test_strings:
            for test_string in test_strings[:10]:  # Limit to 10 test strings
                try:
                    match = compiled_pattern.search(str(test_string))
                    test_results.append({
                        "string": test_string,
                        "matches": bool(match),
                        "match_text": match.group(0) if match else None
                    })
                except Exception as e:
                    test_results.append({
                        "string": test_string,
                        "matches": False,
                        "error": str(e)
                    })
        
        # Pattern complexity analysis
        complexity_score = 0
        complexity_notes = []
        
        if len(pattern) > 100:
            complexity_score += 1
            complexity_notes.append("Long pattern - consider breaking into multiple rules")
        
        if pattern.count('.*') > 3:
            complexity_score += 1
            complexity_notes.append("Many .* wildcards - may be too broad")
        
        if '|' in pattern and pattern.count('|') > 5:
            complexity_score += 1
            complexity_notes.effective = "High"
            complexity_notes.append("Many alternatives - consider separate rules")
        
        complexity_level = "Low" if complexity_score == 0 else "Medium" if complexity_score == 1 else "High"
        
        return {
            "valid": True,
            "pattern": pattern,
            "test_results": test_results,
            "complexity": {
                "level": complexity_level,
                "score": complexity_score,
                "notes": complexity_notes
            },
            "recommendations": [
                "Test with a variety of strings before deploying",
                "Start with a low weight (0.1-0.3) for new patterns",
                "Monitor false positives after deployment",
                "Consider case sensitivity for your use case"
            ]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to validate pattern: {e}")


@router.put("/rules/{rule_id}", tags=["rules"])
def update_rule(
    rule_id: int,
    rule_data: dict,
    _: User = Depends(require_admin_hybrid),
    session: Session = Depends(get_db_session)
):
    """Update an existing rule"""
    try:
        rule = session.query(Rule).filter(Rule.id == rule_id).first()
        if not rule:
            raise HTTPException(status_code=404, detail="Rule not found")
        
        updated_rule = rule_service.update_rule(rule_id, **rule_data)
        
        return {
            "id": updated_rule.id,
            "name": updated_rule.name,
            "detector_type": updated_rule.detector_type,
            "pattern": updated_rule.pattern,
            "weight": float(updated_rule.weight),
            "action_type": updated_rule.action_type,
            "trigger_threshold": float(updated_rule.trigger_threshold),
            "enabled": updated_rule.enabled,
            "is_default": updated_rule.is_default,
            "message": "Rule updated"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to update rule: {e}")


@router.delete("/rules/{rule_id}", tags=["rules"])
def delete_rule(
    rule_id: int,
    _: User = Depends(require_admin_hybrid),
    session: Session = Depends(get_db_session)
):
    """Delete a rule"""
    try:
        rule_service.delete_rule(rule_id)
        
        return {"message": "Rule deleted successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to delete rule: {e}")


@router.post("/rules/{rule_id}/toggle", tags=["rules"])
def toggle_rule(
    rule_id: int,
    _: User = Depends(require_admin_hybrid),
    session: Session = Depends(get_db_session)
):
    """Toggle rule enabled/disabled status"""
    try:
        toggled_rule = rule_service.toggle_rule(rule_id, not rule_service.get_rule_by_id(rule_id).enabled)
        
        # Invalidate content scans due to rule changes
        enhanced_scanner = EnhancedScanningSystem()
        enhanced_scanner.invalidate_content_scans(rule_changes=True)
        
        return {
            "id": toggled_rule.id,
            "name": toggled_rule.name,
            "enabled": toggled_rule.enabled,
            "message": f"Rule {"enabled" if toggled_rule.enabled else "disabled"}"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to toggle rule: {e}")


@router.post("/rules/bulk-toggle", tags=["rules"])
def bulk_toggle_rules(
    rule_ids: List[int],
    enabled: bool,
    _: User = Depends(require_admin_hybrid),
    session: Session = Depends(get_db_session)
):
    """Toggle multiple rules at once"""
    try:
        updated_rules = rule_service.bulk_toggle_rules(rule_ids, enabled)
        
        # Invalidate content scans due to rule changes
        enhanced_scanner = EnhancedScanningSystem()
        enhanced_scanner.invalidate_content_scans(rule_changes=True)

        return {
            "message": f"Successfully {"enabled" if enabled else "disabled"} {len(updated_rules)} rules.",
            "updated_rules_count": len(updated_rules)
        }
        
    except HTTPException:
        raise
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to bulk toggle rules: {e}")
