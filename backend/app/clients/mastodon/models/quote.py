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

from ..models.state_enum import StateEnum
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.status import Status


T = TypeVar("T", bound="Quote")


@_attrs_define
class Quote:
    """Represents a quote or a quote placeholder, with the current authorization status.

    Example:
        {'state': 'accepted', 'quoted_status': {'id': '103270115826048975', 'created_at': '2019-12-08T03:48:33.901Z',
            'in_reply_to_id': None, 'in_reply_to_account_id': None, 'sensitive': False, 'spoiler_text': '', 'visibility':
            'public', 'language': 'en', 'uri': 'https://mastodon.social/users/Gargron/statuses/103270115826048975', 'url':
            'https://mastodon.social/@Gargron/103270115826048975', 'replies_count': 5, 'reblogs_count': 6,
            'favourites_count': 11, 'favourited': False, 'reblogged': False, 'muted': False, 'bookmarked': False, 'content':
            '<p>&quot;I lost my inheritance with one wrong digit on my sort code&quot;</p><p><a
            href="https://www.theguardian.com/money/2019/dec/07/i-lost-my-193000-inheritance-with-one-wrong-digit-on-my-
            sort-code" rel="nofollow noopener noreferrer" target="_blank"><span class="invisible">https://www.</span><span
            class="ellipsis">theguardian.com/money/2019/dec</span><span class="invisible">/07/i-lost-my-193000-inheritance-
            with-one-wrong-digit-on-my-sort-code</span}</p>', 'reblog': None, 'application': {'name': 'Web', 'website':
            None}, 'account': {'id': '1', 'username': 'Gargron', 'acct': 'Gargron', 'display_name': 'Eugen', 'locked':
            False, 'bot': False, 'discoverable': True, 'group': False, 'created_at': '2016-03-16T14:34:26.392Z', 'note':
            '<p>Developer of Mastodon and administrator of mastodon.social. I post service announcements, development
            updates, and personal stuff.</p>', 'url': 'https://mastodon.social/@Gargron', 'avatar':
            'https://files.mastodon.social/accounts/avatars/000/000/001/original/d96d39a0abb45b92.jpg', 'avatar_static':
            'https://files.mastodon.social/accounts/avatars/000/000/001/original/d96d39a0abb45b92.jpg', 'header':
            'https://files.mastodon.social/accounts/headers/000/000/001/original/c91b871f294ea63e.png', 'header_static':
            'https://files.mastodon.social/accounts/headers/000/000/001/original/c91b871f294ea63e.png', 'followers_count':
            322930, 'following_count': 459, 'statuses_count': 61323, 'last_status_at': '2019-12-10T08:14:44.811Z', 'emojis':
            [], 'fields': []}, 'media_attachments': [], 'mentions': [], 'tags': [], 'emojis': [], 'card': None, 'poll':
            None}}

    Attributes:
        state (StateEnum):
        quoted_status (Union['Status', None, Unset]): The status being quoted, if the quote has been accepted. This will
            be `null`, unless the `state` attribute is `accepted`.
    """

    state: StateEnum
    quoted_status: Union["Status", None, Unset] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.status import Status

        state = self.state.value

        quoted_status: Union[None, Unset, dict[str, Any]]
        if isinstance(self.quoted_status, Unset):
            quoted_status = UNSET
        elif isinstance(self.quoted_status, Status):
            quoted_status = self.quoted_status.to_dict()
        else:
            quoted_status = self.quoted_status

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "state": state,
            }
        )
        if quoted_status is not UNSET:
            field_dict["quoted_status"] = quoted_status

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.status import Status

        d = dict(src_dict)
        state = StateEnum(d.pop("state"))

        def _parse_quoted_status(data: object) -> Union["Status", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                quoted_status_type_0 = Status.from_dict(data)

                return quoted_status_type_0
            except:  # noqa: E722
                pass
            return cast(Union["Status", None, Unset], data)

        quoted_status = _parse_quoted_status(d.pop("quoted_status", UNSET))

        quote = cls(
            state=state,
            quoted_status=quoted_status,
        )

        quote.additional_properties = d
        return quote

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
