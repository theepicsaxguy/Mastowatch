from enum import Enum


class FilterContext(str, Enum):
    ACCOUNT = "account"
    HOME = "home"
    NOTIFICATIONS = "notifications"
    PUBLIC = "public"
    THREAD = "thread"

    def __str__(self) -> str:
        return str(self.value)
