from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="AdminEmailDomainBlockHistory")


@_attrs_define
class AdminEmailDomainBlockHistory:
    """Nested entity extracted from Admin::EmailDomainBlock.history

    Attributes:
        accounts (str): The counted accounts signup attempts using that email domain within that day.
        day (str): UNIX timestamp on midnight of the given day.
        uses (str): The counted IP signup attempts of that email domain within that day.
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
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        accounts = d.pop("accounts")

        day = d.pop("day")

        uses = d.pop("uses")

        admin_email_domain_block_history = cls(
            accounts=accounts,
            day=day,
            uses=uses,
        )

        admin_email_domain_block_history.additional_properties = d
        return admin_email_domain_block_history

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
