import datetime
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.relationship_severance_event_type import RelationshipSeveranceEventType

T = TypeVar("T", bound="RelationshipSeveranceEvent")


@_attrs_define
class RelationshipSeveranceEvent:
    """Summary of a moderation or block event that caused follow relationships to be severed.

    Attributes:
        created_at (datetime.datetime): When the event took place.
        followers_count (int): Number of followers that were removed as result of the event.
        following_count (int): Number of accounts the user stopped following as result of the event.
        id (str): The ID of the relationship severance event in the database.
        purged (bool): Whether the list of severed relationships is unavailable because the underlying issue has been
            purged.
        target_name (str): Name of the target of the moderation/block event. This is either a domain name or a user
            handle, depending on the event type.
        type_ (RelationshipSeveranceEventType): Type of event.
    """

    created_at: datetime.datetime
    followers_count: int
    following_count: int
    id: str
    purged: bool
    target_name: str
    type_: RelationshipSeveranceEventType
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        created_at = self.created_at.isoformat()

        followers_count = self.followers_count

        following_count = self.following_count

        id = self.id

        purged = self.purged

        target_name = self.target_name

        type_ = self.type_.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "created_at": created_at,
                "followers_count": followers_count,
                "following_count": following_count,
                "id": id,
                "purged": purged,
                "target_name": target_name,
                "type": type_,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        created_at = isoparse(d.pop("created_at"))

        followers_count = d.pop("followers_count")

        following_count = d.pop("following_count")

        id = d.pop("id")

        purged = d.pop("purged")

        target_name = d.pop("target_name")

        type_ = RelationshipSeveranceEventType(d.pop("type"))

        relationship_severance_event = cls(
            created_at=created_at,
            followers_count=followers_count,
            following_count=following_count,
            id=id,
            purged=purged,
            target_name=target_name,
            type_=type_,
        )

        relationship_severance_event.additional_properties = d
        return relationship_severance_event

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
