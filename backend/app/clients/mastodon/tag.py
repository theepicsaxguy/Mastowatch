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

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.tag_history import TagHistory


T = TypeVar("T", bound="Tag")


@_attrs_define
class Tag:
    """Represents a hashtag used within the content of a status.

    Attributes:
        history (list['TagHistory']): Usage statistics for given days (typically the past week).
        id (str): ID of the hashtag in the database. Useful for constructing URLs for the moderation tools & Admin API.
        name (str): The value of the hashtag after the # sign.
        url (str): A link to the hashtag on the instance.
        featuring (Union[None, Unset, bool]): Whether the current token's authorized user is featuring this tag on their
            profile.
        following (Union[None, Unset, bool]): Whether the current token's authorized user is following this tag.
    """

    history: list["TagHistory"]
    id: str
    name: str
    url: str
    featuring: Union[None, Unset, bool] = UNSET
    following: Union[None, Unset, bool] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        history = []
        for history_item_data in self.history:
            history_item = history_item_data.to_dict()
            history.append(history_item)

        id = self.id

        name = self.name

        url = self.url

        featuring: Union[None, Unset, bool]
        if isinstance(self.featuring, Unset):
            featuring = UNSET
        else:
            featuring = self.featuring

        following: Union[None, Unset, bool]
        if isinstance(self.following, Unset):
            following = UNSET
        else:
            following = self.following

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "history": history,
                "id": id,
                "name": name,
                "url": url,
            }
        )
        if featuring is not UNSET:
            field_dict["featuring"] = featuring
        if following is not UNSET:
            field_dict["following"] = following

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.tag_history import TagHistory

        d = dict(src_dict)
        history = []
        _history = d.pop("history")
        for history_item_data in _history:
            history_item = TagHistory.from_dict(history_item_data)

            history.append(history_item)

        id = d.pop("id")

        name = d.pop("name")

        url = d.pop("url")

        def _parse_featuring(data: object) -> Union[None, Unset, bool]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, bool], data)

        featuring = _parse_featuring(d.pop("featuring", UNSET))

        def _parse_following(data: object) -> Union[None, Unset, bool]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, bool], data)

        following = _parse_following(d.pop("following", UNSET))

        tag = cls(
            history=history,
            id=id,
            name=name,
            url=url,
            featuring=featuring,
            following=following,
        )

        tag.additional_properties = d
        return tag

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
