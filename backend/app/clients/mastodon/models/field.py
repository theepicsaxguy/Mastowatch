import datetime
from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
    Union,
    cast,
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="Field")


@_attrs_define
class Field:
    """Additional entity definition for Field

    Attributes:
        name (str): The key of a given field's key-value pair.
        value (str): The value associated with the `name` key.
        verified_at (Union[None, Unset, datetime.datetime]): Timestamp of when the server verified a URL value for a
            rel="me" link.
    """

    name: str
    value: str
    verified_at: Union[None, Unset, datetime.datetime] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        value = self.value

        verified_at: Union[None, Unset, str]
        if isinstance(self.verified_at, Unset):
            verified_at = UNSET
        elif isinstance(self.verified_at, datetime.datetime):
            verified_at = self.verified_at.isoformat()
        else:
            verified_at = self.verified_at

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "value": value,
            }
        )
        if verified_at is not UNSET:
            field_dict["verified_at"] = verified_at

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name")

        value = d.pop("value")

        def _parse_verified_at(data: object) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                verified_at_type_0 = isoparse(data)

                return verified_at_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

        verified_at = _parse_verified_at(d.pop("verified_at", UNSET))

        field = cls(
            name=name,
            value=value,
            verified_at=verified_at,
        )

        field.additional_properties = d
        return field

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
