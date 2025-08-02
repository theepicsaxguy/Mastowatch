from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="PostAccountFollowBody")


@_attrs_define
class PostAccountFollowBody:
    """
    Attributes:
        languages (Union[Unset, list[str]]): Array of String (ISO 639-1 language two-letter code). Filter received
            statuses for these languages. If not provided, you will receive this account's posts in all languages.
        notify (Union[Unset, bool]): Receive notifications when this account posts a status? Defaults to false. Default:
            False.
        reblogs (Union[Unset, bool]): Receive this account's reblogs in home timeline? Defaults to true. Default: True.
    """

    languages: Union[Unset, list[str]] = UNSET
    notify: Union[Unset, bool] = False
    reblogs: Union[Unset, bool] = True
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        languages: Union[Unset, list[str]] = UNSET
        if not isinstance(self.languages, Unset):
            languages = self.languages

        notify = self.notify

        reblogs = self.reblogs

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if languages is not UNSET:
            field_dict["languages"] = languages
        if notify is not UNSET:
            field_dict["notify"] = notify
        if reblogs is not UNSET:
            field_dict["reblogs"] = reblogs

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        languages = cast(list[str], d.pop("languages", UNSET))

        notify = d.pop("notify", UNSET)

        reblogs = d.pop("reblogs", UNSET)

        post_account_follow_body = cls(
            languages=languages,
            notify=notify,
            reblogs=reblogs,
        )

        post_account_follow_body.additional_properties = d
        return post_account_follow_body

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
