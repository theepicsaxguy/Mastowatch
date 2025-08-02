from abc import ABC, abstractmethod
from typing import List, Dict

from app.schemas import Violation


class BaseDetector(ABC):
    @abstractmethod
    def evaluate(self, rule: Any, account_data: Dict, statuses: List[Dict]) -> List[Violation]:
        pass
