from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.instance_usage_users import InstanceUsageUsers


T = TypeVar("T", bound="InstanceUsage")


@_attrs_define
class InstanceUsage:
    """Usage data for this instance.

    Attributes:
        users (InstanceUsageUsers): Usage data related to users on this instance.

    """

    users: "InstanceUsageUsers"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        users = self.users.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "users": users,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.instance_usage_users import InstanceUsageUsers

        d = dict(src_dict)
        users = InstanceUsageUsers.from_dict(d.pop("users"))

        instance_usage = cls(
            users=users,
        )

        instance_usage.additional_properties = d
        return instance_usage

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
