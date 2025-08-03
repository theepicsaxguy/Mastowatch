from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.translation_attachment import TranslationAttachment
    from ..models.translation_poll import TranslationPoll


T = TypeVar("T", bound="Translation")


@_attrs_define
class Translation:
    """Represents the result of machine translating some status content

    Attributes:
        content (str): HTML-encoded translated content of the status.
        detected_source_language (str): The language of the source text, as auto-detected by the machine translation
            provider.
        media_attachments (list['TranslationAttachment']): The translated media descriptions of the status.
        provider (str): The service that provided the machine translation.
        spoiler_text (str): The translated spoiler warning of the status.
        poll (Union['TranslationPoll', None, Unset]): The translated poll of the status.

    """

    content: str
    detected_source_language: str
    media_attachments: list["TranslationAttachment"]
    provider: str
    spoiler_text: str
    poll: Union["TranslationPoll", None, Unset] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.translation_poll import TranslationPoll

        content = self.content

        detected_source_language = self.detected_source_language

        media_attachments = []
        for media_attachments_item_data in self.media_attachments:
            media_attachments_item = media_attachments_item_data.to_dict()
            media_attachments.append(media_attachments_item)

        provider = self.provider

        spoiler_text = self.spoiler_text

        poll: None | Unset | dict[str, Any]
        if isinstance(self.poll, Unset):
            poll = UNSET
        elif isinstance(self.poll, TranslationPoll):
            poll = self.poll.to_dict()
        else:
            poll = self.poll

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "content": content,
                "detected_source_language": detected_source_language,
                "media_attachments": media_attachments,
                "provider": provider,
                "spoiler_text": spoiler_text,
            }
        )
        if poll is not UNSET:
            field_dict["poll"] = poll

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.translation_attachment import TranslationAttachment
        from ..models.translation_poll import TranslationPoll

        d = dict(src_dict)
        content = d.pop("content")

        detected_source_language = d.pop("detected_source_language")

        media_attachments = []
        _media_attachments = d.pop("media_attachments")
        for media_attachments_item_data in _media_attachments:
            media_attachments_item = TranslationAttachment.from_dict(media_attachments_item_data)

            media_attachments.append(media_attachments_item)

        provider = d.pop("provider")

        spoiler_text = d.pop("spoiler_text")

        def _parse_poll(data: object) -> Union["TranslationPoll", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                poll_type_0 = TranslationPoll.from_dict(data)

                return poll_type_0
            except:  # noqa: E722
                pass
            return cast(Union["TranslationPoll", None, Unset], data)

        poll = _parse_poll(d.pop("poll", UNSET))

        translation = cls(
            content=content,
            detected_source_language=detected_source_language,
            media_attachments=media_attachments,
            provider=provider,
            spoiler_text=spoiler_text,
            poll=poll,
        )

        translation.additional_properties = d
        return translation

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
