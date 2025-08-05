from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="StatusSource")


@_attrs_define
class StatusSource:
    """Represents a status's source as plain text.

    Example:
        {'id': '108942703571991143', 'text': 'this is a status that will be edited', 'spoiler_text': ''}

    Attributes:
        id (str): ID of the status in the database.
        spoiler_text (str): The plain text used to compose the status's subject or content warning.
        text (str): The plain text used to compose the status.
    """

    id: str
    spoiler_text: str
    text: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        spoiler_text = self.spoiler_text

        text = self.text

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "spoiler_text": spoiler_text,
                "text": text,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        spoiler_text = d.pop("spoiler_text")

        text = d.pop("text")

        status_source = cls(
            id=id,
            spoiler_text=spoiler_text,
            text=text,
        )

        status_source.additional_properties = d
        return status_source

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
