from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="V1InstanceConfigurationMediaAttachments")


@_attrs_define
class V1InstanceConfigurationMediaAttachments:
    """Hints for which attachments will be accepted.

    Attributes:
        image_matrix_limit (int): The maximum number of pixels (width times height) for image uploads.
        image_size_limit (int): The maximum size of any uploaded image, in bytes.
        supported_mime_types (list[str]): Contains MIME types that can be uploaded.
        video_frame_rate_limit (int): The maximum frame rate for any uploaded video.
        video_matrix_limit (int): The maximum number of pixels (width times height) for video uploads.
        video_size_limit (int): The maximum size of any uploaded video, in bytes.
    """

    image_matrix_limit: int
    image_size_limit: int
    supported_mime_types: list[str]
    video_frame_rate_limit: int
    video_matrix_limit: int
    video_size_limit: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        image_matrix_limit = self.image_matrix_limit

        image_size_limit = self.image_size_limit

        supported_mime_types = self.supported_mime_types

        video_frame_rate_limit = self.video_frame_rate_limit

        video_matrix_limit = self.video_matrix_limit

        video_size_limit = self.video_size_limit

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "image_matrix_limit": image_matrix_limit,
                "image_size_limit": image_size_limit,
                "supported_mime_types": supported_mime_types,
                "video_frame_rate_limit": video_frame_rate_limit,
                "video_matrix_limit": video_matrix_limit,
                "video_size_limit": video_size_limit,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        image_matrix_limit = d.pop("image_matrix_limit")

        image_size_limit = d.pop("image_size_limit")

        supported_mime_types = cast(list[str], d.pop("supported_mime_types"))

        video_frame_rate_limit = d.pop("video_frame_rate_limit")

        video_matrix_limit = d.pop("video_matrix_limit")

        video_size_limit = d.pop("video_size_limit")

        v1_instance_configuration_media_attachments = cls(
            image_matrix_limit=image_matrix_limit,
            image_size_limit=image_size_limit,
            supported_mime_types=supported_mime_types,
            video_frame_rate_limit=video_frame_rate_limit,
            video_matrix_limit=video_matrix_limit,
            video_size_limit=video_size_limit,
        )

        v1_instance_configuration_media_attachments.additional_properties = d
        return v1_instance_configuration_media_attachments

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
