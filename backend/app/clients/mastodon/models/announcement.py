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

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.announcement_account import AnnouncementAccount
    from ..models.announcement_status import AnnouncementStatus
    from ..models.custom_emoji import CustomEmoji
    from ..models.reaction import Reaction
    from ..models.status_tag import StatusTag


T = TypeVar("T", bound="Announcement")


@_attrs_define
class Announcement:
    """Represents an announcement set by an administrator.

    Example:
        {'id': '8', 'content': '<p>Looks like there was an issue processing audio attachments without embedded art since
            yesterday due to an experimental new feature. That issue has now been fixed, so you may see older posts with
            audio from other servers pop up in your feeds now as they are being finally properly processed. Sorry!</p>',
            'starts_at': None, 'ends_at': None, 'all_day': False, 'published_at': '2020-07-03T01:27:38.726Z', 'updated_at':
            '2020-07-03T01:27:38.752Z', 'read': True, 'mentions': [], 'statuses': [], 'tags': [], 'emojis': [], 'reactions':
            [{'name': 'bongoCat', 'count': 9, 'me': False, 'url':
            'https://files.mastodon.social/custom_emojis/images/000/067/715/original/fdba57dff7576d53.png', 'static_url':
            'https://files.mastodon.social/custom_emojis/images/000/067/715/static/fdba57dff7576d53.png'}, {'name':
            'thonking', 'count': 1, 'me': False, 'url':
            'https://files.mastodon.social/custom_emojis/images/000/098/690/original/a8d36edc4a7032e8.png', 'static_url':
            'https://files.mastodon.social/custom_emojis/images/000/098/690/static/a8d36edc4a7032e8.png'}, {'name':
            'AAAAAA', 'count': 1, 'me': False, 'url':
            'https://files.mastodon.social/custom_emojis/images/000/071/387/original/AAAAAA.png', 'static_url':
            'https://files.mastodon.social/custom_emojis/images/000/071/387/static/AAAAAA.png'}, {'name': '🤔', 'count': 1,
            'me': True}]}

    Attributes:
        all_day (bool): Whether the announcement should start and end on dates only instead of datetimes. Will be false
            if there is no `starts_at` or `ends_at` time.
        content (str): The text of the announcement.
        emojis (list['CustomEmoji']): Custom emoji used in the announcement text.
        id (str): The ID of the announcement in the database.
        mentions (list['AnnouncementAccount']): Accounts mentioned in the announcement text.
        published_at (datetime.datetime): When the announcement was published.
        reactions (list['Reaction']): Emoji reactions attached to the announcement.
        statuses (list['AnnouncementStatus']): Statuses linked in the announcement text.
        tags (list['StatusTag']): Tags linked in the announcement text.
        updated_at (datetime.datetime): When the announcement was last updated.
        ends_at (Union[None, Unset, datetime.datetime]): When the announcement will end.
        read (Union[None, Unset, bool]): Whether the announcement has been read by the current user.
        starts_at (Union[None, Unset, datetime.datetime]): When the announcement will start.
    """

    all_day: bool
    content: str
    emojis: list["CustomEmoji"]
    id: str
    mentions: list["AnnouncementAccount"]
    published_at: datetime.datetime
    reactions: list["Reaction"]
    statuses: list["AnnouncementStatus"]
    tags: list["StatusTag"]
    updated_at: datetime.datetime
    ends_at: Union[None, Unset, datetime.datetime] = UNSET
    read: Union[None, Unset, bool] = UNSET
    starts_at: Union[None, Unset, datetime.datetime] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        all_day = self.all_day

        content = self.content

        emojis = []
        for emojis_item_data in self.emojis:
            emojis_item = emojis_item_data.to_dict()
            emojis.append(emojis_item)

        id = self.id

        mentions = []
        for mentions_item_data in self.mentions:
            mentions_item = mentions_item_data.to_dict()
            mentions.append(mentions_item)

        published_at = self.published_at.isoformat()

        reactions = []
        for reactions_item_data in self.reactions:
            reactions_item = reactions_item_data.to_dict()
            reactions.append(reactions_item)

        statuses = []
        for statuses_item_data in self.statuses:
            statuses_item = statuses_item_data.to_dict()
            statuses.append(statuses_item)

        tags = []
        for tags_item_data in self.tags:
            tags_item = tags_item_data.to_dict()
            tags.append(tags_item)

        updated_at = self.updated_at.isoformat()

        ends_at: Union[None, Unset, str]
        if isinstance(self.ends_at, Unset):
            ends_at = UNSET
        elif isinstance(self.ends_at, datetime.datetime):
            ends_at = self.ends_at.isoformat()
        else:
            ends_at = self.ends_at

        read: Union[None, Unset, bool]
        if isinstance(self.read, Unset):
            read = UNSET
        else:
            read = self.read

        starts_at: Union[None, Unset, str]
        if isinstance(self.starts_at, Unset):
            starts_at = UNSET
        elif isinstance(self.starts_at, datetime.datetime):
            starts_at = self.starts_at.isoformat()
        else:
            starts_at = self.starts_at

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "all_day": all_day,
                "content": content,
                "emojis": emojis,
                "id": id,
                "mentions": mentions,
                "published_at": published_at,
                "reactions": reactions,
                "statuses": statuses,
                "tags": tags,
                "updated_at": updated_at,
            }
        )
        if ends_at is not UNSET:
            field_dict["ends_at"] = ends_at
        if read is not UNSET:
            field_dict["read"] = read
        if starts_at is not UNSET:
            field_dict["starts_at"] = starts_at

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.announcement_account import AnnouncementAccount
        from ..models.announcement_status import AnnouncementStatus
        from ..models.custom_emoji import CustomEmoji
        from ..models.reaction import Reaction
        from ..models.status_tag import StatusTag

        d = dict(src_dict)
        all_day = d.pop("all_day")

        content = d.pop("content")

        emojis = []
        _emojis = d.pop("emojis")
        for emojis_item_data in _emojis:
            emojis_item = CustomEmoji.from_dict(emojis_item_data)

            emojis.append(emojis_item)

        id = d.pop("id")

        mentions = []
        _mentions = d.pop("mentions")
        for mentions_item_data in _mentions:
            mentions_item = AnnouncementAccount.from_dict(mentions_item_data)

            mentions.append(mentions_item)

        published_at = isoparse(d.pop("published_at"))

        reactions = []
        _reactions = d.pop("reactions")
        for reactions_item_data in _reactions:
            reactions_item = Reaction.from_dict(reactions_item_data)

            reactions.append(reactions_item)

        statuses = []
        _statuses = d.pop("statuses")
        for statuses_item_data in _statuses:
            statuses_item = AnnouncementStatus.from_dict(statuses_item_data)

            statuses.append(statuses_item)

        tags = []
        _tags = d.pop("tags")
        for tags_item_data in _tags:
            tags_item = StatusTag.from_dict(tags_item_data)

            tags.append(tags_item)

        updated_at = isoparse(d.pop("updated_at"))

        def _parse_ends_at(data: object) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                ends_at_type_0 = isoparse(data)

                return ends_at_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

        ends_at = _parse_ends_at(d.pop("ends_at", UNSET))

        def _parse_read(data: object) -> Union[None, Unset, bool]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, bool], data)

        read = _parse_read(d.pop("read", UNSET))

        def _parse_starts_at(data: object) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                starts_at_type_0 = isoparse(data)

                return starts_at_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

        starts_at = _parse_starts_at(d.pop("starts_at", UNSET))

        announcement = cls(
            all_day=all_day,
            content=content,
            emojis=emojis,
            id=id,
            mentions=mentions,
            published_at=published_at,
            reactions=reactions,
            statuses=statuses,
            tags=tags,
            updated_at=updated_at,
            ends_at=ends_at,
            read=read,
            starts_at=starts_at,
        )

        announcement.additional_properties = d
        return announcement

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
