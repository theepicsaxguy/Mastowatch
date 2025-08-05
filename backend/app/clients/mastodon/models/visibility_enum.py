from enum import Enum


class VisibilityEnum(str, Enum):
    DIRECT = "direct"
    PRIVATE = "private"
    PUBLIC = "public"
    UNLISTED = "unlisted"

    def __str__(self) -> str:
        return str(self.value)
