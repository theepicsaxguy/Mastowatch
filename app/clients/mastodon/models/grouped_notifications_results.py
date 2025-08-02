from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.account import Account
    from ..models.notification_group import NotificationGroup
    from ..models.partial_account_with_avatar import PartialAccountWithAvatar
    from ..models.status import Status


T = TypeVar("T", bound="GroupedNotificationsResults")


@_attrs_define
class GroupedNotificationsResults:
    """### Attributes

    Attributes:
        accounts (list['Account']): Accounts referenced by grouped notifications.
        notification_groups (NotificationGroup): ### Attributes
        statuses (list['Status']): Statuses referenced by grouped notifications.
        partial_accounts (Union[None, Unset, list['PartialAccountWithAvatar']]): Partial accounts referenced by grouped
            notifications. Those are only returned when requesting grouped notifications with
            `expand_accounts=partial_avatars`.
    """

    accounts: list["Account"]
    notification_groups: "NotificationGroup"
    statuses: list["Status"]
    partial_accounts: Union[None, Unset, list["PartialAccountWithAvatar"]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        accounts = []
        for accounts_item_data in self.accounts:
            accounts_item = accounts_item_data.to_dict()
            accounts.append(accounts_item)

        notification_groups = self.notification_groups.to_dict()

        statuses = []
        for statuses_item_data in self.statuses:
            statuses_item = statuses_item_data.to_dict()
            statuses.append(statuses_item)

        partial_accounts: Union[None, Unset, list[dict[str, Any]]]
        if isinstance(self.partial_accounts, Unset):
            partial_accounts = UNSET
        elif isinstance(self.partial_accounts, list):
            partial_accounts = []
            for partial_accounts_type_0_item_data in self.partial_accounts:
                partial_accounts_type_0_item = (
                    partial_accounts_type_0_item_data.to_dict()
                )
                partial_accounts.append(partial_accounts_type_0_item)

        else:
            partial_accounts = self.partial_accounts

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "accounts": accounts,
                "notification_groups": notification_groups,
                "statuses": statuses,
            }
        )
        if partial_accounts is not UNSET:
            field_dict["partial_accounts"] = partial_accounts

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.account import Account
        from ..models.notification_group import NotificationGroup
        from ..models.partial_account_with_avatar import PartialAccountWithAvatar
        from ..models.status import Status

        d = src_dict.copy()
        accounts = []
        _accounts = d.pop("accounts")
        for accounts_item_data in _accounts:
            accounts_item = Account.from_dict(accounts_item_data)

            accounts.append(accounts_item)

        notification_groups = NotificationGroup.from_dict(d.pop("notification_groups"))

        statuses = []
        _statuses = d.pop("statuses")
        for statuses_item_data in _statuses:
            statuses_item = Status.from_dict(statuses_item_data)

            statuses.append(statuses_item)

        def _parse_partial_accounts(
            data: object,
        ) -> Union[None, Unset, list["PartialAccountWithAvatar"]]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                partial_accounts_type_0 = []
                _partial_accounts_type_0 = data
                for partial_accounts_type_0_item_data in _partial_accounts_type_0:
                    partial_accounts_type_0_item = PartialAccountWithAvatar.from_dict(
                        partial_accounts_type_0_item_data
                    )

                    partial_accounts_type_0.append(partial_accounts_type_0_item)

                return partial_accounts_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, list["PartialAccountWithAvatar"]], data)

        partial_accounts = _parse_partial_accounts(d.pop("partial_accounts", UNSET))

        grouped_notifications_results = cls(
            accounts=accounts,
            notification_groups=notification_groups,
            statuses=statuses,
            partial_accounts=partial_accounts,
        )

        grouped_notifications_results.additional_properties = d
        return grouped_notifications_results

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
