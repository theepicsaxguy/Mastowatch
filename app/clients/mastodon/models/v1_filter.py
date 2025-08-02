import datetime
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.filter_context import FilterContext
from ..types import UNSET, Unset

T = TypeVar("T", bound="V1Filter")


@_attrs_define
class V1Filter:
    """Represents a user-defined filter for determining which statuses should not be shown to the user. Contains a single
    keyword or phrase.

        Example:
            {'id': '8449', 'phrase': 'test', 'context': ['home', 'notifications', 'public', 'thread'], 'whole_word': False,
                'expires_at': '2019-11-26T09:08:06.254Z', 'irreversible': True}

        Attributes:
            context (list[FilterContext]): The contexts in which the filter should be applied.
            id (str): The ID of the filter in the database.
            irreversible (bool): Should matching entities in home and notifications be dropped by the server? See
                [implementation guidelines for filters]({{< relref "api/guidelines#filters" >}}).
            phrase (str): The text to be filtered.
            whole_word (bool): Should the filter consider word boundaries? See [implementation guidelines for filters]({{<
                relref "api/guidelines#filters" >}}).
            expires_at (Union[None, Unset, datetime.datetime]): When the filter should no longer be applied.
    """

    context: list[FilterContext]
    id: str
    irreversible: bool
    phrase: str
    whole_word: bool
    expires_at: Union[None, Unset, datetime.datetime] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        context = []
        for context_item_data in self.context:
            context_item = context_item_data.value
            context.append(context_item)

        id = self.id

        irreversible = self.irreversible

        phrase = self.phrase

        whole_word = self.whole_word

        expires_at: Union[None, Unset, str]
        if isinstance(self.expires_at, Unset):
            expires_at = UNSET
        elif isinstance(self.expires_at, datetime.datetime):
            expires_at = self.expires_at.isoformat()
        else:
            expires_at = self.expires_at

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "context": context,
                "id": id,
                "irreversible": irreversible,
                "phrase": phrase,
                "whole_word": whole_word,
            }
        )
        if expires_at is not UNSET:
            field_dict["expires_at"] = expires_at

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        context = []
        _context = d.pop("context")
        for context_item_data in _context:
            context_item = FilterContext(context_item_data)

            context.append(context_item)

        id = d.pop("id")

        irreversible = d.pop("irreversible")

        phrase = d.pop("phrase")

        whole_word = d.pop("whole_word")

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

        v1_filter = cls(
            context=context,
            id=id,
            irreversible=irreversible,
            phrase=phrase,
            whole_word=whole_word,
            expires_at=expires_at,
        )

        v1_filter.additional_properties = d
        return v1_filter

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
