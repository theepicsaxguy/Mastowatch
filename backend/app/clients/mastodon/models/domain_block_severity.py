from enum import Enum


class DomainBlockSeverity(str, Enum):
    SILENCE = "silence"
    SUSPEND = "suspend"

    def __str__(self) -> str:
        return str(self.value)
