import datetime
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.notification_type_enum import NotificationTypeEnum
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.account import Account
    from ..models.account_warning import AccountWarning
    from ..models.relationship_severance_event import \
        RelationshipSeveranceEvent
    from ..models.report import Report
    from ..models.status import Status


T = TypeVar("T", bound="Notification")


@_attrs_define
class Notification:
    r"""Represents a notification of an event relevant to the user.

    Attributes:
        account (Account): Represents a user of Mastodon and their associated profile. Example: {'id': '23634',
            'username': 'noiob', 'acct': 'noiob@awoo.space', 'display_name': 'ikea shark fan account', 'locked': False,
            'bot': False, 'created_at': '2017-02-08T02:00:53.274Z', 'note': '<p>:ms_rainbow_flag:\u200b
            :ms_bisexual_flagweb:\u200b :ms_nonbinary_flag:\u200b <a href="https://awoo.space/tags/awoo" class="mention
            hashtag" rel="nofollow noopener noreferrer" target="_blank">#<span>awoo</span}.space <a
            href="https://awoo.space/tags/admin" class="mention hashtag" rel="nofollow noopener noreferrer"
            target="_blank">#<span>admin</span} ~ <a href="https://awoo.space/tags/bi" class="mention hashtag" rel="nofollow
            noopener noreferrer" target="_blank">#<span>bi</span} ~ <a href="https://awoo.space/tags/nonbinary"
            class="mention hashtag" rel="nofollow noopener noreferrer" target="_blank">#<span>nonbinary</span} ~ compsci
            student ~ likes video <a href="https://awoo.space/tags/games" class="mention hashtag" rel="nofollow noopener
            noreferrer" target="_blank">#<span>games</span} and weird/ old electronics and will post obsessively about both
            ~ avatar by <span class="h-card"><a href="https://weirder.earth/@dzuk" class="u-url mention" rel="nofollow
            noopener noreferrer" target="_blank">@<span>dzuk</span}</span></p>', 'url': 'https://awoo.space/@noiob',
            'avatar': 'https://files.mastodon.social/accounts/avatars/000/023/634/original/6ca8804dc46800ad.png',
            'avatar_static': 'https://files.mastodon.social/accounts/avatars/000/023/634/original/6ca8804dc46800ad.png',
            'header': 'https://files.mastodon.social/accounts/headers/000/023/634/original/256eb8d7ac40f49a.png',
            'header_static': 'https://files.mastodon.social/accounts/headers/000/023/634/original/256eb8d7ac40f49a.png',
            'followers_count': 547, 'following_count': 404, 'statuses_count': 28468, 'last_status_at': '2019-11-17',
            'emojis': [{'shortcode': 'ms_rainbow_flag', 'url':
            'https://files.mastodon.social/custom_emojis/images/000/028/691/original/6de008d6281f4f59.png', 'static_url':
            'https://files.mastodon.social/custom_emojis/images/000/028/691/static/6de008d6281f4f59.png',
            'visible_in_picker': True}, {'shortcode': 'ms_bisexual_flag', 'url':
            'https://files.mastodon.social/custom_emojis/images/000/050/744/original/02f94a5fca7eaf78.png', 'static_url':
            'https://files.mastodon.social/custom_emojis/images/000/050/744/static/02f94a5fca7eaf78.png',
            'visible_in_picker': True}, {'shortcode': 'ms_nonbinary_flag', 'url':
            'https://files.mastodon.social/custom_emojis/images/000/105/099/original/8106088bd4782072.png', 'static_url':
            'https://files.mastodon.social/custom_emojis/images/000/105/099/static/8106088bd4782072.png',
            'visible_in_picker': True}], 'fields': [{'name': 'Pronouns', 'value': 'they/them', 'verified_at': None},
            {'name': 'Alt', 'value': '<span class="h-card"><a href="https://cybre.space/@noiob" class="u-url mention"
            rel="nofollow noopener noreferrer" target="_blank">@<span>noiob</span}</span>', 'verified_at': None}, {'name':
            'Bots', 'value': '<span class="h-card"><a href="https://botsin.space/@darksouls" class="u-url mention"
            rel="nofollow noopener noreferrer" target="_blank">@<span>darksouls</span}</span>, <span class="h-card"><a
            href="https://botsin.space/@nierautomata" class="u-url mention" rel="nofollow noopener noreferrer"
            target="_blank">@<span>nierautomata</span}</span>, <span class="h-card"><a href="https://mastodon.social/@fedi"
            class="u-url mention" rel="nofollow noopener noreferrer" target="_blank">@<span>fedi</span}</span>, code for
            <span class="h-card"><a href="https://botsin.space/@awoobot" class="u-url mention" rel="nofollow noopener
            noreferrer" target="_blank">@<span>awoobot</span}</span>', 'verified_at': None}, {'name': 'Website', 'value':
            '<a href="http://shork.xyz" rel="nofollow noopener noreferrer" target="_blank"><span
            class="invisible">http://</span><span class="">shork.xyz</span><span class="invisible"></span}', 'verified_at':
            '2019-11-10T10:31:10.744+00:00'}]}.
        created_at (datetime.datetime): The timestamp of the notification.
        group_key (str): Group key shared by similar notifications, to be used in the grouped notifications feature.
            Should be considered opaque, but ungrouped notifications can be assumed to have a `group_key` of the form
            `ungrouped-{notification_id}`.
        id (str): The id of the notification in the database.
        type_ (NotificationTypeEnum):
        event (Union['RelationshipSeveranceEvent', None, Unset]): Summary of the event that caused follow relationships
            to be severed. Attached when `type` of the notification is `severed_relationships`.
        moderation_warning (Union['AccountWarning', None, Unset]): Moderation warning that caused the notification.
            Attached when `type` of the notification is `moderation_warning`.
        report (Union['Report', None, Unset]): Report that was the object of the notification. Attached when `type` of
            the notification is `admin.report`.
        status (Union['Status', None, Unset]): Status that was the object of the notification. Attached when `type` of
            the notification is `favourite`, `reblog`, `status`, `mention`, `poll`, or `update`.
    """

    account: "Account"
    created_at: datetime.datetime
    group_key: str
    id: str
    type_: NotificationTypeEnum
    event: Union["RelationshipSeveranceEvent", None, Unset] = UNSET
    moderation_warning: Union["AccountWarning", None, Unset] = UNSET
    report: Union["Report", None, Unset] = UNSET
    status: Union["Status", None, Unset] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.account_warning import AccountWarning
        from ..models.relationship_severance_event import \
            RelationshipSeveranceEvent
        from ..models.report import Report
        from ..models.status import Status

        account = self.account.to_dict()

        created_at = self.created_at.isoformat()

        group_key = self.group_key

        id = self.id

        type_ = self.type_.value

        event: Union[None, Unset, dict[str, Any]]
        if isinstance(self.event, Unset):
            event = UNSET
        elif isinstance(self.event, RelationshipSeveranceEvent):
            event = self.event.to_dict()
        else:
            event = self.event

        moderation_warning: Union[None, Unset, dict[str, Any]]
        if isinstance(self.moderation_warning, Unset):
            moderation_warning = UNSET
        elif isinstance(self.moderation_warning, AccountWarning):
            moderation_warning = self.moderation_warning.to_dict()
        else:
            moderation_warning = self.moderation_warning

        report: Union[None, Unset, dict[str, Any]]
        if isinstance(self.report, Unset):
            report = UNSET
        elif isinstance(self.report, Report):
            report = self.report.to_dict()
        else:
            report = self.report

        status: Union[None, Unset, dict[str, Any]]
        if isinstance(self.status, Unset):
            status = UNSET
        elif isinstance(self.status, Status):
            status = self.status.to_dict()
        else:
            status = self.status

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "account": account,
                "created_at": created_at,
                "group_key": group_key,
                "id": id,
                "type": type_,
            }
        )
        if event is not UNSET:
            field_dict["event"] = event
        if moderation_warning is not UNSET:
            field_dict["moderation_warning"] = moderation_warning
        if report is not UNSET:
            field_dict["report"] = report
        if status is not UNSET:
            field_dict["status"] = status

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.account import Account
        from ..models.account_warning import AccountWarning
        from ..models.relationship_severance_event import \
            RelationshipSeveranceEvent
        from ..models.report import Report
        from ..models.status import Status

        d = src_dict.copy()
        account = Account.from_dict(d.pop("account"))

        created_at = isoparse(d.pop("created_at"))

        group_key = d.pop("group_key")

        id = d.pop("id")

        type_ = NotificationTypeEnum(d.pop("type"))

        def _parse_event(
            data: object,
        ) -> Union["RelationshipSeveranceEvent", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                event_type_0 = RelationshipSeveranceEvent.from_dict(data)

                return event_type_0
            except:  # noqa: E722
                pass
            return cast(Union["RelationshipSeveranceEvent", None, Unset], data)

        event = _parse_event(d.pop("event", UNSET))

        def _parse_moderation_warning(
            data: object,
        ) -> Union["AccountWarning", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                moderation_warning_type_0 = AccountWarning.from_dict(data)

                return moderation_warning_type_0
            except:  # noqa: E722
                pass
            return cast(Union["AccountWarning", None, Unset], data)

        moderation_warning = _parse_moderation_warning(d.pop("moderation_warning", UNSET))

        def _parse_report(data: object) -> Union["Report", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                report_type_0 = Report.from_dict(data)

                return report_type_0
            except:  # noqa: E722
                pass
            return cast(Union["Report", None, Unset], data)

        report = _parse_report(d.pop("report", UNSET))

        def _parse_status(data: object) -> Union["Status", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                status_type_0 = Status.from_dict(data)

                return status_type_0
            except:  # noqa: E722
                pass
            return cast(Union["Status", None, Unset], data)

        status = _parse_status(d.pop("status", UNSET))

        notification = cls(
            account=account,
            created_at=created_at,
            group_key=group_key,
            id=id,
            type_=type_,
            event=event,
            moderation_warning=moderation_warning,
            report=report,
            status=status,
        )

        notification.additional_properties = d
        return notification

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
