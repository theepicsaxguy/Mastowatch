from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="V1InstanceConfigurationStatuses")


@_attrs_define
class V1InstanceConfigurationStatuses:
    """Limits related to authoring statuses.

    Attributes:
        characters_reserved_per_url (int): Each URL in a status will be assumed to be exactly this many characters.
        max_characters (int): The maximum number of allowed characters per status.
        max_media_attachments (int): The maximum number of media attachments that can be added to a status.
    """

    characters_reserved_per_url: int
    max_characters: int
    max_media_attachments: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        characters_reserved_per_url = self.characters_reserved_per_url

        max_characters = self.max_characters

        max_media_attachments = self.max_media_attachments

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "characters_reserved_per_url": characters_reserved_per_url,
                "max_characters": max_characters,
                "max_media_attachments": max_media_attachments,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        characters_reserved_per_url = d.pop("characters_reserved_per_url")

        max_characters = d.pop("max_characters")

        max_media_attachments = d.pop("max_media_attachments")

        v1_instance_configuration_statuses = cls(
            characters_reserved_per_url=characters_reserved_per_url,
            max_characters=max_characters,
            max_media_attachments=max_media_attachments,
        )

        v1_instance_configuration_statuses.additional_properties = d
        return v1_instance_configuration_statuses

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
