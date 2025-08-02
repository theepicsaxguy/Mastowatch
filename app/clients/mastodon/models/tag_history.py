from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="TagHistory")


@_attrs_define
class TagHistory:
    """Nested entity extracted from Tag.history

    Attributes:
        accounts (str): The total of accounts using the tag within that day.
        day (str): UNIX timestamp on midnight of the given day.
        uses (str): The counted usage of the tag within that day.
    """

    accounts: str
    day: str
    uses: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        accounts = self.accounts

        day = self.day

        uses = self.uses

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "accounts": accounts,
                "day": day,
                "uses": uses,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        accounts = d.pop("accounts")

        day = d.pop("day")

        uses = d.pop("uses")

        tag_history = cls(
            accounts=accounts,
            day=day,
            uses=uses,
        )

        tag_history.additional_properties = d
        return tag_history

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
