from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
    Union,
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.filter_context import FilterContext
from ..types import UNSET, Unset

T = TypeVar("T", bound="UpdateFilterBody")


@_attrs_define
class UpdateFilterBody:
    """
    Attributes:
        context (list[FilterContext]): Specify at least one of `home`, `notifications`, `public`, `thread`, `account`.
        phrase (str): The text to be filtered.
        expires_in (Union[Unset, int]): Number of seconds from now that the filter should expire. Otherwise, `null` for
            a filter that doesn't expire.
        irreversible (Union[Unset, bool]): Should the server irreversibly drop matching entities from home and
            notifications? Defaults to false. Default: False.
        whole_word (Union[Unset, bool]): Should the filter consider word boundaries? Defaults to false. Default: False.
    """

    context: list[FilterContext]
    phrase: str
    expires_in: Union[Unset, int] = UNSET
    irreversible: Union[Unset, bool] = False
    whole_word: Union[Unset, bool] = False
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        context = []
        for context_item_data in self.context:
            context_item = context_item_data.value
            context.append(context_item)

        phrase = self.phrase

        expires_in = self.expires_in

        irreversible = self.irreversible

        whole_word = self.whole_word

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "context": context,
                "phrase": phrase,
            }
        )
        if expires_in is not UNSET:
            field_dict["expires_in"] = expires_in
        if irreversible is not UNSET:
            field_dict["irreversible"] = irreversible
        if whole_word is not UNSET:
            field_dict["whole_word"] = whole_word

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        context = []
        _context = d.pop("context")
        for context_item_data in _context:
            context_item = FilterContext(context_item_data)

            context.append(context_item)

        phrase = d.pop("phrase")

        expires_in = d.pop("expires_in", UNSET)

        irreversible = d.pop("irreversible", UNSET)

        whole_word = d.pop("whole_word", UNSET)

        update_filter_body = cls(
            context=context,
            phrase=phrase,
            expires_in=expires_in,
            irreversible=irreversible,
            whole_word=whole_word,
        )

        update_filter_body.additional_properties = d
        return update_filter_body

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
