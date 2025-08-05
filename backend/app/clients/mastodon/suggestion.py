from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    TypeVar,
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.suggestion_sources_item import SuggestionSourcesItem

if TYPE_CHECKING:
    from ..models.account import Account


T = TypeVar("T", bound="Suggestion")


@_attrs_define
class Suggestion:
    """Represents a suggested account to follow and an associated reason for the suggestion.

    Attributes:
        account (Account): Represents a user of Mastodon and their associated profile.
        sources (list[SuggestionSourcesItem]): A list of reasons this account is being suggested. This replaces `source`
    """

    account: "Account"
    sources: list[SuggestionSourcesItem]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        account = self.account.to_dict()

        sources = []
        for sources_item_data in self.sources:
            sources_item = sources_item_data.value
            sources.append(sources_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "account": account,
                "sources": sources,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.account import Account

        d = dict(src_dict)
        account = Account.from_dict(d.pop("account"))

        sources = []
        _sources = d.pop("sources")
        for sources_item_data in _sources:
            sources_item = SuggestionSourcesItem(sources_item_data)

            sources.append(sources_item)

        suggestion = cls(
            account=account,
            sources=sources,
        )

        suggestion.additional_properties = d
        return suggestion

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
