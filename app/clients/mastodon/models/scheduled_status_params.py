from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.scheduled_status_params_visibility import ScheduledStatusParamsVisibility
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.scheduled_status_params_poll_type_0 import (
        ScheduledStatusParamsPollType0,
    )


T = TypeVar("T", bound="ScheduledStatusParams")


@_attrs_define
class ScheduledStatusParams:
    """The parameters that were used when scheduling the status, to be used when the status is posted.

    Attributes:
        application_id (int): Internal ID of the Application that posted the status. Provided for historical
            compatibility only and can be ignored.
        text (str): Text to be used as status content.
        visibility (ScheduledStatusParamsVisibility): The visibility that the status will have once it is posted.
        with_rate_limit (bool): Whether status creation is subject to rate limiting. Provided for historical
            compatibility only and can be ignored.
        idempotency (Union[None, Unset, str]): Idempotency key to prevent duplicate statuses.
        in_reply_to_id (Union[None, Unset, int]): ID of the Status that will be replied to.
        language (Union[None, Unset, str]): The language that will be used for the status.
        media_ids (Union[None, Unset, list[str]]): IDs of the MediaAttachments that will be attached to the status.
        poll (Union['ScheduledStatusParamsPollType0', None, Unset]): Poll to be attached to the status.
        scheduled_at (Union[None, Unset, str]): When the status will be scheduled. This will be null because the status
            is only scheduled once.
        sensitive (Union[None, Unset, bool]): Whether the status will be marked as sensitive.
        spoiler_text (Union[None, Unset, str]): The text of the content warning or summary for the status.
    """

    application_id: int
    text: str
    visibility: ScheduledStatusParamsVisibility
    with_rate_limit: bool
    idempotency: Union[None, Unset, str] = UNSET
    in_reply_to_id: Union[None, Unset, int] = UNSET
    language: Union[None, Unset, str] = UNSET
    media_ids: Union[None, Unset, list[str]] = UNSET
    poll: Union["ScheduledStatusParamsPollType0", None, Unset] = UNSET
    scheduled_at: Union[None, Unset, str] = UNSET
    sensitive: Union[None, Unset, bool] = UNSET
    spoiler_text: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.scheduled_status_params_poll_type_0 import (
            ScheduledStatusParamsPollType0,
        )

        application_id = self.application_id

        text = self.text

        visibility = self.visibility.value

        with_rate_limit = self.with_rate_limit

        idempotency: Union[None, Unset, str]
        if isinstance(self.idempotency, Unset):
            idempotency = UNSET
        else:
            idempotency = self.idempotency

        in_reply_to_id: Union[None, Unset, int]
        if isinstance(self.in_reply_to_id, Unset):
            in_reply_to_id = UNSET
        else:
            in_reply_to_id = self.in_reply_to_id

        language: Union[None, Unset, str]
        if isinstance(self.language, Unset):
            language = UNSET
        else:
            language = self.language

        media_ids: Union[None, Unset, list[str]]
        if isinstance(self.media_ids, Unset):
            media_ids = UNSET
        elif isinstance(self.media_ids, list):
            media_ids = self.media_ids

        else:
            media_ids = self.media_ids

        poll: Union[None, Unset, dict[str, Any]]
        if isinstance(self.poll, Unset):
            poll = UNSET
        elif isinstance(self.poll, ScheduledStatusParamsPollType0):
            poll = self.poll.to_dict()
        else:
            poll = self.poll

        scheduled_at: Union[None, Unset, str]
        if isinstance(self.scheduled_at, Unset):
            scheduled_at = UNSET
        else:
            scheduled_at = self.scheduled_at

        sensitive: Union[None, Unset, bool]
        if isinstance(self.sensitive, Unset):
            sensitive = UNSET
        else:
            sensitive = self.sensitive

        spoiler_text: Union[None, Unset, str]
        if isinstance(self.spoiler_text, Unset):
            spoiler_text = UNSET
        else:
            spoiler_text = self.spoiler_text

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "application_id": application_id,
                "text": text,
                "visibility": visibility,
                "with_rate_limit": with_rate_limit,
            }
        )
        if idempotency is not UNSET:
            field_dict["idempotency"] = idempotency
        if in_reply_to_id is not UNSET:
            field_dict["in_reply_to_id"] = in_reply_to_id
        if language is not UNSET:
            field_dict["language"] = language
        if media_ids is not UNSET:
            field_dict["media_ids"] = media_ids
        if poll is not UNSET:
            field_dict["poll"] = poll
        if scheduled_at is not UNSET:
            field_dict["scheduled_at"] = scheduled_at
        if sensitive is not UNSET:
            field_dict["sensitive"] = sensitive
        if spoiler_text is not UNSET:
            field_dict["spoiler_text"] = spoiler_text

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.scheduled_status_params_poll_type_0 import (
            ScheduledStatusParamsPollType0,
        )

        d = src_dict.copy()
        application_id = d.pop("application_id")

        text = d.pop("text")

        visibility = ScheduledStatusParamsVisibility(d.pop("visibility"))

        with_rate_limit = d.pop("with_rate_limit")

        def _parse_idempotency(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        idempotency = _parse_idempotency(d.pop("idempotency", UNSET))

        def _parse_in_reply_to_id(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        in_reply_to_id = _parse_in_reply_to_id(d.pop("in_reply_to_id", UNSET))

        def _parse_language(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        language = _parse_language(d.pop("language", UNSET))

        def _parse_media_ids(data: object) -> Union[None, Unset, list[str]]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                media_ids_type_0 = cast(list[str], data)

                return media_ids_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, list[str]], data)

        media_ids = _parse_media_ids(d.pop("media_ids", UNSET))

        def _parse_poll(
            data: object,
        ) -> Union["ScheduledStatusParamsPollType0", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                poll_type_0 = ScheduledStatusParamsPollType0.from_dict(data)

                return poll_type_0
            except:  # noqa: E722
                pass
            return cast(Union["ScheduledStatusParamsPollType0", None, Unset], data)

        poll = _parse_poll(d.pop("poll", UNSET))

        def _parse_scheduled_at(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        scheduled_at = _parse_scheduled_at(d.pop("scheduled_at", UNSET))

        def _parse_sensitive(data: object) -> Union[None, Unset, bool]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, bool], data)

        sensitive = _parse_sensitive(d.pop("sensitive", UNSET))

        def _parse_spoiler_text(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        spoiler_text = _parse_spoiler_text(d.pop("spoiler_text", UNSET))

        scheduled_status_params = cls(
            application_id=application_id,
            text=text,
            visibility=visibility,
            with_rate_limit=with_rate_limit,
            idempotency=idempotency,
            in_reply_to_id=in_reply_to_id,
            language=language,
            media_ids=media_ids,
            poll=poll,
            scheduled_at=scheduled_at,
            sensitive=sensitive,
            spoiler_text=spoiler_text,
        )

        scheduled_status_params.additional_properties = d
        return scheduled_status_params

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
