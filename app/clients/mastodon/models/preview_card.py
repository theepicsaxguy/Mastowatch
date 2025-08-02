from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.preview_type_enum import PreviewTypeEnum
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.preview_card_author import PreviewCardAuthor


T = TypeVar("T", bound="PreviewCard")


@_attrs_define
class PreviewCard:
    """Represents a rich preview card that is generated using OpenGraph tags from a URL.

    Attributes:
        author_name (str): The author of the original resource. Deprecated since 4.3.0, clients should use `authors`
            instead.
        author_url (str): A link to the author of the original resource. Deprecated since 4.3.0, clients should use
            `authors` instead.
        authors (list['PreviewCardAuthor']): Fediverse account of the authors of the original resource.
        description (str): Description of preview.
        embed_url (str): Used for photo embeds, instead of custom `html`.
        height (int): Height of preview, in pixels.
        html (str): HTML to be used for generating the preview card.
        provider_name (str): The provider of the original resource.
        provider_url (str): A link to the provider of the original resource.
        title (str): Title of linked resource.
        type_ (PreviewTypeEnum):
        url (str): Location of linked resource.
        width (int): Width of preview, in pixels.
        blurhash (Union[None, Unset, str]): A hash computed by [the BlurHash
            algorithm](https://github.com/woltapp/blurhash), for generating colorful preview thumbnails when media has not
            been downloaded yet.
        image (Union[None, Unset, str]): Preview thumbnail.
    """

    author_name: str
    author_url: str
    authors: list["PreviewCardAuthor"]
    description: str
    embed_url: str
    height: int
    html: str
    provider_name: str
    provider_url: str
    title: str
    type_: PreviewTypeEnum
    url: str
    width: int
    blurhash: Union[None, Unset, str] = UNSET
    image: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        author_name = self.author_name

        author_url = self.author_url

        authors = []
        for authors_item_data in self.authors:
            authors_item = authors_item_data.to_dict()
            authors.append(authors_item)

        description = self.description

        embed_url = self.embed_url

        height = self.height

        html = self.html

        provider_name = self.provider_name

        provider_url = self.provider_url

        title = self.title

        type_ = self.type_.value

        url = self.url

        width = self.width

        blurhash: Union[None, Unset, str]
        if isinstance(self.blurhash, Unset):
            blurhash = UNSET
        else:
            blurhash = self.blurhash

        image: Union[None, Unset, str]
        if isinstance(self.image, Unset):
            image = UNSET
        else:
            image = self.image

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "author_name": author_name,
                "author_url": author_url,
                "authors": authors,
                "description": description,
                "embed_url": embed_url,
                "height": height,
                "html": html,
                "provider_name": provider_name,
                "provider_url": provider_url,
                "title": title,
                "type": type_,
                "url": url,
                "width": width,
            }
        )
        if blurhash is not UNSET:
            field_dict["blurhash"] = blurhash
        if image is not UNSET:
            field_dict["image"] = image

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.preview_card_author import PreviewCardAuthor

        d = src_dict.copy()
        author_name = d.pop("author_name")

        author_url = d.pop("author_url")

        authors = []
        _authors = d.pop("authors")
        for authors_item_data in _authors:
            authors_item = PreviewCardAuthor.from_dict(authors_item_data)

            authors.append(authors_item)

        description = d.pop("description")

        embed_url = d.pop("embed_url")

        height = d.pop("height")

        html = d.pop("html")

        provider_name = d.pop("provider_name")

        provider_url = d.pop("provider_url")

        title = d.pop("title")

        type_ = PreviewTypeEnum(d.pop("type"))

        url = d.pop("url")

        width = d.pop("width")

        def _parse_blurhash(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        blurhash = _parse_blurhash(d.pop("blurhash", UNSET))

        def _parse_image(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        image = _parse_image(d.pop("image", UNSET))

        preview_card = cls(
            author_name=author_name,
            author_url=author_url,
            authors=authors,
            description=description,
            embed_url=embed_url,
            height=height,
            html=html,
            provider_name=provider_name,
            provider_url=provider_url,
            title=title,
            type_=type_,
            url=url,
            width=width,
            blurhash=blurhash,
            image=image,
        )

        preview_card.additional_properties = d
        return preview_card

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
