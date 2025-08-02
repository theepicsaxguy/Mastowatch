import datetime
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.category_enum import CategoryEnum
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.admin_account import AdminAccount
    from ..models.rule import Rule
    from ..models.status import Status


T = TypeVar("T", bound="AdminReport")


@_attrs_define
class AdminReport:
    """Admin-level information about a filed report.

    Example:
        {'id': '1', 'action_taken': False, 'action_taken_at': None, 'category': 'spam', 'comment': '', 'forwarded':
            False, 'created_at': '2022-09-09T21:19:23.085Z', 'updated_at': '2022-09-09T21:19:23.085Z', 'account': {'id':
            '108965218747268792', 'username': 'admin', 'domain': None, 'created_at': '2022-09-08T22:48:07.985Z', 'email':
            'admin@mastodon.local', 'account': {'id': '108965218747268792', 'username': 'admin', 'acct': 'admin'}},
            'target_account': {'id': '108965430868193066', 'username': 'goody', 'domain': None, 'created_at':
            '2022-09-08T23:42:04.731Z', 'email': 'goody@mastodon.local', 'account': {'id': '108965430868193066', 'username':
            'goody', 'acct': 'goody'}}, 'assigned_account': None, 'action_taken_by_account': None, 'statuses': [], 'rules':
            []}

    Attributes:
        account (AdminAccount): Admin-level information about a given account. Example: {'id': '108965278956942133',
            'username': 'admin', 'domain': None, 'created_at': '2022-09-08T23:03:26.762Z', 'email': 'admin@mastodon.local',
            'ip': '192.168.42.1', 'role': {'id': 3, 'name': 'Owner', 'color': '', 'position': 1000, 'permissions': 1,
            'highlighted': True, 'created_at': '2022-09-08T22:48:07.983Z', 'updated_at': '2022-09-08T22:48:07.983Z'},
            'confirmed': True, 'suspended': False, 'silenced': False, 'disabled': False, 'approved': True, 'locale': None,
            'invite_request': None, 'ips': [{'ip': '192.168.42.1', 'used_at': '2022-09-15T01:38:58.851Z'}], 'account':
            {'id': '108965278956942133', 'username': 'admin', 'acct': 'admin', 'display_name': '', 'locked': False, 'bot':
            False, 'discoverable': None, 'group': False, 'created_at': '2022-09-08T00:00:00.000Z', 'note': '', 'url':
            'http://mastodon.local/@admin', 'avatar': 'http://mastodon.local/avatars/original/missing.png', 'avatar_static':
            'http://mastodon.local/avatars/original/missing.png', 'header':
            'http://mastodon.local/headers/original/missing.png', 'header_static':
            'http://mastodon.local/headers/original/missing.png', 'followers_count': 0, 'following_count': 0,
            'statuses_count': 0, 'last_status_at': None, 'emojis': [], 'fields': []}}.
        action_taken (bool): Whether an action was taken to resolve this report.
        category (CategoryEnum):
        comment (str): An optional reason for reporting.
        created_at (datetime.datetime): The time the report was filed.
        forwarded (bool): Whether a report was forwarded to a remote instance.
        id (str): The ID of the report in the database.
        rules (list['Rule']): Rules attached to the report, for context.
        statuses (list['Status']): Statuses attached to the report, for context.
        target_account (AdminAccount): Admin-level information about a given account. Example: {'id':
            '108965278956942133', 'username': 'admin', 'domain': None, 'created_at': '2022-09-08T23:03:26.762Z', 'email':
            'admin@mastodon.local', 'ip': '192.168.42.1', 'role': {'id': 3, 'name': 'Owner', 'color': '', 'position': 1000,
            'permissions': 1, 'highlighted': True, 'created_at': '2022-09-08T22:48:07.983Z', 'updated_at':
            '2022-09-08T22:48:07.983Z'}, 'confirmed': True, 'suspended': False, 'silenced': False, 'disabled': False,
            'approved': True, 'locale': None, 'invite_request': None, 'ips': [{'ip': '192.168.42.1', 'used_at':
            '2022-09-15T01:38:58.851Z'}], 'account': {'id': '108965278956942133', 'username': 'admin', 'acct': 'admin',
            'display_name': '', 'locked': False, 'bot': False, 'discoverable': None, 'group': False, 'created_at':
            '2022-09-08T00:00:00.000Z', 'note': '', 'url': 'http://mastodon.local/@admin', 'avatar':
            'http://mastodon.local/avatars/original/missing.png', 'avatar_static':
            'http://mastodon.local/avatars/original/missing.png', 'header':
            'http://mastodon.local/headers/original/missing.png', 'header_static':
            'http://mastodon.local/headers/original/missing.png', 'followers_count': 0, 'following_count': 0,
            'statuses_count': 0, 'last_status_at': None, 'emojis': [], 'fields': []}}.
        updated_at (datetime.datetime): The time of last action on this report.
        action_taken_at (Union[None, Unset, datetime.datetime]): When an action was taken, if this report is currently
            resolved.
        action_taken_by_account (Union['AdminAccount', None, Unset]): The account of the moderator who handled the
            report.
        assigned_account (Union['AdminAccount', None, Unset]): The account of the moderator assigned to this report.
    """

    account: "AdminAccount"
    action_taken: bool
    category: CategoryEnum
    comment: str
    created_at: datetime.datetime
    forwarded: bool
    id: str
    rules: list["Rule"]
    statuses: list["Status"]
    target_account: "AdminAccount"
    updated_at: datetime.datetime
    action_taken_at: Union[None, Unset, datetime.datetime] = UNSET
    action_taken_by_account: Union["AdminAccount", None, Unset] = UNSET
    assigned_account: Union["AdminAccount", None, Unset] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.admin_account import AdminAccount

        account = self.account.to_dict()

        action_taken = self.action_taken

        category = self.category.value

        comment = self.comment

        created_at = self.created_at.isoformat()

        forwarded = self.forwarded

        id = self.id

        rules = []
        for rules_item_data in self.rules:
            rules_item = rules_item_data.to_dict()
            rules.append(rules_item)

        statuses = []
        for statuses_item_data in self.statuses:
            statuses_item = statuses_item_data.to_dict()
            statuses.append(statuses_item)

        target_account = self.target_account.to_dict()

        updated_at = self.updated_at.isoformat()

        action_taken_at: Union[None, Unset, str]
        if isinstance(self.action_taken_at, Unset):
            action_taken_at = UNSET
        elif isinstance(self.action_taken_at, datetime.datetime):
            action_taken_at = self.action_taken_at.isoformat()
        else:
            action_taken_at = self.action_taken_at

        action_taken_by_account: Union[None, Unset, dict[str, Any]]
        if isinstance(self.action_taken_by_account, Unset):
            action_taken_by_account = UNSET
        elif isinstance(self.action_taken_by_account, AdminAccount):
            action_taken_by_account = self.action_taken_by_account.to_dict()
        else:
            action_taken_by_account = self.action_taken_by_account

        assigned_account: Union[None, Unset, dict[str, Any]]
        if isinstance(self.assigned_account, Unset):
            assigned_account = UNSET
        elif isinstance(self.assigned_account, AdminAccount):
            assigned_account = self.assigned_account.to_dict()
        else:
            assigned_account = self.assigned_account

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "account": account,
                "action_taken": action_taken,
                "category": category,
                "comment": comment,
                "created_at": created_at,
                "forwarded": forwarded,
                "id": id,
                "rules": rules,
                "statuses": statuses,
                "target_account": target_account,
                "updated_at": updated_at,
            }
        )
        if action_taken_at is not UNSET:
            field_dict["action_taken_at"] = action_taken_at
        if action_taken_by_account is not UNSET:
            field_dict["action_taken_by_account"] = action_taken_by_account
        if assigned_account is not UNSET:
            field_dict["assigned_account"] = assigned_account

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.admin_account import AdminAccount
        from ..models.rule import Rule
        from ..models.status import Status

        d = src_dict.copy()
        account = AdminAccount.from_dict(d.pop("account"))

        action_taken = d.pop("action_taken")

        category = CategoryEnum(d.pop("category"))

        comment = d.pop("comment")

        created_at = isoparse(d.pop("created_at"))

        forwarded = d.pop("forwarded")

        id = d.pop("id")

        rules = []
        _rules = d.pop("rules")
        for rules_item_data in _rules:
            rules_item = Rule.from_dict(rules_item_data)

            rules.append(rules_item)

        statuses = []
        _statuses = d.pop("statuses")
        for statuses_item_data in _statuses:
            statuses_item = Status.from_dict(statuses_item_data)

            statuses.append(statuses_item)

        target_account = AdminAccount.from_dict(d.pop("target_account"))

        updated_at = isoparse(d.pop("updated_at"))

        def _parse_action_taken_at(
            data: object,
        ) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                action_taken_at_type_0 = isoparse(data)

                return action_taken_at_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

        action_taken_at = _parse_action_taken_at(d.pop("action_taken_at", UNSET))

        def _parse_action_taken_by_account(
            data: object,
        ) -> Union["AdminAccount", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                action_taken_by_account_type_0 = AdminAccount.from_dict(data)

                return action_taken_by_account_type_0
            except:  # noqa: E722
                pass
            return cast(Union["AdminAccount", None, Unset], data)

        action_taken_by_account = _parse_action_taken_by_account(d.pop("action_taken_by_account", UNSET))

        def _parse_assigned_account(data: object) -> Union["AdminAccount", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                assigned_account_type_0 = AdminAccount.from_dict(data)

                return assigned_account_type_0
            except:  # noqa: E722
                pass
            return cast(Union["AdminAccount", None, Unset], data)

        assigned_account = _parse_assigned_account(d.pop("assigned_account", UNSET))

        admin_report = cls(
            account=account,
            action_taken=action_taken,
            category=category,
            comment=comment,
            created_at=created_at,
            forwarded=forwarded,
            id=id,
            rules=rules,
            statuses=statuses,
            target_account=target_account,
            updated_at=updated_at,
            action_taken_at=action_taken_at,
            action_taken_by_account=action_taken_by_account,
            assigned_account=assigned_account,
        )

        admin_report.additional_properties = d
        return admin_report

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
