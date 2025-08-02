import datetime
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

T = TypeVar("T", bound="AdminDomainAllow")


@_attrs_define
class AdminDomainAllow:
    """Represents a domain allowed to federate.

    Example:
        {'id': '1', 'domain': 'mastodon.social', 'created_at': '2022-09-14T21:23:02.755Z'}

    Attributes:
        created_at (datetime.datetime): When the domain was allowed to federate.
        domain (str): The domain that is allowed to federate.
        id (str): The ID of the DomainAllow in the database.
    """

    created_at: datetime.datetime
    domain: str
    id: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        created_at = self.created_at.isoformat()

        domain = self.domain

        id = self.id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "created_at": created_at,
                "domain": domain,
                "id": id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        created_at = isoparse(d.pop("created_at"))

        domain = d.pop("domain")

        id = d.pop("id")

        admin_domain_allow = cls(
            created_at=created_at,
            domain=domain,
            id=id,
        )

        admin_domain_allow.additional_properties = d
        return admin_domain_allow

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
