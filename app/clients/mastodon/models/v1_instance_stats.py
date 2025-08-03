from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="V1InstanceStats")


@_attrs_define
class V1InstanceStats:
    """Statistics about how much information the instance contains.

    Attributes:
        domain_count (int): Total domains discovered by this instance.
        status_count (int): Total statuses on this instance.
        user_count (int): Total users on this instance.

    """

    domain_count: int
    status_count: int
    user_count: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        domain_count = self.domain_count

        status_count = self.status_count

        user_count = self.user_count

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "domain_count": domain_count,
                "status_count": status_count,
                "user_count": user_count,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        domain_count = d.pop("domain_count")

        status_count = d.pop("status_count")

        user_count = d.pop("user_count")

        v1_instance_stats = cls(
            domain_count=domain_count,
            status_count=status_count,
            user_count=user_count,
        )

        v1_instance_stats.additional_properties = d
        return v1_instance_stats

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
