from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
    Union,
    cast,
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="InstanceConfigurationUrls")


@_attrs_define
class InstanceConfigurationUrls:
    """URLs of interest for clients apps.

    Attributes:
        about (str): The URL of the server's about page.
        streaming (str): The Websockets URL for connecting to the streaming API.
        privacy_policy (Union[None, Unset, str]): The URL of the server's privacy policy.
        terms_of_service (Union[None, Unset, str]): The URL of the server's current terms of service, if any.
    """

    about: str
    streaming: str
    privacy_policy: Union[None, Unset, str] = UNSET
    terms_of_service: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        about = self.about

        streaming = self.streaming

        privacy_policy: Union[None, Unset, str]
        if isinstance(self.privacy_policy, Unset):
            privacy_policy = UNSET
        else:
            privacy_policy = self.privacy_policy

        terms_of_service: Union[None, Unset, str]
        if isinstance(self.terms_of_service, Unset):
            terms_of_service = UNSET
        else:
            terms_of_service = self.terms_of_service

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "about": about,
                "streaming": streaming,
            }
        )
        if privacy_policy is not UNSET:
            field_dict["privacy_policy"] = privacy_policy
        if terms_of_service is not UNSET:
            field_dict["terms_of_service"] = terms_of_service

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        about = d.pop("about")

        streaming = d.pop("streaming")

        def _parse_privacy_policy(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        privacy_policy = _parse_privacy_policy(d.pop("privacy_policy", UNSET))

        def _parse_terms_of_service(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        terms_of_service = _parse_terms_of_service(d.pop("terms_of_service", UNSET))

        instance_configuration_urls = cls(
            about=about,
            streaming=streaming,
            privacy_policy=privacy_policy,
            terms_of_service=terms_of_service,
        )

        instance_configuration_urls.additional_properties = d
        return instance_configuration_urls

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
