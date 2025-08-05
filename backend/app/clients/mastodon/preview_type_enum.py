from enum import Enum


class PreviewTypeEnum(str, Enum):
    LINK = "link"
    PHOTO = "photo"
    RICH = "rich"
    VIDEO = "video"

    def __str__(self) -> str:
        return str(self.value)
