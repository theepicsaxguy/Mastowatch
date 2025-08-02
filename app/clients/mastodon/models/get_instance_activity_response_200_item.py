from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="GetInstanceActivityResponse200Item")


@_attrs_define
class GetInstanceActivityResponse200Item:
    """
    Attributes:
        week (Union[Unset, str]): Midnight at the first day of the week.
        statuses (Union[Unset, str]): The number of Statuses created since the week began.
        logins (Union[Unset, str]): The number of user logins since the week began.
        registrations (Union[Unset, str]): The number of user registrations since the week began.
    """

    week: Union[Unset, str] = UNSET
    statuses: Union[Unset, str] = UNSET
    logins: Union[Unset, str] = UNSET
    registrations: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        week = self.week

        statuses = self.statuses

        logins = self.logins

        registrations = self.registrations

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if week is not UNSET:
            field_dict["week"] = week
        if statuses is not UNSET:
            field_dict["statuses"] = statuses
        if logins is not UNSET:
            field_dict["logins"] = logins
        if registrations is not UNSET:
            field_dict["registrations"] = registrations

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        week = d.pop("week", UNSET)

        statuses = d.pop("statuses", UNSET)

        logins = d.pop("logins", UNSET)

        registrations = d.pop("registrations", UNSET)

        get_instance_activity_response_200_item = cls(
            week=week,
            statuses=statuses,
            logins=logins,
            registrations=registrations,
        )

        get_instance_activity_response_200_item.additional_properties = d
        return get_instance_activity_response_200_item

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
