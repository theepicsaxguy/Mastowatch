from enum import Enum


class CreateReportBodyCategory(str, Enum):
    LEGAL = "legal"
    OTHER = "other"
    SPAM = "spam"
    VIOLATION = "violation"

    def __str__(self) -> str:
        return str(self.value)
