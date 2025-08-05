from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="WebPushSubscriptionAlerts")


@_attrs_define
class WebPushSubscriptionAlerts:
    """Which alerts should be delivered to the `endpoint`.

    Attributes:
        admin_report (bool): Receive a push notification when a new report has been filed?
        admin_sign_up (bool): Receive a push notification when a new user has signed up?
        favourite (bool): Receive a push notification when a status you created has been favourited by someone else?
        follow (bool): Receive a push notification when someone has followed you?
        follow_request (bool): Receive a push notification when someone has requested to followed you?
        mention (bool): Receive a push notification when someone else has mentioned you in a status?
        poll (bool): Receive a push notification when a poll you voted in or created has ended?
        reblog (bool): Receive a push notification when a status you created has been boosted by someone else?
        status (bool): Receive a push notification when a subscribed account posts a status?
        update (bool): Receive a push notification when a status you interacted with has been edited?
    """

    admin_report: bool
    admin_sign_up: bool
    favourite: bool
    follow: bool
    follow_request: bool
    mention: bool
    poll: bool
    reblog: bool
    status: bool
    update: bool
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        admin_report = self.admin_report

        admin_sign_up = self.admin_sign_up

        favourite = self.favourite

        follow = self.follow

        follow_request = self.follow_request

        mention = self.mention

        poll = self.poll

        reblog = self.reblog

        status = self.status

        update = self.update

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "admin.report": admin_report,
                "admin.sign_up": admin_sign_up,
                "favourite": favourite,
                "follow": follow,
                "follow_request": follow_request,
                "mention": mention,
                "poll": poll,
                "reblog": reblog,
                "status": status,
                "update": update,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        admin_report = d.pop("admin.report")

        admin_sign_up = d.pop("admin.sign_up")

        favourite = d.pop("favourite")

        follow = d.pop("follow")

        follow_request = d.pop("follow_request")

        mention = d.pop("mention")

        poll = d.pop("poll")

        reblog = d.pop("reblog")

        status = d.pop("status")

        update = d.pop("update")

        web_push_subscription_alerts = cls(
            admin_report=admin_report,
            admin_sign_up=admin_sign_up,
            favourite=favourite,
            follow=follow,
            follow_request=follow_request,
            mention=mention,
            poll=poll,
            reblog=reblog,
            status=status,
            update=update,
        )

        web_push_subscription_alerts.additional_properties = d
        return web_push_subscription_alerts

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
