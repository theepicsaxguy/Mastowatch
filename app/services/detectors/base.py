"""Base detector class for content analysis."""

from abc import ABC, abstractmethod

from app.models import Rule
from app.schemas import Violation


class BaseDetector(ABC):
    """Abstract base class for content detectors."""

    @abstractmethod
    def evaluate(self, rule: Rule, account_data: dict, statuses: list[dict]) -> list[Violation]:
        """Evaluate account and statuses against a rule.

        Args:
            rule: The rule to evaluate against
            account_data: Dictionary containing account information
            statuses: List of status dictionaries

        Returns:
            List of violations found

        """
        pass
