from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.filter_ import Filter


T = TypeVar("T", bound="FilterResult")


@_attrs_define
class FilterResult:
    """Represents a filter whose keywords matched a given status.

    Example:
        {'filter': {'id': '3', 'title': 'Hide completely', 'context': ['home'], 'expires_at':
            '2022-09-20T17:27:39.296Z', 'filter_action': 'hide'}, 'keyword_matches': ['bad word'], 'status_matches':
            ['109031743575371913']}

    Attributes:
        filter_ (Filter): Represents a user-defined filter for determining which statuses should not be shown to the
            user. Example: {'id': '19972', 'title': 'Test filter', 'context': ['home'], 'expires_at':
            '2022-09-20T17:27:39.296Z', 'filter_action': 'warn', 'keywords': [{'id': '1197', 'keyword': 'bad word',
            'whole_word': False}], 'statuses': [{'id': '1', 'status_id': '109031743575371913'}]}.
        keyword_matches (Union[None, Unset, list[str]]): The keyword within the filter that was matched.
        status_matches (Union[None, Unset, list[str]]): The status ID within the filter that was matched.
    """

    filter_: "Filter"
    keyword_matches: Union[None, Unset, list[str]] = UNSET
    status_matches: Union[None, Unset, list[str]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        filter_ = self.filter_.to_dict()

        keyword_matches: Union[None, Unset, list[str]]
        if isinstance(self.keyword_matches, Unset):
            keyword_matches = UNSET
        elif isinstance(self.keyword_matches, list):
            keyword_matches = self.keyword_matches

        else:
            keyword_matches = self.keyword_matches

        status_matches: Union[None, Unset, list[str]]
        if isinstance(self.status_matches, Unset):
            status_matches = UNSET
        elif isinstance(self.status_matches, list):
            status_matches = self.status_matches

        else:
            status_matches = self.status_matches

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "filter": filter_,
            }
        )
        if keyword_matches is not UNSET:
            field_dict["keyword_matches"] = keyword_matches
        if status_matches is not UNSET:
            field_dict["status_matches"] = status_matches

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.filter_ import Filter

        d = src_dict.copy()
        filter_ = Filter.from_dict(d.pop("filter"))

        def _parse_keyword_matches(data: object) -> Union[None, Unset, list[str]]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                keyword_matches_type_0 = cast(list[str], data)

                return keyword_matches_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, list[str]], data)

        keyword_matches = _parse_keyword_matches(d.pop("keyword_matches", UNSET))

        def _parse_status_matches(data: object) -> Union[None, Unset, list[str]]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                status_matches_type_0 = cast(list[str], data)

                return status_matches_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, list[str]], data)

        status_matches = _parse_status_matches(d.pop("status_matches", UNSET))

        filter_result = cls(
            filter_=filter_,
            keyword_matches=keyword_matches,
            status_matches=status_matches,
        )

        filter_result.additional_properties = d
        return filter_result

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
