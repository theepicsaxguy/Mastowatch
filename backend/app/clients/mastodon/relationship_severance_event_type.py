from enum import Enum


class RelationshipSeveranceEventType(str, Enum):
    ACCOUNT_SUSPENSION = "account_suspension"
    DOMAIN_BLOCK = "domain_block"
    USER_DOMAIN_BLOCK = "user_domain_block"

    def __str__(self) -> str:
        return str(self.value)
