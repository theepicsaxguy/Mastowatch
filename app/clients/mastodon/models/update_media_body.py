from collections.abc import Mapping
from io import BytesIO
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from .. import types
from ..types import UNSET, File, FileTypes, Unset

T = TypeVar("T", bound="UpdateMediaBody")


@_attrs_define
class UpdateMediaBody:
    """
    Attributes:
        description (Union[Unset, str]): A plain-text description of the media, for accessibility purposes.
        focus (Union[Unset, str]): Two floating points (x,y), comma-delimited, ranging from -1.0 to 1.0. See [Focal
            points for cropping media thumbnails] for more information.
        thumbnail (Union[Unset, File]): The custom thumbnail of the media to be attached, encoded using multipart form
            data.

    """

    description: Unset | str = UNSET
    focus: Unset | str = UNSET
    thumbnail: Unset | File = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        description = self.description

        focus = self.focus

        thumbnail: Unset | FileTypes = UNSET
        if not isinstance(self.thumbnail, Unset):
            thumbnail = self.thumbnail.to_tuple()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if description is not UNSET:
            field_dict["description"] = description
        if focus is not UNSET:
            field_dict["focus"] = focus
        if thumbnail is not UNSET:
            field_dict["thumbnail"] = thumbnail

        return field_dict

    def to_multipart(self) -> types.RequestFiles:
        files: types.RequestFiles = []

        if not isinstance(self.description, Unset):
            files.append(("description", (None, str(self.description).encode(), "text/plain")))

        if not isinstance(self.focus, Unset):
            files.append(("focus", (None, str(self.focus).encode(), "text/plain")))

        if not isinstance(self.thumbnail, Unset):
            files.append(("thumbnail", self.thumbnail.to_tuple()))

        for prop_name, prop in self.additional_properties.items():
            files.append((prop_name, (None, str(prop).encode(), "text/plain")))

        return files

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        description = d.pop("description", UNSET)

        focus = d.pop("focus", UNSET)

        _thumbnail = d.pop("thumbnail", UNSET)
        thumbnail: Unset | File
        if isinstance(_thumbnail, Unset):
            thumbnail = UNSET
        else:
            thumbnail = File(payload=BytesIO(_thumbnail))

        update_media_body = cls(
            description=description,
            focus=focus,
            thumbnail=thumbnail,
        )

        update_media_body.additional_properties = d
        return update_media_body

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
