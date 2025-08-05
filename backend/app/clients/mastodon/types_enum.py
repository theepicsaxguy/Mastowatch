from enum import Enum


class TypesEnum(str, Enum):
    ADMIN_REPORT = "admin.report"
    ADMIN_SIGN_UP = "admin.sign_up"
    FAVOURITE = "favourite"
    FOLLOW = "follow"
    FOLLOW_REQUEST = "follow_request"
    MENTION = "mention"
    POLL = "poll"
    REBLOG = "reblog"
    STATUS = "status"
    UPDATE = "update"

    def __str__(self) -> str:
        return str(self.value)
