from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    TypeVar,
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.status import Status


T = TypeVar("T", bound="Context")


@_attrs_define
class Context:
    """Represents the tree around a given status. Used for reconstructing threads of statuses.

    Attributes:
        ancestors (list['Status']): Parents in the thread.
        descendants (list['Status']): Children in the thread.
    """

    ancestors: list["Status"]
    descendants: list["Status"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        ancestors = []
        for ancestors_item_data in self.ancestors:
            ancestors_item = ancestors_item_data.to_dict()
            ancestors.append(ancestors_item)

        descendants = []
        for descendants_item_data in self.descendants:
            descendants_item = descendants_item_data.to_dict()
            descendants.append(descendants_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "ancestors": ancestors,
                "descendants": descendants,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.status import Status

        d = dict(src_dict)
        ancestors = []
        _ancestors = d.pop("ancestors")
        for ancestors_item_data in _ancestors:
            ancestors_item = Status.from_dict(ancestors_item_data)

            ancestors.append(ancestors_item)

        descendants = []
        _descendants = d.pop("descendants")
        for descendants_item_data in _descendants:
            descendants_item = Status.from_dict(descendants_item_data)

            descendants.append(descendants_item)

        context = cls(
            ancestors=ancestors,
            descendants=descendants,
        )

        context.additional_properties = d
        return context

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
