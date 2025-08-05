from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="AdminCanonicalEmailBlock")


@_attrs_define
class AdminCanonicalEmailBlock:
    """Represents a canonical email block (hashed).

    Example:
        {'id': '2', 'canonical_email_hash': 'b344e55d11b3fc25d0d53194e0475838bf17e9be67ce3e6469956222d9a34f9c'}

    Attributes:
        canonical_email_hash (str): The SHA256 hash of the canonical email address.
        id (str): The ID of the email block in the database.
    """

    canonical_email_hash: str
    id: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        canonical_email_hash = self.canonical_email_hash

        id = self.id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "canonical_email_hash": canonical_email_hash,
                "id": id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        canonical_email_hash = d.pop("canonical_email_hash")

        id = d.pop("id")

        admin_canonical_email_block = cls(
            canonical_email_hash=canonical_email_hash,
            id=id,
        )

        admin_canonical_email_block.additional_properties = d
        return admin_canonical_email_block

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
