from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="UpdateFiltersKeywordsByIdV2Body")


@_attrs_define
class UpdateFiltersKeywordsByIdV2Body:
    """
    Attributes:
        keyword (str): The keyword to be added to the filter group.
        whole_word (Union[Unset, bool]): Whether the keyword should consider word boundaries.

    """

    keyword: str
    whole_word: Unset | bool = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        keyword = self.keyword

        whole_word = self.whole_word

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "keyword": keyword,
            }
        )
        if whole_word is not UNSET:
            field_dict["whole_word"] = whole_word

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        keyword = d.pop("keyword")

        whole_word = d.pop("whole_word", UNSET)

        update_filters_keywords_by_id_v2_body = cls(
            keyword=keyword,
            whole_word=whole_word,
        )

        update_filters_keywords_by_id_v2_body.additional_properties = d
        return update_filters_keywords_by_id_v2_body

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
