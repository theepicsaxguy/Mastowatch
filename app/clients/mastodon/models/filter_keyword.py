from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="FilterKeyword")


@_attrs_define
class FilterKeyword:
    """Represents a keyword that, if matched, should cause the filter action to be taken.

    Example:
        {'id': '1197', 'keyword': 'bad word', 'whole_word': False}

    Attributes:
        id (str): The ID of the FilterKeyword in the database.
        keyword (str): The phrase to be matched against.
        whole_word (bool): Should the filter consider word boundaries? See [implementation guidelines for filters]({{<
            relref "api/guidelines#filters" >}}).
    """

    id: str
    keyword: str
    whole_word: bool
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        keyword = self.keyword

        whole_word = self.whole_word

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "keyword": keyword,
                "whole_word": whole_word,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        keyword = d.pop("keyword")

        whole_word = d.pop("whole_word")

        filter_keyword = cls(
            id=id,
            keyword=keyword,
            whole_word=whole_word,
        )

        filter_keyword.additional_properties = d
        return filter_keyword

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
