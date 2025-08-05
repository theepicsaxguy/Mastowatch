from enum import Enum


class GetMarkersTimelineItem(str, Enum):
    HOME = "home"
    NOTIFICATIONS = "notifications"

    def __str__(self) -> str:
        return str(self.value)
