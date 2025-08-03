from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.policy_enum import PolicyEnum
from ..types import UNSET, Unset

T = TypeVar("T", bound="CreateListBody")


@_attrs_define
class CreateListBody:
    """
    Attributes:
        title (str): The title of the list to be created.
        exclusive (Union[Unset, bool]): Whether members of this list need to get removed from the “Home” feed.
        replies_policy (Union[Unset, PolicyEnum]):

    """

    title: str
    exclusive: Unset | bool = UNSET
    replies_policy: Unset | PolicyEnum = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        title = self.title

        exclusive = self.exclusive

        replies_policy: Unset | str = UNSET
        if not isinstance(self.replies_policy, Unset):
            replies_policy = self.replies_policy.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "title": title,
            }
        )
        if exclusive is not UNSET:
            field_dict["exclusive"] = exclusive
        if replies_policy is not UNSET:
            field_dict["replies_policy"] = replies_policy

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        title = d.pop("title")

        exclusive = d.pop("exclusive", UNSET)

        _replies_policy = d.pop("replies_policy", UNSET)
        replies_policy: Unset | PolicyEnum
        if isinstance(_replies_policy, Unset):
            replies_policy = UNSET
        else:
            replies_policy = PolicyEnum(_replies_policy)

        create_list_body = cls(
            title=title,
            exclusive=exclusive,
            replies_policy=replies_policy,
        )

        create_list_body.additional_properties = d
        return create_list_body

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
