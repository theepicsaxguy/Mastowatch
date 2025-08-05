from enum import Enum


class PolicyEnum(str, Enum):
    FOLLOWED = "followed"
    LIST = "list"
    NONE = "none"

    def __str__(self) -> str:
        return str(self.value)
