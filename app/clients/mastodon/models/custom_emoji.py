from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="CustomEmoji")


@_attrs_define
class CustomEmoji:
    """Represents a custom emoji.

    Example:
        {'shortcode': 'blobaww', 'url':
            'https://files.mastodon.social/custom_emojis/images/000/011/739/original/blobaww.png', 'static_url':
            'https://files.mastodon.social/custom_emojis/images/000/011/739/static/blobaww.png', 'visible_in_picker': True,
            'category': 'Blobs'}

    Attributes:
        shortcode (str): The name of the custom emoji.
        static_url (str): A link to a static copy of the custom emoji.
        url (str): A link to the custom emoji.
        visible_in_picker (bool): Whether this Emoji should be visible in the picker or unlisted.
        category (Union[None, Unset, str]): Used for sorting custom emoji in the picker.

    """

    shortcode: str
    static_url: str
    url: str
    visible_in_picker: bool
    category: None | Unset | str = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        shortcode = self.shortcode

        static_url = self.static_url

        url = self.url

        visible_in_picker = self.visible_in_picker

        category: None | Unset | str
        if isinstance(self.category, Unset):
            category = UNSET
        else:
            category = self.category

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "shortcode": shortcode,
                "static_url": static_url,
                "url": url,
                "visible_in_picker": visible_in_picker,
            }
        )
        if category is not UNSET:
            field_dict["category"] = category

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        shortcode = d.pop("shortcode")

        static_url = d.pop("static_url")

        url = d.pop("url")

        visible_in_picker = d.pop("visible_in_picker")

        def _parse_category(data: object) -> None | Unset | str:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | Unset | str, data)

        category = _parse_category(d.pop("category", UNSET))

        custom_emoji = cls(
            shortcode=shortcode,
            static_url=static_url,
            url=url,
            visible_in_picker=visible_in_picker,
            category=category,
        )

        custom_emoji.additional_properties = d
        return custom_emoji

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
