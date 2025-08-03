from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.update_status_body_poll import UpdateStatusBodyPoll


T = TypeVar("T", bound="UpdateStatusBody")


@_attrs_define
class UpdateStatusBody:
    """
    Attributes:
        language (Union[Unset, str]): ISO 639-1 language code for the status.
        media_attributes (Union[Unset, list[str]]): Each array includes id, description, and focus.
        media_ids (Union[Unset, list[str]]): Include Attachment IDs to be attached as media. If provided, `status`
            becomes optional, and `poll` cannot be used.
        poll (Union[Unset, UpdateStatusBodyPoll]): Object containing properties
        sensitive (Union[Unset, bool]): Whether the status should be marked as sensitive.
        spoiler_text (Union[Unset, str]): The plain text subject or content warning of the status.
        status (Union[Unset, str]): The plain text content of the status.

    """

    language: Unset | str = UNSET
    media_attributes: Unset | list[str] = UNSET
    media_ids: Unset | list[str] = UNSET
    poll: Union[Unset, "UpdateStatusBodyPoll"] = UNSET
    sensitive: Unset | bool = UNSET
    spoiler_text: Unset | str = UNSET
    status: Unset | str = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        language = self.language

        media_attributes: Unset | list[str] = UNSET
        if not isinstance(self.media_attributes, Unset):
            media_attributes = self.media_attributes

        media_ids: Unset | list[str] = UNSET
        if not isinstance(self.media_ids, Unset):
            media_ids = self.media_ids

        poll: Unset | dict[str, Any] = UNSET
        if not isinstance(self.poll, Unset):
            poll = self.poll.to_dict()

        sensitive = self.sensitive

        spoiler_text = self.spoiler_text

        status = self.status

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if language is not UNSET:
            field_dict["language"] = language
        if media_attributes is not UNSET:
            field_dict["media_attributes[]"] = media_attributes
        if media_ids is not UNSET:
            field_dict["media_ids"] = media_ids
        if poll is not UNSET:
            field_dict["poll"] = poll
        if sensitive is not UNSET:
            field_dict["sensitive"] = sensitive
        if spoiler_text is not UNSET:
            field_dict["spoiler_text"] = spoiler_text
        if status is not UNSET:
            field_dict["status"] = status

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.update_status_body_poll import UpdateStatusBodyPoll

        d = dict(src_dict)
        language = d.pop("language", UNSET)

        media_attributes = cast(list[str], d.pop("media_attributes[]", UNSET))

        media_ids = cast(list[str], d.pop("media_ids", UNSET))

        _poll = d.pop("poll", UNSET)
        poll: Unset | UpdateStatusBodyPoll
        if isinstance(_poll, Unset):
            poll = UNSET
        else:
            poll = UpdateStatusBodyPoll.from_dict(_poll)

        sensitive = d.pop("sensitive", UNSET)

        spoiler_text = d.pop("spoiler_text", UNSET)

        status = d.pop("status", UNSET)

        update_status_body = cls(
            language=language,
            media_attributes=media_attributes,
            media_ids=media_ids,
            poll=poll,
            sensitive=sensitive,
            spoiler_text=spoiler_text,
            status=status,
        )

        update_status_body.additional_properties = d
        return update_status_body

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
