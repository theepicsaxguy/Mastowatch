import datetime
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.account import Account
    from ..models.custom_emoji import CustomEmoji
    from ..models.media_attachment import MediaAttachment
    from ..models.status_edit_poll_type_0 import StatusEditPollType0


T = TypeVar("T", bound="StatusEdit")


@_attrs_define
class StatusEdit:
    r"""Represents a revision of a status that has been edited.

    Example:
        {'content': '<p>this is a status that has been edited three times. this time a poll has been added.</p>',
            'spoiler_text': '', 'sensitive': False, 'created_at': '2022-09-05T00:03:32.480Z', 'poll': {'options': [{'title':
            'cool'}, {'title': 'uncool'}, {'title': 'spiderman (this option has been changed)'}]}, 'account': {'id':
            '14715', 'username': 'trwnh', 'acct': 'trwnh', 'display_name': 'infinite love ⴳ'}, 'media_attachments': [],
            'emojis': []}

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
        content (str): The content of the status at this revision.
        created_at (datetime.datetime): The timestamp of when the revision was published.
        emojis (list['CustomEmoji']): Any custom emoji that are used in the current revision.
        media_attachments (list['MediaAttachment']): The current state of the media attachments at this revision.
        sensitive (bool): Whether the status was marked sensitive at this revision.
        spoiler_text (str): The content of the subject or content warning at this revision.
        poll (Union['StatusEditPollType0', None, Unset]): The current state of the poll options at this revision. Note
            that edits changing the poll options will be collapsed together into one edit, since this action resets the
            poll.
    """

    account: "Account"
    content: str
    created_at: datetime.datetime
    emojis: list["CustomEmoji"]
    media_attachments: list["MediaAttachment"]
    sensitive: bool
    spoiler_text: str
    poll: Union["StatusEditPollType0", None, Unset] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.status_edit_poll_type_0 import StatusEditPollType0

        account = self.account.to_dict()

        content = self.content

        created_at = self.created_at.isoformat()

        emojis = []
        for emojis_item_data in self.emojis:
            emojis_item = emojis_item_data.to_dict()
            emojis.append(emojis_item)

        media_attachments = []
        for media_attachments_item_data in self.media_attachments:
            media_attachments_item = media_attachments_item_data.to_dict()
            media_attachments.append(media_attachments_item)

        sensitive = self.sensitive

        spoiler_text = self.spoiler_text

        poll: Union[None, Unset, dict[str, Any]]
        if isinstance(self.poll, Unset):
            poll = UNSET
        elif isinstance(self.poll, StatusEditPollType0):
            poll = self.poll.to_dict()
        else:
            poll = self.poll

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "account": account,
                "content": content,
                "created_at": created_at,
                "emojis": emojis,
                "media_attachments": media_attachments,
                "sensitive": sensitive,
                "spoiler_text": spoiler_text,
            }
        )
        if poll is not UNSET:
            field_dict["poll"] = poll

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.account import Account
        from ..models.custom_emoji import CustomEmoji
        from ..models.media_attachment import MediaAttachment
        from ..models.status_edit_poll_type_0 import StatusEditPollType0

        d = src_dict.copy()
        account = Account.from_dict(d.pop("account"))

        content = d.pop("content")

        created_at = isoparse(d.pop("created_at"))

        emojis = []
        _emojis = d.pop("emojis")
        for emojis_item_data in _emojis:
            emojis_item = CustomEmoji.from_dict(emojis_item_data)

            emojis.append(emojis_item)

        media_attachments = []
        _media_attachments = d.pop("media_attachments")
        for media_attachments_item_data in _media_attachments:
            media_attachments_item = MediaAttachment.from_dict(media_attachments_item_data)

            media_attachments.append(media_attachments_item)

        sensitive = d.pop("sensitive")

        spoiler_text = d.pop("spoiler_text")

        def _parse_poll(data: object) -> Union["StatusEditPollType0", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                poll_type_0 = StatusEditPollType0.from_dict(data)

                return poll_type_0
            except:  # noqa: E722
                pass
            return cast(Union["StatusEditPollType0", None, Unset], data)

        poll = _parse_poll(d.pop("poll", UNSET))

        status_edit = cls(
            account=account,
            content=content,
            created_at=created_at,
            emojis=emojis,
            media_attachments=media_attachments,
            sensitive=sensitive,
            spoiler_text=spoiler_text,
            poll=poll,
        )

        status_edit.additional_properties = d
        return status_edit

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
