import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.custom_emoji import CustomEmoji
    from ..models.poll_option import PollOption


T = TypeVar("T", bound="Poll")


@_attrs_define
class Poll:
    """Represents a poll attached to a status.

    Example:
        {'id': '34830', 'expires_at': '2019-12-05T04:05:08.302Z', 'expired': True, 'multiple': False, 'votes_count': 10,
            'voters_count': None, 'voted': True, 'own_votes': [1], 'options': [{'title': 'accept', 'votes_count': 6},
            {'title': 'deny', 'votes_count': 4}], 'emojis': []}

    Attributes:
        emojis (list['CustomEmoji']): Custom emoji to be used for rendering poll options.
        expired (bool): Is the poll currently expired?
        id (str): The ID of the poll in the database.
        multiple (bool): Does the poll allow multiple-choice answers?
        options (list['PollOption']): Possible answers for the poll.
        votes_count (int): How many votes have been received.
        expires_at (Union[None, Unset, datetime.datetime]): When the poll ends.
        own_votes (Union[None, Unset, list[int]]): When called with a user token, which options has the authorized user
            chosen? Contains an array of index values for `options`.
        voted (Union[None, Unset, bool]): When called with a user token, has the authorized user voted?
        voters_count (Union[None, Unset, int]): How many unique accounts have voted on a multiple-choice poll.

    """

    emojis: list["CustomEmoji"]
    expired: bool
    id: str
    multiple: bool
    options: list["PollOption"]
    votes_count: int
    expires_at: None | Unset | datetime.datetime = UNSET
    own_votes: None | Unset | list[int] = UNSET
    voted: None | Unset | bool = UNSET
    voters_count: None | Unset | int = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        emojis = []
        for emojis_item_data in self.emojis:
            emojis_item = emojis_item_data.to_dict()
            emojis.append(emojis_item)

        expired = self.expired

        id = self.id

        multiple = self.multiple

        options = []
        for options_item_data in self.options:
            options_item = options_item_data.to_dict()
            options.append(options_item)

        votes_count = self.votes_count

        expires_at: None | Unset | str
        if isinstance(self.expires_at, Unset):
            expires_at = UNSET
        elif isinstance(self.expires_at, datetime.datetime):
            expires_at = self.expires_at.isoformat()
        else:
            expires_at = self.expires_at

        own_votes: None | Unset | list[int]
        if isinstance(self.own_votes, Unset):
            own_votes = UNSET
        elif isinstance(self.own_votes, list):
            own_votes = self.own_votes

        else:
            own_votes = self.own_votes

        voted: None | Unset | bool
        if isinstance(self.voted, Unset):
            voted = UNSET
        else:
            voted = self.voted

        voters_count: None | Unset | int
        if isinstance(self.voters_count, Unset):
            voters_count = UNSET
        else:
            voters_count = self.voters_count

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "emojis": emojis,
                "expired": expired,
                "id": id,
                "multiple": multiple,
                "options": options,
                "votes_count": votes_count,
            }
        )
        if expires_at is not UNSET:
            field_dict["expires_at"] = expires_at
        if own_votes is not UNSET:
            field_dict["own_votes"] = own_votes
        if voted is not UNSET:
            field_dict["voted"] = voted
        if voters_count is not UNSET:
            field_dict["voters_count"] = voters_count

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.custom_emoji import CustomEmoji
        from ..models.poll_option import PollOption

        d = dict(src_dict)
        emojis = []
        _emojis = d.pop("emojis")
        for emojis_item_data in _emojis:
            emojis_item = CustomEmoji.from_dict(emojis_item_data)

            emojis.append(emojis_item)

        expired = d.pop("expired")

        id = d.pop("id")

        multiple = d.pop("multiple")

        options = []
        _options = d.pop("options")
        for options_item_data in _options:
            options_item = PollOption.from_dict(options_item_data)

            options.append(options_item)

        votes_count = d.pop("votes_count")

        def _parse_expires_at(data: object) -> None | Unset | datetime.datetime:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                expires_at_type_0 = isoparse(data)

                return expires_at_type_0
            except:  # noqa: E722
                pass
            return cast(None | Unset | datetime.datetime, data)

        expires_at = _parse_expires_at(d.pop("expires_at", UNSET))

        def _parse_own_votes(data: object) -> None | Unset | list[int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                own_votes_type_0 = cast(list[int], data)

                return own_votes_type_0
            except:  # noqa: E722
                pass
            return cast(None | Unset | list[int], data)

        own_votes = _parse_own_votes(d.pop("own_votes", UNSET))

        def _parse_voted(data: object) -> None | Unset | bool:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | Unset | bool, data)

        voted = _parse_voted(d.pop("voted", UNSET))

        def _parse_voters_count(data: object) -> None | Unset | int:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | Unset | int, data)

        voters_count = _parse_voters_count(d.pop("voters_count", UNSET))

        poll = cls(
            emojis=emojis,
            expired=expired,
            id=id,
            multiple=multiple,
            options=options,
            votes_count=votes_count,
            expires_at=expires_at,
            own_votes=own_votes,
            voted=voted,
            voters_count=voters_count,
        )

        poll.additional_properties = d
        return poll

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
