from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.account import Account


T = TypeVar("T", bound="FamiliarFollowers")


@_attrs_define
class FamiliarFollowers:
    """Represents a subset of your follows who also follow some other user.

    Example:
        [{'id': '1', 'accounts': [{'id': '1087990', 'username': 'moss', 'acct': 'moss@goblin.camp'}, {'id': '1092723',
            'username': 'vivianrose', 'acct': 'vivianrose'}]}, {'id': '2', 'accounts': []}]

    Attributes:
        accounts (list['Account']): Accounts you follow that also follow this account.
        id (str): The ID of the Account in the database.

    """

    accounts: list["Account"]
    id: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        accounts = []
        for accounts_item_data in self.accounts:
            accounts_item = accounts_item_data.to_dict()
            accounts.append(accounts_item)

        id = self.id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "accounts": accounts,
                "id": id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.account import Account

        d = dict(src_dict)
        accounts = []
        _accounts = d.pop("accounts")
        for accounts_item_data in _accounts:
            accounts_item = Account.from_dict(accounts_item_data)

            accounts.append(accounts_item)

        id = d.pop("id")

        familiar_followers = cls(
            accounts=accounts,
            id=id,
        )

        familiar_followers.additional_properties = d
        return familiar_followers

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
