from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="InstanceConfigurationAccounts")


@_attrs_define
class InstanceConfigurationAccounts:
    """Limits related to accounts.

    Attributes:
        max_featured_tags (int): The maximum number of featured tags allowed for each account.
        max_pinned_statuses (int): The maximum number of pinned statuses for each account.

    """

    max_featured_tags: int
    max_pinned_statuses: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        max_featured_tags = self.max_featured_tags

        max_pinned_statuses = self.max_pinned_statuses

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "max_featured_tags": max_featured_tags,
                "max_pinned_statuses": max_pinned_statuses,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        max_featured_tags = d.pop("max_featured_tags")

        max_pinned_statuses = d.pop("max_pinned_statuses")

        instance_configuration_accounts = cls(
            max_featured_tags=max_featured_tags,
            max_pinned_statuses=max_pinned_statuses,
        )

        instance_configuration_accounts.additional_properties = d
        return instance_configuration_accounts

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
