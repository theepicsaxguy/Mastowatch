from enum import Enum


class CategoryEnum(str, Enum):
    OTHER = "other"
    SPAM = "spam"
    VIOLATION = "violation"

    def __str__(self) -> str:
        return str(self.value)
