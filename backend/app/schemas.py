from typing import Any, Dict, List
from pydantic import BaseModel, Field


class Evidence(BaseModel):
    matched_terms: List[str]
    matched_status_ids: List[str]
    metrics: Dict


class Violation(BaseModel):
    rule_name: str
    score: float
    evidence: Evidence
    actions: List[Dict[str, Any]] = Field(default_factory=list)


class AccountsPage(BaseModel):
    accounts: List[Dict[str, Any]]
    next_cursor: str | None = None
