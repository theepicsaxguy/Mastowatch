from enum import Enum


class AccountWarningAction(str, Enum):
    DELETE_STATUSES = "delete_statuses"
    DISABLE = "disable"
    MARK_STATUSES_AS_SENSITIVE = "mark_statuses_as_sensitive"
    NONE = "none"
    SENSITIVE = "sensitive"
    SILENCE = "silence"
    SUSPEND = "suspend"

    def __str__(self) -> str:
        return str(self.value)
