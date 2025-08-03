from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="ScheduledStatusParamsPollType0")


@_attrs_define
class ScheduledStatusParamsPollType0:
    """Poll to be attached to the status.

    Attributes:
        options (list[str]): The poll options to be used.
        expires_in (int): How many seconds the poll should last before closing.
        multiple (bool): Whether the poll allows multiple choices.
        hide_totals (bool): Whether the poll should hide total votes until after voting has ended.

    """

    options: list[str]
    expires_in: int
    multiple: bool
    hide_totals: bool
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        options = self.options

        expires_in = self.expires_in

        multiple = self.multiple

        hide_totals = self.hide_totals

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "options": options,
                "expires_in": expires_in,
                "multiple": multiple,
                "hide_totals": hide_totals,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        options = cast(list[str], d.pop("options"))

        expires_in = d.pop("expires_in")

        multiple = d.pop("multiple")

        hide_totals = d.pop("hide_totals")

        scheduled_status_params_poll_type_0 = cls(
            options=options,
            expires_in=expires_in,
            multiple=multiple,
            hide_totals=hide_totals,
        )

        scheduled_status_params_poll_type_0.additional_properties = d
        return scheduled_status_params_poll_type_0

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
