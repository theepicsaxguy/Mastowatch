from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
    Union,
    cast,
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="UpdateStatusBodyPoll")


@_attrs_define
class UpdateStatusBodyPoll:
    """Object containing properties

    Attributes:
        options (Union[Unset, list[str]]): Possible answers to the poll. If provided, `media_ids` cannot be used, and
            `poll[expires_in]` must be provided.
        expires_in (Union[Unset, int]): Duration that the poll should be open, in seconds. If provided, `media_ids`
            cannot be used, and `poll[options]` must be provided.
        multiple (Union[Unset, bool]): Allow multiple choices? Defaults to false.
        hide_totals (Union[Unset, bool]): Hide vote counts until the poll ends? Defaults to false.
    """

    options: Union[Unset, list[str]] = UNSET
    expires_in: Union[Unset, int] = UNSET
    multiple: Union[Unset, bool] = UNSET
    hide_totals: Union[Unset, bool] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        options: Union[Unset, list[str]] = UNSET
        if not isinstance(self.options, Unset):
            options = self.options

        expires_in = self.expires_in

        multiple = self.multiple

        hide_totals = self.hide_totals

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if options is not UNSET:
            field_dict["options"] = options
        if expires_in is not UNSET:
            field_dict["expires_in"] = expires_in
        if multiple is not UNSET:
            field_dict["multiple"] = multiple
        if hide_totals is not UNSET:
            field_dict["hide_totals"] = hide_totals

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        options = cast(list[str], d.pop("options", UNSET))

        expires_in = d.pop("expires_in", UNSET)

        multiple = d.pop("multiple", UNSET)

        hide_totals = d.pop("hide_totals", UNSET)

        update_status_body_poll = cls(
            options=options,
            expires_in=expires_in,
            multiple=multiple,
            hide_totals=hide_totals,
        )

        update_status_body_poll.additional_properties = d
        return update_status_body_poll

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
