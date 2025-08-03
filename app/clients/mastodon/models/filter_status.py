from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="FilterStatus")


@_attrs_define
class FilterStatus:
    """Represents a status ID that, if matched, should cause the filter action to be taken.

    Example:
        {'id': '1', 'status_id': '109031743575371913'}

    Attributes:
        id (str): The ID of the FilterStatus in the database.
        status_id (str): The ID of the Status that will be filtered.

    """

    id: str
    status_id: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        status_id = self.status_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "status_id": status_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        status_id = d.pop("status_id")

        filter_status = cls(
            id=id,
            status_id=status_id,
        )

        filter_status.additional_properties = d
        return filter_status

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
