from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.create_push_subscription_body_data import CreatePushSubscriptionBodyData
    from ..models.create_push_subscription_body_subscription import CreatePushSubscriptionBodySubscription


T = TypeVar("T", bound="CreatePushSubscriptionBody")


@_attrs_define
class CreatePushSubscriptionBody:
    """
    Attributes:
        subscription (CreatePushSubscriptionBodySubscription): Object containing properties
        data (Union[Unset, CreatePushSubscriptionBodyData]): Object containing properties

    """

    subscription: "CreatePushSubscriptionBodySubscription"
    data: Union[Unset, "CreatePushSubscriptionBodyData"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        subscription = self.subscription.to_dict()

        data: Unset | dict[str, Any] = UNSET
        if not isinstance(self.data, Unset):
            data = self.data.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "subscription": subscription,
            }
        )
        if data is not UNSET:
            field_dict["data"] = data

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.create_push_subscription_body_data import CreatePushSubscriptionBodyData
        from ..models.create_push_subscription_body_subscription import CreatePushSubscriptionBodySubscription

        d = dict(src_dict)
        subscription = CreatePushSubscriptionBodySubscription.from_dict(d.pop("subscription"))

        _data = d.pop("data", UNSET)
        data: Unset | CreatePushSubscriptionBodyData
        if isinstance(_data, Unset):
            data = UNSET
        else:
            data = CreatePushSubscriptionBodyData.from_dict(_data)

        create_push_subscription_body = cls(
            subscription=subscription,
            data=data,
        )

        create_push_subscription_body.additional_properties = d
        return create_push_subscription_body

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
