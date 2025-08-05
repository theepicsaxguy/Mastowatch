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

from ..models.visibility_enum import VisibilityEnum
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.account import Account
    from ..models.custom_emoji import CustomEmoji
    from ..models.filter_result import FilterResult
    from ..models.media_attachment import MediaAttachment
    from ..models.poll import Poll
    from ..models.preview_card import PreviewCard
    from ..models.status_application_type_0 import StatusApplicationType0
    from ..models.status_mention import StatusMention
    from ..models.status_tag import StatusTag


T = TypeVar("T", bound="Status")


@_attrs_define
class Status:
    """Represents a status posted by an account.

    Attributes:
        account (Account): Represents a user of Mastodon and their associated profile.
        content (str): HTML-encoded status content.
        created_at (datetime.datetime): The date when this status was created.
        emojis (list['CustomEmoji']): Custom emoji to be used when rendering status content.
        favourites_count (int): How many favourites this status has received.
        id (str): ID of the status in the database.
        media_attachments (list['MediaAttachment']): Media that is attached to this status.
        mentions (list['StatusMention']): Mentions of users within the status content.
        reblogs_count (int): How many boosts this status has received.
        replies_count (int): How many replies this status has received.
        sensitive (bool): Is this status marked as sensitive content?
        spoiler_text (str): Subject or summary line, below which status content is collapsed until expanded.
        tags (list['StatusTag']): Hashtags used within the status content.
        uri (str): URI of the status used for federation.
        visibility (VisibilityEnum):
        application (Union['StatusApplicationType0', None, Unset]): The application used to post this status.
        bookmarked (Union[None, Unset, bool]): If the current token has an authorized user: Have you bookmarked this
            status?
        card (Union['PreviewCard', None, Unset]): Preview card for links included within status content.
        edited_at (Union[None, Unset, datetime.datetime]): Timestamp of when the status was last edited.
        favourited (Union[None, Unset, bool]): If the current token has an authorized user: Have you favourited this
            status?
        filtered (Union[None, Unset, list['FilterResult']]): If the current token has an authorized user: The filter and
            keywords that matched this status.
        in_reply_to_account_id (Union[None, Unset, str]): Might be the ID of the account that authored the status being
            replied to. This sometimes skips over self-replies. If status A was posted by account 1, and account 2 posts
            statuses B, C, and D as a chain of replies to status A, statuses B, C, and D will all have
            `in_reply_to_account_id` = 1 (instead of C and D having `in_reply_to_account_id` = 2). However, if status A was
            posted by account 1, and account 1 posts status B as a direct reply to A, B will have an
            `in_reply_to_account_id` = 1 (instead of null).
        in_reply_to_id (Union[None, Unset, str]): ID of the status being replied to.
        language (Union[None, Unset, str]): Primary language of this status.
        muted (Union[None, Unset, bool]): If the current token has an authorized user: Have you muted notifications for
            this status's conversation?
        pinned (Union[None, Unset, bool]): If the current token has an authorized user: Have you pinned this status?
            Only appears if the status is pinnable.
        poll (Union['Poll', None, Unset]): The poll attached to the status.
        reblog (Union['Status', None, Unset]): The status being reblogged.
        reblogged (Union[None, Unset, bool]): If the current token has an authorized user: Have you boosted this status?
        text (Union[None, Unset, str]): Plain-text source of a status. Returned instead of `content` when status is
            deleted, so the user may redraft from the source text without the client having to reverse-engineer the original
            text from the HTML content.
        url (Union[None, Unset, str]): A link to the status's HTML representation.
    """

    account: "Account"
    content: str
    created_at: datetime.datetime
    emojis: list["CustomEmoji"]
    favourites_count: int
    id: str
    media_attachments: list["MediaAttachment"]
    mentions: list["StatusMention"]
    reblogs_count: int
    replies_count: int
    sensitive: bool
    spoiler_text: str
    tags: list["StatusTag"]
    uri: str
    visibility: VisibilityEnum
    application: Union["StatusApplicationType0", None, Unset] = UNSET
    bookmarked: Union[None, Unset, bool] = UNSET
    card: Union["PreviewCard", None, Unset] = UNSET
    edited_at: Union[None, Unset, datetime.datetime] = UNSET
    favourited: Union[None, Unset, bool] = UNSET
    filtered: Union[None, Unset, list["FilterResult"]] = UNSET
    in_reply_to_account_id: Union[None, Unset, str] = UNSET
    in_reply_to_id: Union[None, Unset, str] = UNSET
    language: Union[None, Unset, str] = UNSET
    muted: Union[None, Unset, bool] = UNSET
    pinned: Union[None, Unset, bool] = UNSET
    poll: Union["Poll", None, Unset] = UNSET
    reblog: Union["Status", None, Unset] = UNSET
    reblogged: Union[None, Unset, bool] = UNSET
    text: Union[None, Unset, str] = UNSET
    url: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.poll import Poll
        from ..models.preview_card import PreviewCard
        from ..models.status_application_type_0 import StatusApplicationType0

        account = self.account.to_dict()

        content = self.content

        created_at = self.created_at.isoformat()

        emojis = []
        for emojis_item_data in self.emojis:
            emojis_item = emojis_item_data.to_dict()
            emojis.append(emojis_item)

        favourites_count = self.favourites_count

        id = self.id

        media_attachments = []
        for media_attachments_item_data in self.media_attachments:
            media_attachments_item = media_attachments_item_data.to_dict()
            media_attachments.append(media_attachments_item)

        mentions = []
        for mentions_item_data in self.mentions:
            mentions_item = mentions_item_data.to_dict()
            mentions.append(mentions_item)

        reblogs_count = self.reblogs_count

        replies_count = self.replies_count

        sensitive = self.sensitive

        spoiler_text = self.spoiler_text

        tags = []
        for tags_item_data in self.tags:
            tags_item = tags_item_data.to_dict()
            tags.append(tags_item)

        uri = self.uri

        visibility = self.visibility.value

        application: Union[None, Unset, dict[str, Any]]
        if isinstance(self.application, Unset):
            application = UNSET
        elif isinstance(self.application, StatusApplicationType0):
            application = self.application.to_dict()
        else:
            application = self.application

        bookmarked: Union[None, Unset, bool]
        if isinstance(self.bookmarked, Unset):
            bookmarked = UNSET
        else:
            bookmarked = self.bookmarked

        card: Union[None, Unset, dict[str, Any]]
        if isinstance(self.card, Unset):
            card = UNSET
        elif isinstance(self.card, PreviewCard):
            card = self.card.to_dict()
        else:
            card = self.card

        edited_at: Union[None, Unset, str]
        if isinstance(self.edited_at, Unset):
            edited_at = UNSET
        elif isinstance(self.edited_at, datetime.datetime):
            edited_at = self.edited_at.isoformat()
        else:
            edited_at = self.edited_at

        favourited: Union[None, Unset, bool]
        if isinstance(self.favourited, Unset):
            favourited = UNSET
        else:
            favourited = self.favourited

        filtered: Union[None, Unset, list[dict[str, Any]]]
        if isinstance(self.filtered, Unset):
            filtered = UNSET
        elif isinstance(self.filtered, list):
            filtered = []
            for filtered_type_0_item_data in self.filtered:
                filtered_type_0_item = filtered_type_0_item_data.to_dict()
                filtered.append(filtered_type_0_item)

        else:
            filtered = self.filtered

        in_reply_to_account_id: Union[None, Unset, str]
        if isinstance(self.in_reply_to_account_id, Unset):
            in_reply_to_account_id = UNSET
        else:
            in_reply_to_account_id = self.in_reply_to_account_id

        in_reply_to_id: Union[None, Unset, str]
        if isinstance(self.in_reply_to_id, Unset):
            in_reply_to_id = UNSET
        else:
            in_reply_to_id = self.in_reply_to_id

        language: Union[None, Unset, str]
        if isinstance(self.language, Unset):
            language = UNSET
        else:
            language = self.language

        muted: Union[None, Unset, bool]
        if isinstance(self.muted, Unset):
            muted = UNSET
        else:
            muted = self.muted

        pinned: Union[None, Unset, bool]
        if isinstance(self.pinned, Unset):
            pinned = UNSET
        else:
            pinned = self.pinned

        poll: Union[None, Unset, dict[str, Any]]
        if isinstance(self.poll, Unset):
            poll = UNSET
        elif isinstance(self.poll, Poll):
            poll = self.poll.to_dict()
        else:
            poll = self.poll

        reblog: Union[None, Unset, dict[str, Any]]
        if isinstance(self.reblog, Unset):
            reblog = UNSET
        elif isinstance(self.reblog, Status):
            reblog = self.reblog.to_dict()
        else:
            reblog = self.reblog

        reblogged: Union[None, Unset, bool]
        if isinstance(self.reblogged, Unset):
            reblogged = UNSET
        else:
            reblogged = self.reblogged

        text: Union[None, Unset, str]
        if isinstance(self.text, Unset):
            text = UNSET
        else:
            text = self.text

        url: Union[None, Unset, str]
        if isinstance(self.url, Unset):
            url = UNSET
        else:
            url = self.url

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "account": account,
                "content": content,
                "created_at": created_at,
                "emojis": emojis,
                "favourites_count": favourites_count,
                "id": id,
                "media_attachments": media_attachments,
                "mentions": mentions,
                "reblogs_count": reblogs_count,
                "replies_count": replies_count,
                "sensitive": sensitive,
                "spoiler_text": spoiler_text,
                "tags": tags,
                "uri": uri,
                "visibility": visibility,
            }
        )
        if application is not UNSET:
            field_dict["application"] = application
        if bookmarked is not UNSET:
            field_dict["bookmarked"] = bookmarked
        if card is not UNSET:
            field_dict["card"] = card
        if edited_at is not UNSET:
            field_dict["edited_at"] = edited_at
        if favourited is not UNSET:
            field_dict["favourited"] = favourited
        if filtered is not UNSET:
            field_dict["filtered"] = filtered
        if in_reply_to_account_id is not UNSET:
            field_dict["in_reply_to_account_id"] = in_reply_to_account_id
        if in_reply_to_id is not UNSET:
            field_dict["in_reply_to_id"] = in_reply_to_id
        if language is not UNSET:
            field_dict["language"] = language
        if muted is not UNSET:
            field_dict["muted"] = muted
        if pinned is not UNSET:
            field_dict["pinned"] = pinned
        if poll is not UNSET:
            field_dict["poll"] = poll
        if reblog is not UNSET:
            field_dict["reblog"] = reblog
        if reblogged is not UNSET:
            field_dict["reblogged"] = reblogged
        if text is not UNSET:
            field_dict["text"] = text
        if url is not UNSET:
            field_dict["url"] = url

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.account import Account
        from ..models.custom_emoji import CustomEmoji
        from ..models.filter_result import FilterResult
        from ..models.media_attachment import MediaAttachment
        from ..models.poll import Poll
        from ..models.preview_card import PreviewCard
        from ..models.status_application_type_0 import StatusApplicationType0
        from ..models.status_mention import StatusMention
        from ..models.status_tag import StatusTag

        d = dict(src_dict)
        account = Account.from_dict(d.pop("account"))

        content = d.pop("content")

        created_at = isoparse(d.pop("created_at"))

        emojis = []
        _emojis = d.pop("emojis")
        for emojis_item_data in _emojis:
            emojis_item = CustomEmoji.from_dict(emojis_item_data)

            emojis.append(emojis_item)

        favourites_count = d.pop("favourites_count")

        id = d.pop("id")

        media_attachments = []
        _media_attachments = d.pop("media_attachments")
        for media_attachments_item_data in _media_attachments:
            media_attachments_item = MediaAttachment.from_dict(
                media_attachments_item_data
            )

            media_attachments.append(media_attachments_item)

        mentions = []
        _mentions = d.pop("mentions")
        for mentions_item_data in _mentions:
            mentions_item = StatusMention.from_dict(mentions_item_data)

            mentions.append(mentions_item)

        reblogs_count = d.pop("reblogs_count")

        replies_count = d.pop("replies_count")

        sensitive = d.pop("sensitive")

        spoiler_text = d.pop("spoiler_text")

        tags = []
        _tags = d.pop("tags")
        for tags_item_data in _tags:
            tags_item = StatusTag.from_dict(tags_item_data)

            tags.append(tags_item)

        uri = d.pop("uri")

        visibility = VisibilityEnum(d.pop("visibility"))

        def _parse_application(
            data: object,
        ) -> Union["StatusApplicationType0", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                application_type_0 = StatusApplicationType0.from_dict(data)

                return application_type_0
            except:  # noqa: E722
                pass
            return cast(Union["StatusApplicationType0", None, Unset], data)

        application = _parse_application(d.pop("application", UNSET))

        def _parse_bookmarked(data: object) -> Union[None, Unset, bool]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, bool], data)

        bookmarked = _parse_bookmarked(d.pop("bookmarked", UNSET))

        def _parse_card(data: object) -> Union["PreviewCard", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                card_type_0 = PreviewCard.from_dict(data)

                return card_type_0
            except:  # noqa: E722
                pass
            return cast(Union["PreviewCard", None, Unset], data)

        card = _parse_card(d.pop("card", UNSET))

        def _parse_edited_at(data: object) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                edited_at_type_0 = isoparse(data)

                return edited_at_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

        edited_at = _parse_edited_at(d.pop("edited_at", UNSET))

        def _parse_favourited(data: object) -> Union[None, Unset, bool]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, bool], data)

        favourited = _parse_favourited(d.pop("favourited", UNSET))

        def _parse_filtered(data: object) -> Union[None, Unset, list["FilterResult"]]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                filtered_type_0 = []
                _filtered_type_0 = data
                for filtered_type_0_item_data in _filtered_type_0:
                    filtered_type_0_item = FilterResult.from_dict(
                        filtered_type_0_item_data
                    )

                    filtered_type_0.append(filtered_type_0_item)

                return filtered_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, list["FilterResult"]], data)

        filtered = _parse_filtered(d.pop("filtered", UNSET))

        def _parse_in_reply_to_account_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        in_reply_to_account_id = _parse_in_reply_to_account_id(
            d.pop("in_reply_to_account_id", UNSET)
        )

        def _parse_in_reply_to_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        in_reply_to_id = _parse_in_reply_to_id(d.pop("in_reply_to_id", UNSET))

        def _parse_language(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        language = _parse_language(d.pop("language", UNSET))

        def _parse_muted(data: object) -> Union[None, Unset, bool]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, bool], data)

        muted = _parse_muted(d.pop("muted", UNSET))

        def _parse_pinned(data: object) -> Union[None, Unset, bool]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, bool], data)

        pinned = _parse_pinned(d.pop("pinned", UNSET))

        def _parse_poll(data: object) -> Union["Poll", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                poll_type_0 = Poll.from_dict(data)

                return poll_type_0
            except:  # noqa: E722
                pass
            return cast(Union["Poll", None, Unset], data)

        poll = _parse_poll(d.pop("poll", UNSET))

        def _parse_reblog(data: object) -> Union["Status", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                reblog_type_0 = Status.from_dict(data)

                return reblog_type_0
            except:  # noqa: E722
                pass
            return cast(Union["Status", None, Unset], data)

        reblog = _parse_reblog(d.pop("reblog", UNSET))

        def _parse_reblogged(data: object) -> Union[None, Unset, bool]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, bool], data)

        reblogged = _parse_reblogged(d.pop("reblogged", UNSET))

        def _parse_text(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        text = _parse_text(d.pop("text", UNSET))

        def _parse_url(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        url = _parse_url(d.pop("url", UNSET))

        status = cls(
            account=account,
            content=content,
            created_at=created_at,
            emojis=emojis,
            favourites_count=favourites_count,
            id=id,
            media_attachments=media_attachments,
            mentions=mentions,
            reblogs_count=reblogs_count,
            replies_count=replies_count,
            sensitive=sensitive,
            spoiler_text=spoiler_text,
            tags=tags,
            uri=uri,
            visibility=visibility,
            application=application,
            bookmarked=bookmarked,
            card=card,
            edited_at=edited_at,
            favourited=favourited,
            filtered=filtered,
            in_reply_to_account_id=in_reply_to_account_id,
            in_reply_to_id=in_reply_to_id,
            language=language,
            muted=muted,
            pinned=pinned,
            poll=poll,
            reblog=reblog,
            reblogged=reblogged,
            text=text,
            url=url,
        )

        status.additional_properties = d
        return status

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
