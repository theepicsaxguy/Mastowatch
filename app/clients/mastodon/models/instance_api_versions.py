from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="InstanceApiVersions")


@_attrs_define
class InstanceApiVersions:
    """Information about which version of the API is implemented by this server. It contains at least a `mastodon`
    attribute, and other implementations may have their own additional attributes.

        Attributes:
            mastodon (int): API version number that this server implements. Starting from Mastodon v4.3.0, API changes will
                come with a version number, which clients can check against this value.
    """

    mastodon: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        mastodon = self.mastodon

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "mastodon": mastodon,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        mastodon = d.pop("mastodon")

        instance_api_versions = cls(
            mastodon=mastodon,
        )

        instance_api_versions.additional_properties = d
        return instance_api_versions

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
