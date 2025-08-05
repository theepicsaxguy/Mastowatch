from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="Role")


@_attrs_define
class Role:
    """Represents a custom user role that grants permissions.

    Attributes:
        color (str): The hex code assigned to this role. If no hex code is assigned, the string will be empty.
        highlighted (bool): Whether the role is publicly visible as a badge on user profiles.
        id (str): The ID of the Role in the database.
        name (str): The name of the role.
        permissions (str): A bitmask that represents the sum of all permissions granted to the role.
    """

    color: str
    highlighted: bool
    id: str
    name: str
    permissions: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        color = self.color

        highlighted = self.highlighted

        id = self.id

        name = self.name

        permissions = self.permissions

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "color": color,
                "highlighted": highlighted,
                "id": id,
                "name": name,
                "permissions": permissions,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        color = d.pop("color")

        highlighted = d.pop("highlighted")

        id = d.pop("id")

        name = d.pop("name")

        permissions = d.pop("permissions")

        role = cls(
            color=color,
            highlighted=highlighted,
            id=id,
            name=name,
            permissions=permissions,
        )

        role.additional_properties = d
        return role

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
