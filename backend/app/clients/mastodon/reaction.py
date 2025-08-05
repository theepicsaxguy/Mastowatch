from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
    Union,
    cast,
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="Reaction")


@_attrs_define
class Reaction:
    """Represents an emoji reaction to an Announcement.

    Attributes:
        count (int): The total number of users who have added this reaction.
        name (str): The emoji used for the reaction. Either a unicode emoji, or a custom emoji's shortcode.
        me (Union[None, Unset, bool]): If there is a currently authorized user: Have you added this reaction?
        static_url (Union[None, Unset, str]): If the reaction is a custom emoji: A link to a non-animated version of the
            custom emoji.
        url (Union[None, Unset, str]): If the reaction is a custom emoji: A link to the custom emoji.
    """

    count: int
    name: str
    me: Union[None, Unset, bool] = UNSET
    static_url: Union[None, Unset, str] = UNSET
    url: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        count = self.count

        name = self.name

        me: Union[None, Unset, bool]
        if isinstance(self.me, Unset):
            me = UNSET
        else:
            me = self.me

        static_url: Union[None, Unset, str]
        if isinstance(self.static_url, Unset):
            static_url = UNSET
        else:
            static_url = self.static_url

        url: Union[None, Unset, str]
        if isinstance(self.url, Unset):
            url = UNSET
        else:
            url = self.url

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "count": count,
                "name": name,
            }
        )
        if me is not UNSET:
            field_dict["me"] = me
        if static_url is not UNSET:
            field_dict["static_url"] = static_url
        if url is not UNSET:
            field_dict["url"] = url

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        count = d.pop("count")

        name = d.pop("name")

        def _parse_me(data: object) -> Union[None, Unset, bool]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, bool], data)

        me = _parse_me(d.pop("me", UNSET))

        def _parse_static_url(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        static_url = _parse_static_url(d.pop("static_url", UNSET))

        def _parse_url(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        url = _parse_url(d.pop("url", UNSET))

        reaction = cls(
            count=count,
            name=name,
            me=me,
            static_url=static_url,
            url=url,
        )

        reaction.additional_properties = d
        return reaction

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
