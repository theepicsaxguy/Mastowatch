from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
    Union,
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="UpdateFilterV2BodyKeywordsAttributesItem")


@_attrs_define
class UpdateFilterV2BodyKeywordsAttributesItem:
    """
    Attributes:
        keyword (Union[Unset, str]): A keyword to be added to the newly-created filter group.
        whole_word (Union[Unset, bool]): Whether the keyword should consider word boundaries.
        id (Union[Unset, str]): Provide the ID of an existing keyword to modify it, instead of creating a new keyword.
        field_destroy (Union[Unset, bool]): If true, will remove the keyword with the given ID.
    """

    keyword: Union[Unset, str] = UNSET
    whole_word: Union[Unset, bool] = UNSET
    id: Union[Unset, str] = UNSET
    field_destroy: Union[Unset, bool] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        keyword = self.keyword

        whole_word = self.whole_word

        id = self.id

        field_destroy = self.field_destroy

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if keyword is not UNSET:
            field_dict["keyword"] = keyword
        if whole_word is not UNSET:
            field_dict["whole_word"] = whole_word
        if id is not UNSET:
            field_dict["id"] = id
        if field_destroy is not UNSET:
            field_dict["_destroy"] = field_destroy

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        keyword = d.pop("keyword", UNSET)

        whole_word = d.pop("whole_word", UNSET)

        id = d.pop("id", UNSET)

        field_destroy = d.pop("_destroy", UNSET)

        update_filter_v2_body_keywords_attributes_item = cls(
            keyword=keyword,
            whole_word=whole_word,
            id=id,
            field_destroy=field_destroy,
        )

        update_filter_v2_body_keywords_attributes_item.additional_properties = d
        return update_filter_v2_body_keywords_attributes_item

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
