from enum import Enum


class CredentialAccountSourcePrivacy(str, Enum):
    DIRECT = "direct"
    PRIVATE = "private"
    PUBLIC = "public"
    UNLISTED = "unlisted"

    def __str__(self) -> str:
        return str(self.value)
