from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="Relationship")


@_attrs_define
class Relationship:
    """Represents the relationship between accounts, such as following / blocking / muting / etc.

    Example:
        {'id': '1', 'following': True, 'showing_reblogs': True, 'notifying': False, 'followed_by': True, 'blocking':
            False, 'blocked_by': False, 'muting': False, 'muting_notifications': False, 'requested': False, 'requested_by':
            False, 'domain_blocking': False, 'endorsed': False, 'note': ''}

    Attributes:
        blocked_by (bool): Is this user blocking you?
        blocking (bool): Are you blocking this user?
        domain_blocking (bool): Are you blocking this user's domain?
        endorsed (bool): Are you featuring this user on your profile?
        followed_by (bool): Are you followed by this user?
        following (bool): Are you following this user?
        id (str): The account ID.
        muting (bool): Are you muting this user?
        muting_notifications (bool): Are you muting notifications from this user?
        note (str): This user's profile bio
        notifying (bool): Have you enabled notifications for this user?
        requested (bool): Do you have a pending follow request for this user?
        requested_by (bool): Has this user requested to follow you?
        showing_reblogs (bool): Are you receiving this user's boosts in your home timeline?
        languages (Union[None, Unset, list[str]]): Which languages are you following from this user?
    """

    blocked_by: bool
    blocking: bool
    domain_blocking: bool
    endorsed: bool
    followed_by: bool
    following: bool
    id: str
    muting: bool
    muting_notifications: bool
    note: str
    notifying: bool
    requested: bool
    requested_by: bool
    showing_reblogs: bool
    languages: Union[None, Unset, list[str]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        blocked_by = self.blocked_by

        blocking = self.blocking

        domain_blocking = self.domain_blocking

        endorsed = self.endorsed

        followed_by = self.followed_by

        following = self.following

        id = self.id

        muting = self.muting

        muting_notifications = self.muting_notifications

        note = self.note

        notifying = self.notifying

        requested = self.requested

        requested_by = self.requested_by

        showing_reblogs = self.showing_reblogs

        languages: Union[None, Unset, list[str]]
        if isinstance(self.languages, Unset):
            languages = UNSET
        elif isinstance(self.languages, list):
            languages = self.languages

        else:
            languages = self.languages

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "blocked_by": blocked_by,
                "blocking": blocking,
                "domain_blocking": domain_blocking,
                "endorsed": endorsed,
                "followed_by": followed_by,
                "following": following,
                "id": id,
                "muting": muting,
                "muting_notifications": muting_notifications,
                "note": note,
                "notifying": notifying,
                "requested": requested,
                "requested_by": requested_by,
                "showing_reblogs": showing_reblogs,
            }
        )
        if languages is not UNSET:
            field_dict["languages"] = languages

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        blocked_by = d.pop("blocked_by")

        blocking = d.pop("blocking")

        domain_blocking = d.pop("domain_blocking")

        endorsed = d.pop("endorsed")

        followed_by = d.pop("followed_by")

        following = d.pop("following")

        id = d.pop("id")

        muting = d.pop("muting")

        muting_notifications = d.pop("muting_notifications")

        note = d.pop("note")

        notifying = d.pop("notifying")

        requested = d.pop("requested")

        requested_by = d.pop("requested_by")

        showing_reblogs = d.pop("showing_reblogs")

        def _parse_languages(data: object) -> Union[None, Unset, list[str]]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                languages_type_0 = cast(list[str], data)

                return languages_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, list[str]], data)

        languages = _parse_languages(d.pop("languages", UNSET))

        relationship = cls(
            blocked_by=blocked_by,
            blocking=blocking,
            domain_blocking=domain_blocking,
            endorsed=endorsed,
            followed_by=followed_by,
            following=following,
            id=id,
            muting=muting,
            muting_notifications=muting_notifications,
            note=note,
            notifying=notifying,
            requested=requested,
            requested_by=requested_by,
            showing_reblogs=showing_reblogs,
            languages=languages,
        )

        relationship.additional_properties = d
        return relationship

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
