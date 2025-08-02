from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="V1InstanceConfigurationPolls")


@_attrs_define
class V1InstanceConfigurationPolls:
    """Limits related to polls.

    Attributes:
        max_characters_per_option (int): Each poll option is allowed to have this many characters.
        max_expiration (int): The longest allowed poll duration, in seconds.
        max_options (int): Each poll is allowed to have up to this many options.
        min_expiration (int): The shortest allowed poll duration, in seconds.
    """

    max_characters_per_option: int
    max_expiration: int
    max_options: int
    min_expiration: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        max_characters_per_option = self.max_characters_per_option

        max_expiration = self.max_expiration

        max_options = self.max_options

        min_expiration = self.min_expiration

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "max_characters_per_option": max_characters_per_option,
                "max_expiration": max_expiration,
                "max_options": max_options,
                "min_expiration": min_expiration,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        max_characters_per_option = d.pop("max_characters_per_option")

        max_expiration = d.pop("max_expiration")

        max_options = d.pop("max_options")

        min_expiration = d.pop("min_expiration")

        v1_instance_configuration_polls = cls(
            max_characters_per_option=max_characters_per_option,
            max_expiration=max_expiration,
            max_options=max_options,
            min_expiration=min_expiration,
        )

        v1_instance_configuration_polls.additional_properties = d
        return v1_instance_configuration_polls

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
