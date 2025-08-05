from enum import Enum


class StateEnum(str, Enum):
    ACCEPTED = "accepted"
    DELETED = "deleted"
    PENDING = "pending"
    REJECTED = "rejected"
    REVOKED = "revoked"
    UNAUTHORIZED = "unauthorized"

    def __str__(self) -> str:
        return str(self.value)
