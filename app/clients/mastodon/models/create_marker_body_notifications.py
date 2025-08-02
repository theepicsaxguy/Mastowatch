from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="CreateMarkerBodyNotifications")


@_attrs_define
class CreateMarkerBodyNotifications:
    """Object containing properties

    Attributes:
        last_read_id (Union[Unset, str]): ID of the last notification read.
    """

    last_read_id: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        last_read_id = self.last_read_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if last_read_id is not UNSET:
            field_dict["last_read_id"] = last_read_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        last_read_id = d.pop("last_read_id", UNSET)

        create_marker_body_notifications = cls(
            last_read_id=last_read_id,
        )

        create_marker_body_notifications.additional_properties = d
        return create_marker_body_notifications

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
