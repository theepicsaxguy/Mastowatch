from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.web_push_subscription_alerts import WebPushSubscriptionAlerts


T = TypeVar("T", bound="WebPushSubscription")


@_attrs_define
class WebPushSubscription:
    """Represents a subscription to the push streaming server.

    Example:
        {'id': 328183, 'endpoint': 'https://yourdomain.example/listener', 'standard': True, 'alerts': {'follow': False,
            'favourite': False, 'reblog': False, 'mention': True, 'poll': False}, 'server_key': 'BCk-
            QqERU0q-CfYZjcuB6lnyyOYfJ2AifKqfeGIm7Z-HiTU5T9eTG5GxVA0_OH5mMlI4UkkDTpaZwozy0TzdZ2M='}

    Attributes:
        alerts (WebPushSubscriptionAlerts): Which alerts should be delivered to the `endpoint`.
        endpoint (str): Where push alerts will be sent to.
        id (str): The ID of the Web Push subscription in the database.
        server_key (str): The streaming server's VAPID key.
        standard (bool): If the push messages follow the standardized specifications (RFC8030+RFC8291+RFC8292). Else
            they follow a legacy version of the specifications (4th draft of RFC8291 and 1st draft of RFC8292).
    """

    alerts: "WebPushSubscriptionAlerts"
    endpoint: str
    id: str
    server_key: str
    standard: bool
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        alerts = self.alerts.to_dict()

        endpoint = self.endpoint

        id = self.id

        server_key = self.server_key

        standard = self.standard

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "alerts": alerts,
                "endpoint": endpoint,
                "id": id,
                "server_key": server_key,
                "standard": standard,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.web_push_subscription_alerts import \
            WebPushSubscriptionAlerts

        d = src_dict.copy()
        alerts = WebPushSubscriptionAlerts.from_dict(d.pop("alerts"))

        endpoint = d.pop("endpoint")

        id = d.pop("id")

        server_key = d.pop("server_key")

        standard = d.pop("standard")

        web_push_subscription = cls(
            alerts=alerts,
            endpoint=endpoint,
            id=id,
            server_key=server_key,
            standard=standard,
        )

        web_push_subscription.additional_properties = d
        return web_push_subscription

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
