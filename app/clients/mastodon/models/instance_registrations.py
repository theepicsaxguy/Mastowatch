from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="InstanceRegistrations")


@_attrs_define
class InstanceRegistrations:
    """Information about registering for this website.

    Attributes:
        approval_required (bool): Whether registrations require moderator approval.
        enabled (bool): Whether registrations are enabled.
        message (Union[None, Unset, str]): A custom message to be shown when registrations are closed.
        min_age (Union[None, Unset, int]): A minimum age required to register, if configured.
        reason_required (Union[None, Unset, bool]): Whether registrations require the user to provide a reason for
            joining. Only applicable when `registrations[approval_required]` is true.
    """

    approval_required: bool
    enabled: bool
    message: Union[None, Unset, str] = UNSET
    min_age: Union[None, Unset, int] = UNSET
    reason_required: Union[None, Unset, bool] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        approval_required = self.approval_required

        enabled = self.enabled

        message: Union[None, Unset, str]
        if isinstance(self.message, Unset):
            message = UNSET
        else:
            message = self.message

        min_age: Union[None, Unset, int]
        if isinstance(self.min_age, Unset):
            min_age = UNSET
        else:
            min_age = self.min_age

        reason_required: Union[None, Unset, bool]
        if isinstance(self.reason_required, Unset):
            reason_required = UNSET
        else:
            reason_required = self.reason_required

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "approval_required": approval_required,
                "enabled": enabled,
            }
        )
        if message is not UNSET:
            field_dict["message"] = message
        if min_age is not UNSET:
            field_dict["min_age"] = min_age
        if reason_required is not UNSET:
            field_dict["reason_required"] = reason_required

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        approval_required = d.pop("approval_required")

        enabled = d.pop("enabled")

        def _parse_message(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        message = _parse_message(d.pop("message", UNSET))

        def _parse_min_age(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        min_age = _parse_min_age(d.pop("min_age", UNSET))

        def _parse_reason_required(data: object) -> Union[None, Unset, bool]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, bool], data)

        reason_required = _parse_reason_required(d.pop("reason_required", UNSET))

        instance_registrations = cls(
            approval_required=approval_required,
            enabled=enabled,
            message=message,
            min_age=min_age,
            reason_required=reason_required,
        )

        instance_registrations.additional_properties = d
        return instance_registrations

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
