import datetime
from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

T = TypeVar("T", bound="IdentityProof")


@_attrs_define
class IdentityProof:
    """Represents a proof from an external identity provider.

    Attributes:
        profile_url (str): The account owner's profile URL on the identity provider.
        proof_url (str): A link to a statement of identity proof, hosted by the identity provider.
        provider (str): The name of the identity provider.
        provider_username (str): The account owner's username on the identity provider's service.
        updated_at (datetime.datetime): When the identity proof was last updated.
    """

    profile_url: str
    proof_url: str
    provider: str
    provider_username: str
    updated_at: datetime.datetime
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        profile_url = self.profile_url

        proof_url = self.proof_url

        provider = self.provider

        provider_username = self.provider_username

        updated_at = self.updated_at.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "profile_url": profile_url,
                "proof_url": proof_url,
                "provider": provider,
                "provider_username": provider_username,
                "updated_at": updated_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        profile_url = d.pop("profile_url")

        proof_url = d.pop("proof_url")

        provider = d.pop("provider")

        provider_username = d.pop("provider_username")

        updated_at = isoparse(d.pop("updated_at"))

        identity_proof = cls(
            profile_url=profile_url,
            proof_url=proof_url,
            provider=provider,
            provider_username=provider_username,
            updated_at=updated_at,
        )

        identity_proof.additional_properties = d
        return identity_proof

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
