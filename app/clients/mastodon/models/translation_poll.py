from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.translation_poll_option import TranslationPollOption


T = TypeVar("T", bound="TranslationPoll")


@_attrs_define
class TranslationPoll:
    """Additional entity definition for Translation::Poll

    Attributes:
        id (str): The ID of the poll.
        options (list['TranslationPollOption']): The translated poll options.

    """

    id: str
    options: list["TranslationPollOption"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        options = []
        for options_item_data in self.options:
            options_item = options_item_data.to_dict()
            options.append(options_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "options": options,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.translation_poll_option import TranslationPollOption

        d = dict(src_dict)
        id = d.pop("id")

        options = []
        _options = d.pop("options")
        for options_item_data in _options:
            options_item = TranslationPollOption.from_dict(options_item_data)

            options.append(options_item)

        translation_poll = cls(
            id=id,
            options=options,
        )

        translation_poll.additional_properties = d
        return translation_poll

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
