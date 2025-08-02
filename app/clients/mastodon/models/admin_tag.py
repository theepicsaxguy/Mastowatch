from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="AdminTag")


@_attrs_define
class AdminTag:
    """Additional entity definition for Admin::Tag

    Attributes:
        requires_review (bool): Whether the hashtag has not been reviewed yet to approve or deny its trending.
        trendable (bool): Whether the hashtag has been approved to trend.
        usable (bool): Whether the hashtag has not been disabled from auto-linking.
    """

    requires_review: bool
    trendable: bool
    usable: bool
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        requires_review = self.requires_review

        trendable = self.trendable

        usable = self.usable

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "requires_review": requires_review,
                "trendable": trendable,
                "usable": usable,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        requires_review = d.pop("requires_review")

        trendable = d.pop("trendable")

        usable = d.pop("usable")

        admin_tag = cls(
            requires_review=requires_review,
            trendable=trendable,
            usable=usable,
        )

        admin_tag.additional_properties = d
        return admin_tag

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
