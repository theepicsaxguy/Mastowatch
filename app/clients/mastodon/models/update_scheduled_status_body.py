import datetime
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="UpdateScheduledStatusBody")


@_attrs_define
class UpdateScheduledStatusBody:
    """
    Attributes:
        scheduled_at (Union[Unset, datetime.datetime]): [Datetime] at which the status will be published. Must be at
            least 5 minutes into the future.
    """

    scheduled_at: Union[Unset, datetime.datetime] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        scheduled_at: Union[Unset, str] = UNSET
        if not isinstance(self.scheduled_at, Unset):
            scheduled_at = self.scheduled_at.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if scheduled_at is not UNSET:
            field_dict["scheduled_at"] = scheduled_at

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        _scheduled_at = d.pop("scheduled_at", UNSET)
        scheduled_at: Union[Unset, datetime.datetime]
        if isinstance(_scheduled_at, Unset):
            scheduled_at = UNSET
        else:
            scheduled_at = isoparse(_scheduled_at)

        update_scheduled_status_body = cls(
            scheduled_at=scheduled_at,
        )

        update_scheduled_status_body.additional_properties = d
        return update_scheduled_status_body

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
