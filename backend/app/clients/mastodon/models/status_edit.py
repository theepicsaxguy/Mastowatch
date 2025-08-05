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
    from ..models.account import Account
    from ..models.custom_emoji import CustomEmoji
    from ..models.media_attachment import MediaAttachment
    from ..models.status_edit_poll_type_0 import StatusEditPollType0


T = TypeVar("T", bound="StatusEdit")


@_attrs_define
class StatusEdit:
    """Represents a revision of a status that has been edited.

    Attributes:
        account (Account): Represents a user of Mastodon and their associated profile.
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
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.account import Account
        from ..models.custom_emoji import CustomEmoji
        from ..models.media_attachment import MediaAttachment
        from ..models.status_edit_poll_type_0 import StatusEditPollType0

        d = dict(src_dict)
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
            media_attachments_item = MediaAttachment.from_dict(
                media_attachments_item_data
            )

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
