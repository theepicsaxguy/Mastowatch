from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.account import Account
    from ..models.status import Status


T = TypeVar("T", bound="Conversation")


@_attrs_define
class Conversation:
    """Represents a conversation with "direct message" visibility.

    Example:
        {'id': '418450', 'unread': True, 'accounts': [{'id': '482403', 'username': 'amic', 'acct': 'amic@nulled.red'}],
            'last_status': {'id': '103196583826321184', 'created_at': '2019-11-25T04:08:24.000Z', 'in_reply_to_id':
            '103196540587943467', 'in_reply_to_account_id': '14715'}}

    Attributes:
        accounts (list['Account']): Participants in the conversation.
        id (str): The ID of the conversation in the database.
        unread (bool): Is the conversation currently marked as unread?
        last_status (Union['Status', None, Unset]): The last status in the conversation.

    """

    accounts: list["Account"]
    id: str
    unread: bool
    last_status: Union["Status", None, Unset] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.status import Status

        accounts = []
        for accounts_item_data in self.accounts:
            accounts_item = accounts_item_data.to_dict()
            accounts.append(accounts_item)

        id = self.id

        unread = self.unread

        last_status: None | Unset | dict[str, Any]
        if isinstance(self.last_status, Unset):
            last_status = UNSET
        elif isinstance(self.last_status, Status):
            last_status = self.last_status.to_dict()
        else:
            last_status = self.last_status

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "accounts": accounts,
                "id": id,
                "unread": unread,
            }
        )
        if last_status is not UNSET:
            field_dict["last_status"] = last_status

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.account import Account
        from ..models.status import Status

        d = dict(src_dict)
        accounts = []
        _accounts = d.pop("accounts")
        for accounts_item_data in _accounts:
            accounts_item = Account.from_dict(accounts_item_data)

            accounts.append(accounts_item)

        id = d.pop("id")

        unread = d.pop("unread")

        def _parse_last_status(data: object) -> Union["Status", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                last_status_type_0 = Status.from_dict(data)

                return last_status_type_0
            except:  # noqa: E722
                pass
            return cast(Union["Status", None, Unset], data)

        last_status = _parse_last_status(d.pop("last_status", UNSET))

        conversation = cls(
            accounts=accounts,
            id=id,
            unread=unread,
            last_status=last_status,
        )

        conversation.additional_properties = d
        return conversation

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
