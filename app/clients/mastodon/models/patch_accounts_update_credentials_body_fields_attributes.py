from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="PatchAccountsUpdateCredentialsBodyFieldsAttributes")


@_attrs_define
class PatchAccountsUpdateCredentialsBodyFieldsAttributes:
    """The profile fields to be set. Inside this hash, the key is an integer cast to a string (although the exact integer
    does not matter), and the value is another hash including `name` and `value`. By default, max 4 fields.

    """

    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        patch_accounts_update_credentials_body_fields_attributes = cls()

        patch_accounts_update_credentials_body_fields_attributes.additional_properties = d
        return patch_accounts_update_credentials_body_fields_attributes

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
