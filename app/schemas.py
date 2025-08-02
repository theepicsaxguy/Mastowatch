from typing import List, Dict
from pydantic import BaseModel


class Evidence(BaseModel):
    matched_terms: List[str]
    matched_status_ids: List[str]
    metrics: Dict


class Violation(BaseModel):
    rule_name: str
    score: float
    evidence: Evidence
