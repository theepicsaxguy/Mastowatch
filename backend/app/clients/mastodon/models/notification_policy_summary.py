from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="NotificationPolicySummary")


@_attrs_define
class NotificationPolicySummary:
    """Summary of the filtered notifications

    Attributes:
        pending_notifications_count (int): Number of total non-dismissed filtered notifications. May be inaccurate.
        pending_requests_count (int): Number of different accounts from which the user has non-dismissed filtered
            notifications. Capped at 100.
    """

    pending_notifications_count: int
    pending_requests_count: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        pending_notifications_count = self.pending_notifications_count

        pending_requests_count = self.pending_requests_count

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "pending_notifications_count": pending_notifications_count,
                "pending_requests_count": pending_requests_count,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        pending_notifications_count = d.pop("pending_notifications_count")

        pending_requests_count = d.pop("pending_requests_count")

        notification_policy_summary = cls(
            pending_notifications_count=pending_notifications_count,
            pending_requests_count=pending_requests_count,
        )

        notification_policy_summary.additional_properties = d
        return notification_policy_summary

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
