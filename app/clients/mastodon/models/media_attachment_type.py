from enum import Enum


class MediaAttachmentType(str, Enum):
    AUDIO = "audio"
    GIFV = "gifv"
    IMAGE = "image"
    UNKNOWN = "unknown"
    VIDEO = "video"

    def __str__(self) -> str:
        return str(self.value)
