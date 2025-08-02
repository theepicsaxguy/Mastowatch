from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.put_push_subscription_body_data import PutPushSubscriptionBodyData


T = TypeVar("T", bound="PutPushSubscriptionBody")


@_attrs_define
class PutPushSubscriptionBody:
    """
    Attributes:
        data (Union[Unset, PutPushSubscriptionBodyData]): Object containing properties
        policy (Union[Unset, str]): Specify whether to receive push notifications from `all`, `followed`, `follower`, or
            `none` users.
    """

    data: Union[Unset, "PutPushSubscriptionBodyData"] = UNSET
    policy: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        data: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.data, Unset):
            data = self.data.to_dict()

        policy = self.policy

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if data is not UNSET:
            field_dict["data"] = data
        if policy is not UNSET:
            field_dict["policy"] = policy

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.put_push_subscription_body_data import PutPushSubscriptionBodyData

        d = src_dict.copy()
        _data = d.pop("data", UNSET)
        data: Union[Unset, PutPushSubscriptionBodyData]
        if isinstance(_data, Unset):
            data = UNSET
        else:
            data = PutPushSubscriptionBodyData.from_dict(_data)

        policy = d.pop("policy", UNSET)

        put_push_subscription_body = cls(
            data=data,
            policy=policy,
        )

        put_push_subscription_body.additional_properties = d
        return put_push_subscription_body

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
