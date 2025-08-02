from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="PutPushSubscriptionBodyDataAlerts")


@_attrs_define
class PutPushSubscriptionBodyDataAlerts:
    """
    Attributes:
        mention (Union[Unset, bool]): Receive mention notifications? Defaults to false.
        status (Union[Unset, bool]): Receive new subscribed account notifications? Defaults to false.
        reblog (Union[Unset, bool]): Receive reblog notifications? Defaults to false.
        follow (Union[Unset, bool]): Receive follow notifications? Defaults to false.
        follow_request (Union[Unset, bool]): Receive follow request notifications? Defaults to false.
        favourite (Union[Unset, bool]): Receive favourite notifications? Defaults to false.
        poll (Union[Unset, bool]): Receive poll notifications? Defaults to false.
        update (Union[Unset, bool]): Receive status edited notifications? Defaults to false.
        admin_sign_up (Union[Unset, bool]): Receive new user signup notifications? Defaults to false. Must have a role
            with the appropriate permissions.
        admin_report (Union[Unset, bool]): Receive new report notifications? Defaults to false. Must have a role with
            the appropriate permissions.
    """

    mention: Union[Unset, bool] = UNSET
    status: Union[Unset, bool] = UNSET
    reblog: Union[Unset, bool] = UNSET
    follow: Union[Unset, bool] = UNSET
    follow_request: Union[Unset, bool] = UNSET
    favourite: Union[Unset, bool] = UNSET
    poll: Union[Unset, bool] = UNSET
    update: Union[Unset, bool] = UNSET
    admin_sign_up: Union[Unset, bool] = UNSET
    admin_report: Union[Unset, bool] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        mention = self.mention

        status = self.status

        reblog = self.reblog

        follow = self.follow

        follow_request = self.follow_request

        favourite = self.favourite

        poll = self.poll

        update = self.update

        admin_sign_up = self.admin_sign_up

        admin_report = self.admin_report

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if mention is not UNSET:
            field_dict["mention"] = mention
        if status is not UNSET:
            field_dict["status"] = status
        if reblog is not UNSET:
            field_dict["reblog"] = reblog
        if follow is not UNSET:
            field_dict["follow"] = follow
        if follow_request is not UNSET:
            field_dict["follow_request"] = follow_request
        if favourite is not UNSET:
            field_dict["favourite"] = favourite
        if poll is not UNSET:
            field_dict["poll"] = poll
        if update is not UNSET:
            field_dict["update"] = update
        if admin_sign_up is not UNSET:
            field_dict["admin.sign_up"] = admin_sign_up
        if admin_report is not UNSET:
            field_dict["admin.report"] = admin_report

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        mention = d.pop("mention", UNSET)

        status = d.pop("status", UNSET)

        reblog = d.pop("reblog", UNSET)

        follow = d.pop("follow", UNSET)

        follow_request = d.pop("follow_request", UNSET)

        favourite = d.pop("favourite", UNSET)

        poll = d.pop("poll", UNSET)

        update = d.pop("update", UNSET)

        admin_sign_up = d.pop("admin.sign_up", UNSET)

        admin_report = d.pop("admin.report", UNSET)

        put_push_subscription_body_data_alerts = cls(
            mention=mention,
            status=status,
            reblog=reblog,
            follow=follow,
            follow_request=follow_request,
            favourite=favourite,
            poll=poll,
            update=update,
            admin_sign_up=admin_sign_up,
            admin_report=admin_report,
        )

        put_push_subscription_body_data_alerts.additional_properties = d
        return put_push_subscription_body_data_alerts

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
