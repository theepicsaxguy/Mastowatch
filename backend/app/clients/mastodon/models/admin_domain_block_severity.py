from enum import Enum


class AdminDomainBlockSeverity(str, Enum):
    NOOP = "noop"
    SILENCE = "silence"
    SUSPEND = "suspend"

    def __str__(self) -> str:
        return str(self.value)
