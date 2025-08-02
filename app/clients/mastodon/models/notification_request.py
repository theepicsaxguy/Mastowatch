import datetime
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.account import Account
    from ..models.status import Status


T = TypeVar("T", bound="NotificationRequest")


@_attrs_define
class NotificationRequest:
    r"""Represents a group of filtered notifications from a specific user.

    Example:
        {'id': '112456967201894256', 'created_at': '2024-05-17T14:45:41.171Z', 'updated_at': '2024-05-17T14:45:41.171Z',
            'notifications_count': '1', 'account': {'id': '971724', 'username': 'zsc', 'acct': 'zsc'}, 'last_status': {'id':
            '103186126728896492', 'created_at': '2019-11-23T07:49:01.940Z', 'in_reply_to_id': '103186038209478945',
            'in_reply_to_account_id': '14715', 'content': '<p><span class="h-card"><a href="https://mastodon.social/@trwnh"
            class="u-url mention">@<span>trwnh</span></a></span> sup!</p>', 'account': {'id': '971724', 'username': 'zsc',
            'acct': 'zsc'}, 'mentions': [{'id': '14715', 'username': 'trwnh', 'url': 'https://mastodon.social/@trwnh',
            'acct': 'trwnh'}]}}

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
        created_at (datetime.datetime): The timestamp of the notification request, i.e. when the first filtered
            notification from that user was created.
        id (str): The id of the notification request in the database.
        notifications_count (str): How many of this account's notifications were filtered.
        updated_at (datetime.datetime): The timestamp of when the notification request was last updated.
        last_status (Union['Status', None, Unset]): Most recent status associated with a filtered notification from that
            account.
    """

    account: "Account"
    created_at: datetime.datetime
    id: str
    notifications_count: str
    updated_at: datetime.datetime
    last_status: Union["Status", None, Unset] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.status import Status

        account = self.account.to_dict()

        created_at = self.created_at.isoformat()

        id = self.id

        notifications_count = self.notifications_count

        updated_at = self.updated_at.isoformat()

        last_status: Union[None, Unset, dict[str, Any]]
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
                "account": account,
                "created_at": created_at,
                "id": id,
                "notifications_count": notifications_count,
                "updated_at": updated_at,
            }
        )
        if last_status is not UNSET:
            field_dict["last_status"] = last_status

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.account import Account
        from ..models.status import Status

        d = src_dict.copy()
        account = Account.from_dict(d.pop("account"))

        created_at = isoparse(d.pop("created_at"))

        id = d.pop("id")

        notifications_count = d.pop("notifications_count")

        updated_at = isoparse(d.pop("updated_at"))

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

        notification_request = cls(
            account=account,
            created_at=created_at,
            id=id,
            notifications_count=notifications_count,
            updated_at=updated_at,
            last_status=last_status,
        )

        notification_request.additional_properties = d
        return notification_request

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
