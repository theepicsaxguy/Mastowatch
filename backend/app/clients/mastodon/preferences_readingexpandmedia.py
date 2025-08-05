from enum import Enum


class PreferencesReadingexpandmedia(str, Enum):
    DEFAULT = "default"
    HIDE_ALL = "hide_all"
    SHOW_ALL = "show_all"

    def __str__(self) -> str:
        return str(self.value)
