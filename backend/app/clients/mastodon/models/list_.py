from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.policy_enum import PolicyEnum

T = TypeVar("T", bound="List")


@_attrs_define
class List:
    """Represents a list of some users that the authenticated user follows.

    Example:
        {'id': '12249', 'title': 'Friends', 'replies_policy': 'list', 'exclusive': False}

    Attributes:
        exclusive (bool): Whether members of the list should be removed from the “Home” feed.
        id (str): The ID of the list.
        replies_policy (PolicyEnum):
        title (str): The user-defined title of the list.
    """

    exclusive: bool
    id: str
    replies_policy: PolicyEnum
    title: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        exclusive = self.exclusive

        id = self.id

        replies_policy = self.replies_policy.value

        title = self.title

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "exclusive": exclusive,
                "id": id,
                "replies_policy": replies_policy,
                "title": title,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        exclusive = d.pop("exclusive")

        id = d.pop("id")

        replies_policy = PolicyEnum(d.pop("replies_policy"))

        title = d.pop("title")

        list_ = cls(
            exclusive=exclusive,
            id=id,
            replies_policy=replies_policy,
            title=title,
        )

        list_.additional_properties = d
        return list_

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
