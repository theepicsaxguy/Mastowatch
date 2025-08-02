from io import BytesIO
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, File, FileJsonType, Unset

T = TypeVar("T", bound="CreateMediaV2Body")


@_attrs_define
class CreateMediaV2Body:
    """
    Attributes:
        file (File): The file to be attached, encoded using multipart form data. The file must have a MIME type.
        description (Union[Unset, str]): A plain-text description of the media, for accessibility purposes.
        focus (Union[Unset, str]): Two floating points (x,y), comma-delimited, ranging from -1.0 to 1.0. See [Focal
            points for cropping media thumbnails] for more information.
        thumbnail (Union[Unset, File]): The custom thumbnail of the media to be attached, encoded using multipart form
            data.
    """

    file: File
    description: Union[Unset, str] = UNSET
    focus: Union[Unset, str] = UNSET
    thumbnail: Union[Unset, File] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        file = self.file.to_tuple()

        description = self.description

        focus = self.focus

        thumbnail: Union[Unset, FileJsonType] = UNSET
        if not isinstance(self.thumbnail, Unset):
            thumbnail = self.thumbnail.to_tuple()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "file": file,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description
        if focus is not UNSET:
            field_dict["focus"] = focus
        if thumbnail is not UNSET:
            field_dict["thumbnail"] = thumbnail

        return field_dict

    def to_multipart(self) -> dict[str, Any]:
        file = self.file.to_tuple()

        description = (
            self.description
            if isinstance(self.description, Unset)
            else (None, str(self.description).encode(), "text/plain")
        )

        focus = (
            self.focus
            if isinstance(self.focus, Unset)
            else (None, str(self.focus).encode(), "text/plain")
        )

        thumbnail: Union[Unset, FileJsonType] = UNSET
        if not isinstance(self.thumbnail, Unset):
            thumbnail = self.thumbnail.to_tuple()

        field_dict: dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            field_dict[prop_name] = (None, str(prop).encode(), "text/plain")

        field_dict.update(
            {
                "file": file,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description
        if focus is not UNSET:
            field_dict["focus"] = focus
        if thumbnail is not UNSET:
            field_dict["thumbnail"] = thumbnail

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        file = File(payload=BytesIO(d.pop("file")))

        description = d.pop("description", UNSET)

        focus = d.pop("focus", UNSET)

        _thumbnail = d.pop("thumbnail", UNSET)
        thumbnail: Union[Unset, File]
        if isinstance(_thumbnail, Unset):
            thumbnail = UNSET
        else:
            thumbnail = File(payload=BytesIO(_thumbnail))

        create_media_v2_body = cls(
            file=file,
            description=description,
            focus=focus,
            thumbnail=thumbnail,
        )

        create_media_v2_body.additional_properties = d
        return create_media_v2_body

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
