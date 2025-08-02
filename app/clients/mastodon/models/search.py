from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.account import Account
    from ..models.status import Status
    from ..models.tag import Tag


T = TypeVar("T", bound="Search")


@_attrs_define
class Search:
    """Represents the results of a search.

    Attributes:
        accounts (list['Account']): Accounts which match the given query
        hashtags (list['Tag']): Hashtags which match the given query
        statuses (list['Status']): Statuses which match the given query
    """

    accounts: list["Account"]
    hashtags: list["Tag"]
    statuses: list["Status"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        accounts = []
        for accounts_item_data in self.accounts:
            accounts_item = accounts_item_data.to_dict()
            accounts.append(accounts_item)

        hashtags = []
        for hashtags_item_data in self.hashtags:
            hashtags_item = hashtags_item_data.to_dict()
            hashtags.append(hashtags_item)

        statuses = []
        for statuses_item_data in self.statuses:
            statuses_item = statuses_item_data.to_dict()
            statuses.append(statuses_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "accounts": accounts,
                "hashtags": hashtags,
                "statuses": statuses,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.account import Account
        from ..models.status import Status
        from ..models.tag import Tag

        d = src_dict.copy()
        accounts = []
        _accounts = d.pop("accounts")
        for accounts_item_data in _accounts:
            accounts_item = Account.from_dict(accounts_item_data)

            accounts.append(accounts_item)

        hashtags = []
        _hashtags = d.pop("hashtags")
        for hashtags_item_data in _hashtags:
            hashtags_item = Tag.from_dict(hashtags_item_data)

            hashtags.append(hashtags_item)

        statuses = []
        _statuses = d.pop("statuses")
        for statuses_item_data in _statuses:
            statuses_item = Status.from_dict(statuses_item_data)

            statuses.append(statuses_item)

        search = cls(
            accounts=accounts,
            hashtags=hashtags,
            statuses=statuses,
        )

        search.additional_properties = d
        return search

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
