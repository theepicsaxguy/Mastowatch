from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="PollOption")


@_attrs_define
class PollOption:
    """Additional entity definition for Poll::Option

    Attributes:
        title (str): The text value of the poll option.
        votes_count (Union[None, Unset, int]): The total number of received votes for this option.
    """

    title: str
    votes_count: Union[None, Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        title = self.title

        votes_count: Union[None, Unset, int]
        if isinstance(self.votes_count, Unset):
            votes_count = UNSET
        else:
            votes_count = self.votes_count

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "title": title,
            }
        )
        if votes_count is not UNSET:
            field_dict["votes_count"] = votes_count

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        title = d.pop("title")

        def _parse_votes_count(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        votes_count = _parse_votes_count(d.pop("votes_count", UNSET))

        poll_option = cls(
            title=title,
            votes_count=votes_count,
        )

        poll_option.additional_properties = d
        return poll_option

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
