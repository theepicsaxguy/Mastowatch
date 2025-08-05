import datetime
from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    TypeVar,
    Union,
    cast,
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.notification_type_enum import NotificationTypeEnum
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.account import Account
    from ..models.account_warning import AccountWarning
    from ..models.relationship_severance_event import RelationshipSeveranceEvent
    from ..models.report import Report
    from ..models.status import Status


T = TypeVar("T", bound="Notification")


@_attrs_define
class Notification:
    """Represents a notification of an event relevant to the user.

    Attributes:
        account (Account): Represents a user of Mastodon and their associated profile.
        created_at (datetime.datetime): The timestamp of the notification.
        group_key (str): Group key shared by similar notifications, to be used in the grouped notifications feature.
            Should be considered opaque, but ungrouped notifications can be assumed to have a `group_key` of the form
            `ungrouped-{notification_id}`.
        id (str): The id of the notification in the database.
        type_ (NotificationTypeEnum):
        event (Union['RelationshipSeveranceEvent', None, Unset]): Summary of the event that caused follow relationships
            to be severed. Attached when `type` of the notification is `severed_relationships`.
        moderation_warning (Union['AccountWarning', None, Unset]): Moderation warning that caused the notification.
            Attached when `type` of the notification is `moderation_warning`.
        report (Union['Report', None, Unset]): Report that was the object of the notification. Attached when `type` of
            the notification is `admin.report`.
        status (Union['Status', None, Unset]): Status that was the object of the notification. Attached when `type` of
            the notification is `favourite`, `reblog`, `status`, `mention`, `poll`, or `update`.
    """

    account: "Account"
    created_at: datetime.datetime
    group_key: str
    id: str
    type_: NotificationTypeEnum
    event: Union["RelationshipSeveranceEvent", None, Unset] = UNSET
    moderation_warning: Union["AccountWarning", None, Unset] = UNSET
    report: Union["Report", None, Unset] = UNSET
    status: Union["Status", None, Unset] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.account_warning import AccountWarning
        from ..models.relationship_severance_event import RelationshipSeveranceEvent
        from ..models.report import Report
        from ..models.status import Status

        account = self.account.to_dict()

        created_at = self.created_at.isoformat()

        group_key = self.group_key

        id = self.id

        type_ = self.type_.value

        event: Union[None, Unset, dict[str, Any]]
        if isinstance(self.event, Unset):
            event = UNSET
        elif isinstance(self.event, RelationshipSeveranceEvent):
            event = self.event.to_dict()
        else:
            event = self.event

        moderation_warning: Union[None, Unset, dict[str, Any]]
        if isinstance(self.moderation_warning, Unset):
            moderation_warning = UNSET
        elif isinstance(self.moderation_warning, AccountWarning):
            moderation_warning = self.moderation_warning.to_dict()
        else:
            moderation_warning = self.moderation_warning

        report: Union[None, Unset, dict[str, Any]]
        if isinstance(self.report, Unset):
            report = UNSET
        elif isinstance(self.report, Report):
            report = self.report.to_dict()
        else:
            report = self.report

        status: Union[None, Unset, dict[str, Any]]
        if isinstance(self.status, Unset):
            status = UNSET
        elif isinstance(self.status, Status):
            status = self.status.to_dict()
        else:
            status = self.status

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "account": account,
                "created_at": created_at,
                "group_key": group_key,
                "id": id,
                "type": type_,
            }
        )
        if event is not UNSET:
            field_dict["event"] = event
        if moderation_warning is not UNSET:
            field_dict["moderation_warning"] = moderation_warning
        if report is not UNSET:
            field_dict["report"] = report
        if status is not UNSET:
            field_dict["status"] = status

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.account import Account
        from ..models.account_warning import AccountWarning
        from ..models.relationship_severance_event import RelationshipSeveranceEvent
        from ..models.report import Report
        from ..models.status import Status

        d = dict(src_dict)
        account = Account.from_dict(d.pop("account"))

        created_at = isoparse(d.pop("created_at"))

        group_key = d.pop("group_key")

        id = d.pop("id")

        type_ = NotificationTypeEnum(d.pop("type"))

        def _parse_event(
            data: object,
        ) -> Union["RelationshipSeveranceEvent", None, Unset]:
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

        def _parse_moderation_warning(
            data: object,
        ) -> Union["AccountWarning", None, Unset]:
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

        moderation_warning = _parse_moderation_warning(
            d.pop("moderation_warning", UNSET)
        )

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

        def _parse_status(data: object) -> Union["Status", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                status_type_0 = Status.from_dict(data)

                return status_type_0
            except:  # noqa: E722
                pass
            return cast(Union["Status", None, Unset], data)

        status = _parse_status(d.pop("status", UNSET))

        notification = cls(
            account=account,
            created_at=created_at,
            group_key=group_key,
            id=id,
            type_=type_,
            event=event,
            moderation_warning=moderation_warning,
            report=report,
            status=status,
        )

        notification.additional_properties = d
        return notification

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
