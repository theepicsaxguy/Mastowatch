from enum import Enum


class AdminIpBlockSeverity(str, Enum):
    NO_ACCESS = "no_access"
    SIGN_UP_BLOCK = "sign_up_block"
    SIGN_UP_REQUIRES_APPROVAL = "sign_up_requires_approval"

    def __str__(self) -> str:
        return str(self.value)
