from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.account import Account


T = TypeVar("T", bound="PreviewCardAuthor")


@_attrs_define
class PreviewCardAuthor:
    """Represents an author in a rich preview card.

    Attributes:
        name (str): The original resource author's name. Replaces the deprecated `author_name` attribute of the preview
            card.
        url (str): A link to the author of the original resource. Replaces the deprecated `author_url` attribute of the
            preview card.
        account (Union['Account', None, Unset]): The fediverse account of the author.

    """

    name: str
    url: str
    account: Union["Account", None, Unset] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.account import Account

        name = self.name

        url = self.url

        account: None | Unset | dict[str, Any]
        if isinstance(self.account, Unset):
            account = UNSET
        elif isinstance(self.account, Account):
            account = self.account.to_dict()
        else:
            account = self.account

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "url": url,
            }
        )
        if account is not UNSET:
            field_dict["account"] = account

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.account import Account

        d = dict(src_dict)
        name = d.pop("name")

        url = d.pop("url")

        def _parse_account(data: object) -> Union["Account", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                account_type_0 = Account.from_dict(data)

                return account_type_0
            except:  # noqa: E722
                pass
            return cast(Union["Account", None, Unset], data)

        account = _parse_account(d.pop("account", UNSET))

        preview_card_author = cls(
            name=name,
            url=url,
            account=account,
        )

        preview_card_author.additional_properties = d
        return preview_card_author

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
