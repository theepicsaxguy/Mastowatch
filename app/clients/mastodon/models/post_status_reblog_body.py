from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="PostStatusReblogBody")


@_attrs_define
class PostStatusReblogBody:
    """
    Attributes:
        visibility (Union[Unset, str]): Any visibility except `limited` or `direct` (i.e. `public`, `unlisted`,
            `private`). Defaults to public. Default: 'public'.
    """

    visibility: Union[Unset, str] = "public"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        visibility = self.visibility

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if visibility is not UNSET:
            field_dict["visibility"] = visibility

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        visibility = d.pop("visibility", UNSET)

        post_status_reblog_body = cls(
            visibility=visibility,
        )

        post_status_reblog_body.additional_properties = d
        return post_status_reblog_body

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
