from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.patch_accounts_update_credentials_body_source_privacy import (
    PatchAccountsUpdateCredentialsBodySourcePrivacy,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="PatchAccountsUpdateCredentialsBodySource")


@_attrs_define
class PatchAccountsUpdateCredentialsBodySource:
    """Object containing properties

    Attributes:
        privacy (Union[Unset, PatchAccountsUpdateCredentialsBodySourcePrivacy]): Default post privacy for authored
            statuses. Can be `public`, `unlisted`, or `private`.
        sensitive (Union[Unset, bool]): Whether to mark authored statuses as sensitive by default.
        language (Union[Unset, str]): Default language to use for authored statuses (ISO 639-1)
    """

    privacy: Union[Unset, PatchAccountsUpdateCredentialsBodySourcePrivacy] = UNSET
    sensitive: Union[Unset, bool] = UNSET
    language: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        privacy: Union[Unset, str] = UNSET
        if not isinstance(self.privacy, Unset):
            privacy = self.privacy.value

        sensitive = self.sensitive

        language = self.language

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if privacy is not UNSET:
            field_dict["privacy"] = privacy
        if sensitive is not UNSET:
            field_dict["sensitive"] = sensitive
        if language is not UNSET:
            field_dict["language"] = language

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        _privacy = d.pop("privacy", UNSET)
        privacy: Union[Unset, PatchAccountsUpdateCredentialsBodySourcePrivacy]
        if isinstance(_privacy, Unset):
            privacy = UNSET
        else:
            privacy = PatchAccountsUpdateCredentialsBodySourcePrivacy(_privacy)

        sensitive = d.pop("sensitive", UNSET)

        language = d.pop("language", UNSET)

        patch_accounts_update_credentials_body_source = cls(
            privacy=privacy,
            sensitive=sensitive,
            language=language,
        )

        patch_accounts_update_credentials_body_source.additional_properties = d
        return patch_accounts_update_credentials_body_source

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
