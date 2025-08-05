import datetime
from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    TypeVar,
    Union,
    cast,
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.filter_context import FilterContext
from ..models.filter_filter_action import FilterFilterAction
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.filter_keyword import FilterKeyword
    from ..models.filter_status import FilterStatus


T = TypeVar("T", bound="Filter")


@_attrs_define
class Filter:
    """Represents a user-defined filter for determining which statuses should not be shown to the user.

    Attributes:
        context (list[FilterContext]): The contexts in which the filter should be applied.
        filter_action (FilterFilterAction): The action to be taken when a status matches this filter.
        id (str): The ID of the Filter in the database.
        title (str): A title given by the user to name the filter.
        expires_at (Union[None, Unset, datetime.datetime]): When the filter should no longer be applied.
        keywords (Union[None, Unset, list['FilterKeyword']]): The keywords grouped under this filter. Omitted when part
            of a [FilterResult]({{< relref "entities/FilterResult" >}}).
        statuses (Union[None, Unset, list['FilterStatus']]): The statuses grouped under this filter. Omitted when part
            of a [FilterResult]({{< relref "entities/FilterResult" >}}).
    """

    context: list[FilterContext]
    filter_action: FilterFilterAction
    id: str
    title: str
    expires_at: Union[None, Unset, datetime.datetime] = UNSET
    keywords: Union[None, Unset, list["FilterKeyword"]] = UNSET
    statuses: Union[None, Unset, list["FilterStatus"]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        context = []
        for context_item_data in self.context:
            context_item = context_item_data.value
            context.append(context_item)

        filter_action = self.filter_action.value

        id = self.id

        title = self.title

        expires_at: Union[None, Unset, str]
        if isinstance(self.expires_at, Unset):
            expires_at = UNSET
        elif isinstance(self.expires_at, datetime.datetime):
            expires_at = self.expires_at.isoformat()
        else:
            expires_at = self.expires_at

        keywords: Union[None, Unset, list[dict[str, Any]]]
        if isinstance(self.keywords, Unset):
            keywords = UNSET
        elif isinstance(self.keywords, list):
            keywords = []
            for keywords_type_0_item_data in self.keywords:
                keywords_type_0_item = keywords_type_0_item_data.to_dict()
                keywords.append(keywords_type_0_item)

        else:
            keywords = self.keywords

        statuses: Union[None, Unset, list[dict[str, Any]]]
        if isinstance(self.statuses, Unset):
            statuses = UNSET
        elif isinstance(self.statuses, list):
            statuses = []
            for statuses_type_0_item_data in self.statuses:
                statuses_type_0_item = statuses_type_0_item_data.to_dict()
                statuses.append(statuses_type_0_item)

        else:
            statuses = self.statuses

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "context": context,
                "filter_action": filter_action,
                "id": id,
                "title": title,
            }
        )
        if expires_at is not UNSET:
            field_dict["expires_at"] = expires_at
        if keywords is not UNSET:
            field_dict["keywords"] = keywords
        if statuses is not UNSET:
            field_dict["statuses"] = statuses

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.filter_keyword import FilterKeyword
        from ..models.filter_status import FilterStatus

        d = dict(src_dict)
        context = []
        _context = d.pop("context")
        for context_item_data in _context:
            context_item = FilterContext(context_item_data)

            context.append(context_item)

        filter_action = FilterFilterAction(d.pop("filter_action"))

        id = d.pop("id")

        title = d.pop("title")

        def _parse_expires_at(data: object) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                expires_at_type_0 = isoparse(data)

                return expires_at_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

        expires_at = _parse_expires_at(d.pop("expires_at", UNSET))

        def _parse_keywords(data: object) -> Union[None, Unset, list["FilterKeyword"]]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                keywords_type_0 = []
                _keywords_type_0 = data
                for keywords_type_0_item_data in _keywords_type_0:
                    keywords_type_0_item = FilterKeyword.from_dict(
                        keywords_type_0_item_data
                    )

                    keywords_type_0.append(keywords_type_0_item)

                return keywords_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, list["FilterKeyword"]], data)

        keywords = _parse_keywords(d.pop("keywords", UNSET))

        def _parse_statuses(data: object) -> Union[None, Unset, list["FilterStatus"]]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                statuses_type_0 = []
                _statuses_type_0 = data
                for statuses_type_0_item_data in _statuses_type_0:
                    statuses_type_0_item = FilterStatus.from_dict(
                        statuses_type_0_item_data
                    )

                    statuses_type_0.append(statuses_type_0_item)

                return statuses_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, list["FilterStatus"]], data)

        statuses = _parse_statuses(d.pop("statuses", UNSET))

        filter_ = cls(
            context=context,
            filter_action=filter_action,
            id=id,
            title=title,
            expires_at=expires_at,
            keywords=keywords,
            statuses=statuses,
        )

        filter_.additional_properties = d
        return filter_

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
