import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.notification_type_enum import NotificationTypeEnum
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.account_warning import AccountWarning
    from ..models.relationship_severance_event import RelationshipSeveranceEvent
    from ..models.report import Report


T = TypeVar("T", bound="NotificationGroup")


@_attrs_define
class NotificationGroup:
    """### Attributes

    Attributes:
        group_key (str): Group key identifying the grouped notifications. Should be treated as an opaque value.
        most_recent_notification_id (str): ID of the most recent notification in the group.
        notifications_count (int): Total number of individual notifications that are part of this notification group.
        sample_account_ids (list[str]): IDs of some of the accounts who most recently triggered notifications in this
            group.
        type_ (NotificationTypeEnum):
        event (Union['RelationshipSeveranceEvent', None, Unset]): Summary of the event that caused follow relationships
            to be severed. Attached when `type` of the notification is `severed_relationships`.
        latest_page_notification_at (Union[None, Unset, datetime.datetime]): Date at which the most recent notification
            from this group within the current page has been created. This is only returned when paginating through
            notification groups.
        moderation_warning (Union['AccountWarning', None, Unset]): Moderation warning that caused the notification.
            Attached when `type` of the notification is `moderation_warning`.
        page_max_id (Union[None, Unset, str]): ID of the newest notification from this group represented within the
            current page. This is only returned when paginating through notification groups. Useful when polling new
            notifications.
        page_min_id (Union[None, Unset, str]): ID of the oldest notification from this group represented within the
            current page. This is only returned when paginating through notification groups. Useful when polling new
            notifications.
        report (Union['Report', None, Unset]): Report that was the object of the notification. Attached when `type` of
            the notification is `admin.report`.
        status_id (Union[None, Unset, str]): ID of the [Status]({{< relref "entities/Status" >}}) that was the object of
            the notification. Attached when `type` of the notification is `favourite`, `reblog`, `status`, `mention`,
            `poll`, or `update`.

    """

    group_key: str
    most_recent_notification_id: str
    notifications_count: int
    sample_account_ids: list[str]
    type_: NotificationTypeEnum
    event: Union["RelationshipSeveranceEvent", None, Unset] = UNSET
    latest_page_notification_at: None | Unset | datetime.datetime = UNSET
    moderation_warning: Union["AccountWarning", None, Unset] = UNSET
    page_max_id: None | Unset | str = UNSET
    page_min_id: None | Unset | str = UNSET
    report: Union["Report", None, Unset] = UNSET
    status_id: None | Unset | str = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.account_warning import AccountWarning
        from ..models.relationship_severance_event import RelationshipSeveranceEvent
        from ..models.report import Report

        group_key = self.group_key

        most_recent_notification_id = self.most_recent_notification_id

        notifications_count = self.notifications_count

        sample_account_ids = self.sample_account_ids

        type_ = self.type_.value

        event: None | Unset | dict[str, Any]
        if isinstance(self.event, Unset):
            event = UNSET
        elif isinstance(self.event, RelationshipSeveranceEvent):
            event = self.event.to_dict()
        else:
            event = self.event

        latest_page_notification_at: None | Unset | str
        if isinstance(self.latest_page_notification_at, Unset):
            latest_page_notification_at = UNSET
        elif isinstance(self.latest_page_notification_at, datetime.datetime):
            latest_page_notification_at = self.latest_page_notification_at.isoformat()
        else:
            latest_page_notification_at = self.latest_page_notification_at

        moderation_warning: None | Unset | dict[str, Any]
        if isinstance(self.moderation_warning, Unset):
            moderation_warning = UNSET
        elif isinstance(self.moderation_warning, AccountWarning):
            moderation_warning = self.moderation_warning.to_dict()
        else:
            moderation_warning = self.moderation_warning

        page_max_id: None | Unset | str
        if isinstance(self.page_max_id, Unset):
            page_max_id = UNSET
        else:
            page_max_id = self.page_max_id

        page_min_id: None | Unset | str
        if isinstance(self.page_min_id, Unset):
            page_min_id = UNSET
        else:
            page_min_id = self.page_min_id

        report: None | Unset | dict[str, Any]
        if isinstance(self.report, Unset):
            report = UNSET
        elif isinstance(self.report, Report):
            report = self.report.to_dict()
        else:
            report = self.report

        status_id: None | Unset | str
        if isinstance(self.status_id, Unset):
            status_id = UNSET
        else:
            status_id = self.status_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "group_key": group_key,
                "most_recent_notification_id": most_recent_notification_id,
                "notifications_count": notifications_count,
                "sample_account_ids": sample_account_ids,
                "type": type_,
            }
        )
        if event is not UNSET:
            field_dict["event"] = event
        if latest_page_notification_at is not UNSET:
            field_dict["latest_page_notification_at"] = latest_page_notification_at
        if moderation_warning is not UNSET:
            field_dict["moderation_warning"] = moderation_warning
        if page_max_id is not UNSET:
            field_dict["page_max_id"] = page_max_id
        if page_min_id is not UNSET:
            field_dict["page_min_id"] = page_min_id
        if report is not UNSET:
            field_dict["report"] = report
        if status_id is not UNSET:
            field_dict["status_id"] = status_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.account_warning import AccountWarning
        from ..models.relationship_severance_event import RelationshipSeveranceEvent
        from ..models.report import Report

        d = dict(src_dict)
        group_key = d.pop("group_key")

        most_recent_notification_id = d.pop("most_recent_notification_id")

        notifications_count = d.pop("notifications_count")

        sample_account_ids = cast(list[str], d.pop("sample_account_ids"))

        type_ = NotificationTypeEnum(d.pop("type"))

        def _parse_event(data: object) -> Union["RelationshipSeveranceEvent", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                event_type_0 = RelationshipSeveranceEvent.from_dict(data)

                return event_type_0
            except:  # noqa: E722
                pass
            return cast(Union["RelationshipSeveranceEvent", None, Unset], data)

        event = _parse_event(d.pop("event", UNSET))

        def _parse_latest_page_notification_at(data: object) -> None | Unset | datetime.datetime:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                latest_page_notification_at_type_0 = isoparse(data)

                return latest_page_notification_at_type_0
            except:  # noqa: E722
                pass
            return cast(None | Unset | datetime.datetime, data)

        latest_page_notification_at = _parse_latest_page_notification_at(d.pop("latest_page_notification_at", UNSET))

        def _parse_moderation_warning(data: object) -> Union["AccountWarning", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                moderation_warning_type_0 = AccountWarning.from_dict(data)

                return moderation_warning_type_0
            except:  # noqa: E722
                pass
            return cast(Union["AccountWarning", None, Unset], data)

        moderation_warning = _parse_moderation_warning(d.pop("moderation_warning", UNSET))

        def _parse_page_max_id(data: object) -> None | Unset | str:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | Unset | str, data)

        page_max_id = _parse_page_max_id(d.pop("page_max_id", UNSET))

        def _parse_page_min_id(data: object) -> None | Unset | str:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | Unset | str, data)

        page_min_id = _parse_page_min_id(d.pop("page_min_id", UNSET))

        def _parse_report(data: object) -> Union["Report", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                report_type_0 = Report.from_dict(data)

                return report_type_0
            except:  # noqa: E722
                pass
            return cast(Union["Report", None, Unset], data)

        report = _parse_report(d.pop("report", UNSET))

        def _parse_status_id(data: object) -> None | Unset | str:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | Unset | str, data)

        status_id = _parse_status_id(d.pop("status_id", UNSET))

        notification_group = cls(
            group_key=group_key,
            most_recent_notification_id=most_recent_notification_id,
            notifications_count=notifications_count,
            sample_account_ids=sample_account_ids,
            type_=type_,
            event=event,
            latest_page_notification_at=latest_page_notification_at,
            moderation_warning=moderation_warning,
            page_max_id=page_max_id,
            page_min_id=page_min_id,
            report=report,
            status_id=status_id,
        )

        notification_group.additional_properties = d
        return notification_group

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
