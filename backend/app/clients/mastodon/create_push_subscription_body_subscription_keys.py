from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
    Union,
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="CreatePushSubscriptionBodySubscriptionKeys")


@_attrs_define
class CreatePushSubscriptionBodySubscriptionKeys:
    """
    Attributes:
        p256dh (Union[Unset, str]): User agent public key. Base64 encoded string of a public key from a ECDH keypair
            using the `prime256v1` curve.
        auth (Union[Unset, str]): Auth secret. Base64 encoded string of 16 bytes of random data.
    """

    p256dh: Union[Unset, str] = UNSET
    auth: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        p256dh = self.p256dh

        auth = self.auth

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if p256dh is not UNSET:
            field_dict["p256dh"] = p256dh
        if auth is not UNSET:
            field_dict["auth"] = auth

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        p256dh = d.pop("p256dh", UNSET)

        auth = d.pop("auth", UNSET)

        create_push_subscription_body_subscription_keys = cls(
            p256dh=p256dh,
            auth=auth,
        )

        create_push_subscription_body_subscription_keys.additional_properties = d
        return create_push_subscription_body_subscription_keys

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
