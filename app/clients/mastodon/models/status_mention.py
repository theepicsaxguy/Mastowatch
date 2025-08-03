from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="StatusMention")


@_attrs_define
class StatusMention:
    """Additional entity definition for Status::Mention

    Attributes:
        acct (str): The webfinger acct: URI of the mentioned user. Equivalent to `username` for local users, or
            `username@domain` for remote users.
        id (str): The account ID of the mentioned user.
        url (str): The location of the mentioned user's profile.
        username (str): The username of the mentioned user.

    """

    acct: str
    id: str
    url: str
    username: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        acct = self.acct

        id = self.id

        url = self.url

        username = self.username

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "acct": acct,
                "id": id,
                "url": url,
                "username": username,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        acct = d.pop("acct")

        id = d.pop("id")

        url = d.pop("url")

        username = d.pop("username")

        status_mention = cls(
            acct=acct,
            id=id,
            url=url,
            username=username,
        )

        status_mention.additional_properties = d
        return status_mention

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
