from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.media_attachment_meta_focus_type_0 import (
        MediaAttachmentMetaFocusType0,
    )


T = TypeVar("T", bound="MediaAttachmentMeta")


@_attrs_define
class MediaAttachmentMeta:
    """Metadata returned by Paperclip.

    Attributes:
        focus (Union['MediaAttachmentMetaFocusType0', None, Unset]): Coordinates that may be used for smart thumbnail
            cropping -- see [Focal points for cropped media thumbnails]({{< relref "api/guidelines#focal-points" >}}) for
            more.
    """

    focus: Union["MediaAttachmentMetaFocusType0", None, Unset] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.media_attachment_meta_focus_type_0 import (
            MediaAttachmentMetaFocusType0,
        )

        focus: Union[None, Unset, dict[str, Any]]
        if isinstance(self.focus, Unset):
            focus = UNSET
        elif isinstance(self.focus, MediaAttachmentMetaFocusType0):
            focus = self.focus.to_dict()
        else:
            focus = self.focus

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if focus is not UNSET:
            field_dict["focus"] = focus

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.media_attachment_meta_focus_type_0 import (
            MediaAttachmentMetaFocusType0,
        )

        d = src_dict.copy()

        def _parse_focus(
            data: object,
        ) -> Union["MediaAttachmentMetaFocusType0", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                focus_type_0 = MediaAttachmentMetaFocusType0.from_dict(data)

                return focus_type_0
            except:  # noqa: E722
                pass
            return cast(Union["MediaAttachmentMetaFocusType0", None, Unset], data)

        focus = _parse_focus(d.pop("focus", UNSET))

        media_attachment_meta = cls(
            focus=focus,
        )

        media_attachment_meta.additional_properties = d
        return media_attachment_meta

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
