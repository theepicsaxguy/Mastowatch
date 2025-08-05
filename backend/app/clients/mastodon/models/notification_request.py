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

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.account import Account
    from ..models.status import Status


T = TypeVar("T", bound="NotificationRequest")


@_attrs_define
class NotificationRequest:
    """Represents a group of filtered notifications from a specific user.

    Attributes:
        account (Account): Represents a user of Mastodon and their associated profile.
        created_at (datetime.datetime): The timestamp of the notification request, i.e. when the first filtered
            notification from that user was created.
        id (str): The id of the notification request in the database.
        notifications_count (str): How many of this account's notifications were filtered.
        updated_at (datetime.datetime): The timestamp of when the notification request was last updated.
        last_status (Union['Status', None, Unset]): Most recent status associated with a filtered notification from that
            account.
    """

    account: "Account"
    created_at: datetime.datetime
    id: str
    notifications_count: str
    updated_at: datetime.datetime
    last_status: Union["Status", None, Unset] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.status import Status

        account = self.account.to_dict()

        created_at = self.created_at.isoformat()

        id = self.id

        notifications_count = self.notifications_count

        updated_at = self.updated_at.isoformat()

        last_status: Union[None, Unset, dict[str, Any]]
        if isinstance(self.last_status, Unset):
            last_status = UNSET
        elif isinstance(self.last_status, Status):
            last_status = self.last_status.to_dict()
        else:
            last_status = self.last_status

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "account": account,
                "created_at": created_at,
                "id": id,
                "notifications_count": notifications_count,
                "updated_at": updated_at,
            }
        )
        if last_status is not UNSET:
            field_dict["last_status"] = last_status

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.account import Account
        from ..models.status import Status

        d = dict(src_dict)
        account = Account.from_dict(d.pop("account"))

        created_at = isoparse(d.pop("created_at"))

        id = d.pop("id")

        notifications_count = d.pop("notifications_count")

        updated_at = isoparse(d.pop("updated_at"))

        def _parse_last_status(data: object) -> Union["Status", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                last_status_type_0 = Status.from_dict(data)

                return last_status_type_0
            except:  # noqa: E722
                pass
            return cast(Union["Status", None, Unset], data)

        last_status = _parse_last_status(d.pop("last_status", UNSET))

        notification_request = cls(
            account=account,
            created_at=created_at,
            id=id,
            notifications_count=notifications_count,
            updated_at=updated_at,
            last_status=last_status,
        )

        notification_request.additional_properties = d
        return notification_request

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
