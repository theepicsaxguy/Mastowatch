from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
    Union,
    cast,
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="OEmbedResponse")


@_attrs_define
class OEmbedResponse:
    """Response schema for Get OEmbed info as JSON

    Example:
        {'type': 'rich', 'version': '1.0', 'title': 'New status by trwnh', 'author_name': 'infinite love ⴳ',
            'author_url': 'https://mastodon.social/@trwnh', 'provider_name': 'mastodon.social', 'provider_url':
            'https://mastodon.social/', 'cache_age': 86400, 'html': '<iframe
            src="https://mastodon.social/@trwnh/99664077509711321/embed" class="mastodon-embed" style="max-width: 100%;
            border: 0" width="400" allowfullscreen="allowfullscreen"></iframe><script src="https://mastodon.social/embed.js"
            async="async"></script>', 'width': 400, 'height': None}

    Attributes:
        author_name (str): author_name field
        author_url (str): author_url field
        cache_age (int): cache_age field
        html (str): html field
        provider_name (str): provider_name field
        provider_url (str): provider_url field
        title (str): title field
        type_ (str): type field
        version (str): version field
        width (int): width field
        height (Union[None, Unset, str]): height field
    """

    author_name: str
    author_url: str
    cache_age: int
    html: str
    provider_name: str
    provider_url: str
    title: str
    type_: str
    version: str
    width: int
    height: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        author_name = self.author_name

        author_url = self.author_url

        cache_age = self.cache_age

        html = self.html

        provider_name = self.provider_name

        provider_url = self.provider_url

        title = self.title

        type_ = self.type_

        version = self.version

        width = self.width

        height: Union[None, Unset, str]
        if isinstance(self.height, Unset):
            height = UNSET
        else:
            height = self.height

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "author_name": author_name,
                "author_url": author_url,
                "cache_age": cache_age,
                "html": html,
                "provider_name": provider_name,
                "provider_url": provider_url,
                "title": title,
                "type": type_,
                "version": version,
                "width": width,
            }
        )
        if height is not UNSET:
            field_dict["height"] = height

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        author_name = d.pop("author_name")

        author_url = d.pop("author_url")

        cache_age = d.pop("cache_age")

        html = d.pop("html")

        provider_name = d.pop("provider_name")

        provider_url = d.pop("provider_url")

        title = d.pop("title")

        type_ = d.pop("type")

        version = d.pop("version")

        width = d.pop("width")

        def _parse_height(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        height = _parse_height(d.pop("height", UNSET))

        o_embed_response = cls(
            author_name=author_name,
            author_url=author_url,
            cache_age=cache_age,
            html=html,
            provider_name=provider_name,
            provider_url=provider_url,
            title=title,
            type_=type_,
            version=version,
            width=width,
            height=height,
        )

        o_embed_response.additional_properties = d
        return o_embed_response

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
