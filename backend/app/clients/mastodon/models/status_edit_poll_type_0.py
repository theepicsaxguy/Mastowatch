from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    TypeVar,
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.status_edit_poll_type_0_options_item import (
        StatusEditPollType0OptionsItem,
    )


T = TypeVar("T", bound="StatusEditPollType0")


@_attrs_define
class StatusEditPollType0:
    """The current state of the poll options at this revision. Note that edits changing the poll options will be collapsed
    together into one edit, since this action resets the poll.

        Attributes:
            options (list['StatusEditPollType0OptionsItem']): The poll options at this revision.
    """

    options: list["StatusEditPollType0OptionsItem"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        options = []
        for options_item_data in self.options:
            options_item = options_item_data.to_dict()
            options.append(options_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "options": options,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.status_edit_poll_type_0_options_item import (
            StatusEditPollType0OptionsItem,
        )

        d = dict(src_dict)
        options = []
        _options = d.pop("options")
        for options_item_data in _options:
            options_item = StatusEditPollType0OptionsItem.from_dict(options_item_data)

            options.append(options_item)

        status_edit_poll_type_0 = cls(
            options=options,
        )

        status_edit_poll_type_0.additional_properties = d
        return status_edit_poll_type_0

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
