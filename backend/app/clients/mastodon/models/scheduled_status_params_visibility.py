from enum import Enum


class ScheduledStatusParamsVisibility(str, Enum):
    DIRECT = "direct"
    PRIVATE = "private"
    PUBLIC = "public"
    UNLISTED = "unlisted"

    def __str__(self) -> str:
        return str(self.value)
