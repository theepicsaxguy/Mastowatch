from enum import Enum


class FilterFilterAction(str, Enum):
    BLUR = "blur"
    HIDE = "hide"
    WARN = "warn"

    def __str__(self) -> str:
        return str(self.value)
