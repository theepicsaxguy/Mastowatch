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
    from ..models.instance_thumbnail_versions_type_0 import (
        InstanceThumbnailVersionsType0,
    )


T = TypeVar("T", bound="InstanceThumbnail")


@_attrs_define
class InstanceThumbnail:
    """An image used to represent this instance.

    Attributes:
        url (str): The URL for the thumbnail image.
        blurhash (Union[None, Unset, str]): A hash computed by [the BlurHash
            algorithm](https://github.com/woltapp/blurhash), for generating colorful preview thumbnails when media has not
            been downloaded yet.
        versions (Union['InstanceThumbnailVersionsType0', None, Unset]): Links to scaled resolution images, for high DPI
            screens.
    """

    url: str
    blurhash: Union[None, Unset, str] = UNSET
    versions: Union["InstanceThumbnailVersionsType0", None, Unset] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.instance_thumbnail_versions_type_0 import (
            InstanceThumbnailVersionsType0,
        )

        url = self.url

        blurhash: Union[None, Unset, str]
        if isinstance(self.blurhash, Unset):
            blurhash = UNSET
        else:
            blurhash = self.blurhash

        versions: Union[None, Unset, dict[str, Any]]
        if isinstance(self.versions, Unset):
            versions = UNSET
        elif isinstance(self.versions, InstanceThumbnailVersionsType0):
            versions = self.versions.to_dict()
        else:
            versions = self.versions

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "url": url,
            }
        )
        if blurhash is not UNSET:
            field_dict["blurhash"] = blurhash
        if versions is not UNSET:
            field_dict["versions"] = versions

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.instance_thumbnail_versions_type_0 import (
            InstanceThumbnailVersionsType0,
        )

        d = dict(src_dict)
        url = d.pop("url")

        def _parse_blurhash(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        blurhash = _parse_blurhash(d.pop("blurhash", UNSET))

        def _parse_versions(
            data: object,
        ) -> Union["InstanceThumbnailVersionsType0", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                versions_type_0 = InstanceThumbnailVersionsType0.from_dict(data)

                return versions_type_0
            except:  # noqa: E722
                pass
            return cast(Union["InstanceThumbnailVersionsType0", None, Unset], data)

        versions = _parse_versions(d.pop("versions", UNSET))

        instance_thumbnail = cls(
            url=url,
            blurhash=blurhash,
            versions=versions,
        )

        instance_thumbnail.additional_properties = d
        return instance_thumbnail

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
