import datetime
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

T = TypeVar("T", bound="Marker")


@_attrs_define
class Marker:
    """Represents the last read position within a user's timelines.

    Example:
        {'last_read_id': '103194548672408537', 'version': 462, 'updated_at': '2019-11-24T19:39:39.337Z'}

    Attributes:
        last_read_id (str): The ID of the most recently viewed entity.
        updated_at (datetime.datetime): The timestamp of when the marker was set.
        version (int): An incrementing counter, used for locking to prevent write conflicts.
    """

    last_read_id: str
    updated_at: datetime.datetime
    version: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        last_read_id = self.last_read_id

        updated_at = self.updated_at.isoformat()

        version = self.version

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "last_read_id": last_read_id,
                "updated_at": updated_at,
                "version": version,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        last_read_id = d.pop("last_read_id")

        updated_at = isoparse(d.pop("updated_at"))

        version = d.pop("version")

        marker = cls(
            last_read_id=last_read_id,
            updated_at=updated_at,
            version=version,
        )

        marker.additional_properties = d
        return marker

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
