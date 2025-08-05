import datetime
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
from dateutil.parser import isoparse

from ..models.account_warning_action import AccountWarningAction
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.account import Account
    from ..models.appeal import Appeal


T = TypeVar("T", bound="AccountWarning")


@_attrs_define
class AccountWarning:
    """Moderation warning against a particular account.

    Attributes:
        action (AccountWarningAction): Action taken against the account.
        created_at (datetime.datetime): When the event took place.
        id (str): The ID of the account warning.
        target_account (Account): Represents a user of Mastodon and their associated profile.
        text (str): Message from the moderator to the target account.
        appeal (Union['Appeal', None, Unset]): Appeal submitted by the target account, if any.
        status_ids (Union[None, Unset, list[str]]): List of status IDs that are relevant to the warning. When `action`
            is `mark_statuses_as_sensitive` or `delete_statuses`, those are the affected statuses. If the action is
            `delete_statuses` then they have been irrevocably deleted (irrespective of the appeal state), and will be
            inaccessible to the client.
    """

    action: AccountWarningAction
    created_at: datetime.datetime
    id: str
    target_account: "Account"
    text: str
    appeal: Union["Appeal", None, Unset] = UNSET
    status_ids: Union[None, Unset, list[str]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.appeal import Appeal

        action = self.action.value

        created_at = self.created_at.isoformat()

        id = self.id

        target_account = self.target_account.to_dict()

        text = self.text

        appeal: Union[None, Unset, dict[str, Any]]
        if isinstance(self.appeal, Unset):
            appeal = UNSET
        elif isinstance(self.appeal, Appeal):
            appeal = self.appeal.to_dict()
        else:
            appeal = self.appeal

        status_ids: Union[None, Unset, list[str]]
        if isinstance(self.status_ids, Unset):
            status_ids = UNSET
        elif isinstance(self.status_ids, list):
            status_ids = self.status_ids

        else:
            status_ids = self.status_ids

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "action": action,
                "created_at": created_at,
                "id": id,
                "target_account": target_account,
                "text": text,
            }
        )
        if appeal is not UNSET:
            field_dict["appeal"] = appeal
        if status_ids is not UNSET:
            field_dict["status_ids"] = status_ids

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.account import Account
        from ..models.appeal import Appeal

        d = dict(src_dict)
        action = AccountWarningAction(d.pop("action"))

        created_at = isoparse(d.pop("created_at"))

        id = d.pop("id")

        target_account = Account.from_dict(d.pop("target_account"))

        text = d.pop("text")

        def _parse_appeal(data: object) -> Union["Appeal", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                appeal_type_0 = Appeal.from_dict(data)

                return appeal_type_0
            except:  # noqa: E722
                pass
            return cast(Union["Appeal", None, Unset], data)

        appeal = _parse_appeal(d.pop("appeal", UNSET))

        def _parse_status_ids(data: object) -> Union[None, Unset, list[str]]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                status_ids_type_0 = cast(list[str], data)

                return status_ids_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, list[str]], data)

        status_ids = _parse_status_ids(d.pop("status_ids", UNSET))

        account_warning = cls(
            action=action,
            created_at=created_at,
            id=id,
            target_account=target_account,
            text=text,
            appeal=appeal,
            status_ids=status_ids,
        )

        account_warning.additional_properties = d
        return account_warning

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
