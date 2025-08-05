from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
    Union,
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="PostAccountMuteBody")


@_attrs_define
class PostAccountMuteBody:
    """
    Attributes:
        duration (Union[Unset, int]): How long the mute should last, in seconds. Defaults to 0 (indefinite). Default: 0.
        notifications (Union[Unset, bool]): Mute notifications in addition to statuses? Defaults to true. Default: True.
    """

    duration: Union[Unset, int] = 0
    notifications: Union[Unset, bool] = True
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        duration = self.duration

        notifications = self.notifications

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if duration is not UNSET:
            field_dict["duration"] = duration
        if notifications is not UNSET:
            field_dict["notifications"] = notifications

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        duration = d.pop("duration", UNSET)

        notifications = d.pop("notifications", UNSET)

        post_account_mute_body = cls(
            duration=duration,
            notifications=notifications,
        )

        post_account_mute_body.additional_properties = d
        return post_account_mute_body

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
