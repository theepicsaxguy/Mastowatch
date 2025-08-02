from abc import ABC, abstractmethod
from abc import ABC, abstractmethod
from typing import List, Dict, Any

from app.schemas import Violation
from app.models import Rule


class BaseDetector(ABC):
    @abstractmethod
    def evaluate(self, rule: Rule, account_data: Dict, statuses: List[Dict]) -> List[Violation]:
        pass
