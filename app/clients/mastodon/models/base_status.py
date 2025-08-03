import datetime
from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.visibility_enum import VisibilityEnum
from ..types import UNSET, Unset

T = TypeVar("T", bound="BaseStatus")


@_attrs_define
class BaseStatus:
    """Common fields for all status creation requests

    Attributes:
        in_reply_to_id (Union[Unset, str]): ID of the status being replied to, if status is a reply.
        language (Union[Unset, str]): ISO 639-1 language code for this status.
        scheduled_at (Union[Unset, datetime.datetime]): [Datetime] at which to schedule a status. Providing this
            parameter will cause ScheduledStatus to be returned instead of Status. Must be at least 5 minutes in the future.
        sensitive (Union[Unset, bool]): Mark status and attached media as sensitive? Defaults to false. Default: False.
        spoiler_text (Union[Unset, str]): Text to be shown as a warning or subject before the actual content. Statuses
            are generally collapsed behind this field.
        visibility (Union[Unset, VisibilityEnum]):

    """

    in_reply_to_id: Unset | str = UNSET
    language: Unset | str = UNSET
    scheduled_at: Unset | datetime.datetime = UNSET
    sensitive: Unset | bool = False
    spoiler_text: Unset | str = UNSET
    visibility: Unset | VisibilityEnum = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        in_reply_to_id = self.in_reply_to_id

        language = self.language

        scheduled_at: Unset | str = UNSET
        if not isinstance(self.scheduled_at, Unset):
            scheduled_at = self.scheduled_at.isoformat()

        sensitive = self.sensitive

        spoiler_text = self.spoiler_text

        visibility: Unset | str = UNSET
        if not isinstance(self.visibility, Unset):
            visibility = self.visibility.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if in_reply_to_id is not UNSET:
            field_dict["in_reply_to_id"] = in_reply_to_id
        if language is not UNSET:
            field_dict["language"] = language
        if scheduled_at is not UNSET:
            field_dict["scheduled_at"] = scheduled_at
        if sensitive is not UNSET:
            field_dict["sensitive"] = sensitive
        if spoiler_text is not UNSET:
            field_dict["spoiler_text"] = spoiler_text
        if visibility is not UNSET:
            field_dict["visibility"] = visibility

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        in_reply_to_id = d.pop("in_reply_to_id", UNSET)

        language = d.pop("language", UNSET)

        _scheduled_at = d.pop("scheduled_at", UNSET)
        scheduled_at: Unset | datetime.datetime
        if isinstance(_scheduled_at, Unset):
            scheduled_at = UNSET
        else:
            scheduled_at = isoparse(_scheduled_at)

        sensitive = d.pop("sensitive", UNSET)

        spoiler_text = d.pop("spoiler_text", UNSET)

        _visibility = d.pop("visibility", UNSET)
        visibility: Unset | VisibilityEnum
        if isinstance(_visibility, Unset):
            visibility = UNSET
        else:
            visibility = VisibilityEnum(_visibility)

        base_status = cls(
            in_reply_to_id=in_reply_to_id,
            language=language,
            scheduled_at=scheduled_at,
            sensitive=sensitive,
            spoiler_text=spoiler_text,
            visibility=visibility,
        )

        base_status.additional_properties = d
        return base_status

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
