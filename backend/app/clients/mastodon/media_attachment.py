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

from ..models.media_attachment_type import MediaAttachmentType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.media_attachment_meta import MediaAttachmentMeta


T = TypeVar("T", bound="MediaAttachment")


@_attrs_define
class MediaAttachment:
    """Represents a file or media attachment that can be added to a status.

    Attributes:
        id (str): The ID of the attachment in the database.
        meta (MediaAttachmentMeta): Metadata returned by Paperclip.
        type_ (MediaAttachmentType): The type of the attachment.
        url (str): The location of the original full-size attachment.
        blurhash (Union[None, Unset, str]): A hash computed by [the BlurHash
            algorithm](https://github.com/woltapp/blurhash), for generating colorful preview thumbnails when media has not
            been downloaded yet.
        description (Union[None, Unset, str]): Alternate text that describes what is in the media attachment, to be used
            for the visually impaired or when media attachments do not load.
        preview_url (Union[None, Unset, str]): The location of a scaled-down preview of the attachment.
        remote_url (Union[None, Unset, str]): The location of the full-size original attachment on the remote website.
    """

    id: str
    meta: "MediaAttachmentMeta"
    type_: MediaAttachmentType
    url: str
    blurhash: Union[None, Unset, str] = UNSET
    description: Union[None, Unset, str] = UNSET
    preview_url: Union[None, Unset, str] = UNSET
    remote_url: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        meta = self.meta.to_dict()

        type_ = self.type_.value

        url = self.url

        blurhash: Union[None, Unset, str]
        if isinstance(self.blurhash, Unset):
            blurhash = UNSET
        else:
            blurhash = self.blurhash

        description: Union[None, Unset, str]
        if isinstance(self.description, Unset):
            description = UNSET
        else:
            description = self.description

        preview_url: Union[None, Unset, str]
        if isinstance(self.preview_url, Unset):
            preview_url = UNSET
        else:
            preview_url = self.preview_url

        remote_url: Union[None, Unset, str]
        if isinstance(self.remote_url, Unset):
            remote_url = UNSET
        else:
            remote_url = self.remote_url

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "meta": meta,
                "type": type_,
                "url": url,
            }
        )
        if blurhash is not UNSET:
            field_dict["blurhash"] = blurhash
        if description is not UNSET:
            field_dict["description"] = description
        if preview_url is not UNSET:
            field_dict["preview_url"] = preview_url
        if remote_url is not UNSET:
            field_dict["remote_url"] = remote_url

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.media_attachment_meta import MediaAttachmentMeta

        d = dict(src_dict)
        id = d.pop("id")

        meta = MediaAttachmentMeta.from_dict(d.pop("meta"))

        type_ = MediaAttachmentType(d.pop("type"))

        url = d.pop("url")

        def _parse_blurhash(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        blurhash = _parse_blurhash(d.pop("blurhash", UNSET))

        def _parse_description(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        description = _parse_description(d.pop("description", UNSET))

        def _parse_preview_url(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        preview_url = _parse_preview_url(d.pop("preview_url", UNSET))

        def _parse_remote_url(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        remote_url = _parse_remote_url(d.pop("remote_url", UNSET))

        media_attachment = cls(
            id=id,
            meta=meta,
            type_=type_,
            url=url,
            blurhash=blurhash,
            description=description,
            preview_url=preview_url,
            remote_url=remote_url,
        )

        media_attachment.additional_properties = d
        return media_attachment

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
