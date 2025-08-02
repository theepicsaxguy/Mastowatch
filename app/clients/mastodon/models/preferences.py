from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.preferences_readingexpandmedia import PreferencesReadingexpandmedia
from ..models.visibility_enum import VisibilityEnum
from ..types import UNSET, Unset

T = TypeVar("T", bound="Preferences")


@_attrs_define
class Preferences:
    """Represents a user's preferences.

    Example:
        {'posting:default:visibility': 'public', 'posting:default:sensitive': False, 'posting:default:language': None,
            'reading:expand:media': 'default', 'reading:expand:spoilers': False}

    Attributes:
        postingdefaultsensitive (bool): Default sensitivity flag for new posts. Equivalent to [CredentialAccount#source
        postingdefaultvisibility (VisibilityEnum):
        readingexpandmedia (PreferencesReadingexpandmedia): Whether media attachments should be automatically displayed
            or blurred/hidden.
        readingexpandspoilers (bool): Whether CWs should be expanded by default.
        postingdefaultlanguage (Union[None, Unset, str]): Default language for new posts. Equivalent to
            [CredentialAccount#source
    """

    postingdefaultsensitive: bool
    postingdefaultvisibility: VisibilityEnum
    readingexpandmedia: PreferencesReadingexpandmedia
    readingexpandspoilers: bool
    postingdefaultlanguage: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        postingdefaultsensitive = self.postingdefaultsensitive

        postingdefaultvisibility = self.postingdefaultvisibility.value

        readingexpandmedia = self.readingexpandmedia.value

        readingexpandspoilers = self.readingexpandspoilers

        postingdefaultlanguage: Union[None, Unset, str]
        if isinstance(self.postingdefaultlanguage, Unset):
            postingdefaultlanguage = UNSET
        else:
            postingdefaultlanguage = self.postingdefaultlanguage

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "posting:default:sensitive": postingdefaultsensitive,
                "posting:default:visibility": postingdefaultvisibility,
                "reading:expand:media": readingexpandmedia,
                "reading:expand:spoilers": readingexpandspoilers,
            }
        )
        if postingdefaultlanguage is not UNSET:
            field_dict["posting:default:language"] = postingdefaultlanguage

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        postingdefaultsensitive = d.pop("posting:default:sensitive")

        postingdefaultvisibility = VisibilityEnum(d.pop("posting:default:visibility"))

        readingexpandmedia = PreferencesReadingexpandmedia(
            d.pop("reading:expand:media")
        )

        readingexpandspoilers = d.pop("reading:expand:spoilers")

        def _parse_postingdefaultlanguage(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        postingdefaultlanguage = _parse_postingdefaultlanguage(
            d.pop("posting:default:language", UNSET)
        )

        preferences = cls(
            postingdefaultsensitive=postingdefaultsensitive,
            postingdefaultvisibility=postingdefaultvisibility,
            readingexpandmedia=readingexpandmedia,
            readingexpandspoilers=readingexpandspoilers,
            postingdefaultlanguage=postingdefaultlanguage,
        )

        preferences.additional_properties = d
        return preferences

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
