from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.create_push_subscription_body_subscription_keys import CreatePushSubscriptionBodySubscriptionKeys


T = TypeVar("T", bound="CreatePushSubscriptionBodySubscription")


@_attrs_define
class CreatePushSubscriptionBodySubscription:
    """Object containing properties

    Attributes:
        keys (Union[Unset, CreatePushSubscriptionBodySubscriptionKeys]):
        endpoint (Union[Unset, str]): The endpoint URL that is called when a notification event occurs.
        standard (Union[Unset, bool]): Follow standardized webpush (RFC8030+RFC8291+RFC8292) ? Else follow legacy
            webpush (unpublished version, 4th draft of RFC8291 and 1st draft of RFC8292). Defaults to false.

    """

    keys: Union[Unset, "CreatePushSubscriptionBodySubscriptionKeys"] = UNSET
    endpoint: Unset | str = UNSET
    standard: Unset | bool = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        keys: Unset | dict[str, Any] = UNSET
        if not isinstance(self.keys, Unset):
            keys = self.keys.to_dict()

        endpoint = self.endpoint

        standard = self.standard

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if keys is not UNSET:
            field_dict["keys"] = keys
        if endpoint is not UNSET:
            field_dict["endpoint"] = endpoint
        if standard is not UNSET:
            field_dict["standard"] = standard

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.create_push_subscription_body_subscription_keys import CreatePushSubscriptionBodySubscriptionKeys

        d = dict(src_dict)
        _keys = d.pop("keys", UNSET)
        keys: Unset | CreatePushSubscriptionBodySubscriptionKeys
        if isinstance(_keys, Unset):
            keys = UNSET
        else:
            keys = CreatePushSubscriptionBodySubscriptionKeys.from_dict(_keys)

        endpoint = d.pop("endpoint", UNSET)

        standard = d.pop("standard", UNSET)

        create_push_subscription_body_subscription = cls(
            keys=keys,
            endpoint=endpoint,
            standard=standard,
        )

        create_push_subscription_body_subscription.additional_properties = d
        return create_push_subscription_body_subscription

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
