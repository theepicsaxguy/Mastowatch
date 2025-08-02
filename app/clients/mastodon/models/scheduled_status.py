import datetime
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

if TYPE_CHECKING:
    from ..models.media_attachment import MediaAttachment
    from ..models.scheduled_status_params import ScheduledStatusParams


T = TypeVar("T", bound="ScheduledStatus")


@_attrs_define
class ScheduledStatus:
    """Represents a status that will be published at a future scheduled date.

    Attributes:
        id (str): ID of the scheduled status in the database.
        media_attachments (list['MediaAttachment']): Media that will be attached when the status is posted.
        params (ScheduledStatusParams): The parameters that were used when scheduling the status, to be used when the
            status is posted.
        scheduled_at (datetime.datetime): The timestamp for when the status will be posted.
    """

    id: str
    media_attachments: list["MediaAttachment"]
    params: "ScheduledStatusParams"
    scheduled_at: datetime.datetime
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        media_attachments = []
        for media_attachments_item_data in self.media_attachments:
            media_attachments_item = media_attachments_item_data.to_dict()
            media_attachments.append(media_attachments_item)

        params = self.params.to_dict()

        scheduled_at = self.scheduled_at.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "media_attachments": media_attachments,
                "params": params,
                "scheduled_at": scheduled_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.media_attachment import MediaAttachment
        from ..models.scheduled_status_params import ScheduledStatusParams

        d = src_dict.copy()
        id = d.pop("id")

        media_attachments = []
        _media_attachments = d.pop("media_attachments")
        for media_attachments_item_data in _media_attachments:
            media_attachments_item = MediaAttachment.from_dict(media_attachments_item_data)

            media_attachments.append(media_attachments_item)

        params = ScheduledStatusParams.from_dict(d.pop("params"))

        scheduled_at = isoparse(d.pop("scheduled_at"))

        scheduled_status = cls(
            id=id,
            media_attachments=media_attachments,
            params=params,
            scheduled_at=scheduled_at,
        )

        scheduled_status.additional_properties = d
        return scheduled_status

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
