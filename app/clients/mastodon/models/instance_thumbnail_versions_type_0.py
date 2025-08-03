from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="InstanceThumbnailVersionsType0")


@_attrs_define
class InstanceThumbnailVersionsType0:
    """Links to scaled resolution images, for high DPI screens.

    Attributes:
        field_1x (Union[None, Unset, str]): The URL for the thumbnail image at 1x resolution.
        field_2x (Union[None, Unset, str]): The URL for the thumbnail image at 2x resolution.

    """

    field_1x: None | Unset | str = UNSET
    field_2x: None | Unset | str = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        field_1x: None | Unset | str
        if isinstance(self.field_1x, Unset):
            field_1x = UNSET
        else:
            field_1x = self.field_1x

        field_2x: None | Unset | str
        if isinstance(self.field_2x, Unset):
            field_2x = UNSET
        else:
            field_2x = self.field_2x

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if field_1x is not UNSET:
            field_dict["@1x"] = field_1x
        if field_2x is not UNSET:
            field_dict["@2x"] = field_2x

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_field_1x(data: object) -> None | Unset | str:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | Unset | str, data)

        field_1x = _parse_field_1x(d.pop("@1x", UNSET))

        def _parse_field_2x(data: object) -> None | Unset | str:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | Unset | str, data)

        field_2x = _parse_field_2x(d.pop("@2x", UNSET))

        instance_thumbnail_versions_type_0 = cls(
            field_1x=field_1x,
            field_2x=field_2x,
        )

        instance_thumbnail_versions_type_0.additional_properties = d
        return instance_thumbnail_versions_type_0

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
