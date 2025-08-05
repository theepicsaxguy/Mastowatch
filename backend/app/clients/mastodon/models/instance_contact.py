from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    TypeVar,
    Union,
    cast,
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.account import Account


T = TypeVar("T", bound="InstanceContact")


@_attrs_define
class InstanceContact:
    """Hints related to contacting a representative of the website.

    Attributes:
        email (str): An email address that can be messaged regarding inquiries or issues.
        account (Union['Account', None, Unset]): An account that can be contacted natively over the network regarding
            inquiries or issues.
    """

    email: str
    account: Union["Account", None, Unset] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.account import Account

        email = self.email

        account: Union[None, Unset, dict[str, Any]]
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
                "email": email,
            }
        )
        if account is not UNSET:
            field_dict["account"] = account

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.account import Account

        d = dict(src_dict)
        email = d.pop("email")

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

        instance_contact = cls(
            email=email,
            account=account,
        )

        instance_contact.additional_properties = d
        return instance_contact

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
