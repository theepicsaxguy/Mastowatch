import datetime
from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

T = TypeVar("T", bound="FeaturedTag")


@_attrs_define
class FeaturedTag:
    """Represents a hashtag that is featured on an account profile.

    Example:
        {'id': '627', 'name': 'nowplaying', 'url': 'https://mastodon.social/@trwnh/tagged/nowplaying', 'statuses_count':
            '70', 'last_status_at': '2022-08-29'}

    Attributes:
        id (str): The ID of the featured tag.
        last_status_at (datetime.date): The date of the last authored status containing this hashtag.
        name (str): The name of the hashtag being featured.
        statuses_count (str): The number of authored statuses containing this hashtag.
        url (str): A link to all statuses by a user that contain this hashtag.
    """

    id: str
    last_status_at: datetime.date
    name: str
    statuses_count: str
    url: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        last_status_at = self.last_status_at.isoformat()

        name = self.name

        statuses_count = self.statuses_count

        url = self.url

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "last_status_at": last_status_at,
                "name": name,
                "statuses_count": statuses_count,
                "url": url,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        last_status_at = isoparse(d.pop("last_status_at")).date()

        name = d.pop("name")

        statuses_count = d.pop("statuses_count")

        url = d.pop("url")

        featured_tag = cls(
            id=id,
            last_status_at=last_status_at,
            name=name,
            statuses_count=statuses_count,
            url=url,
        )

        featured_tag.additional_properties = d
        return featured_tag

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
