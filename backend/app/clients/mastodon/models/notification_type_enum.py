from enum import Enum


class NotificationTypeEnum(str, Enum):
    ADMIN_REPORT = "admin.report"
    ADMIN_SIGN_UP = "admin.sign_up"
    FAVOURITE = "favourite"
    FOLLOW = "follow"
    FOLLOW_REQUEST = "follow_request"
    MENTION = "mention"
    MODERATION_WARNING = "moderation_warning"
    POLL = "poll"
    REBLOG = "reblog"
    SEVERED_RELATIONSHIPS = "severed_relationships"
    STATUS = "status"
    UPDATE = "update"

    def __str__(self) -> str:
        return str(self.value)
