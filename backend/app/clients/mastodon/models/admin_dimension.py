from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    TypeVar,
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.admin_dimension_data import AdminDimensionData


T = TypeVar("T", bound="AdminDimension")


@_attrs_define
class AdminDimension:
    """Represents qualitative data about the server.

    Attributes:
        data (list['AdminDimensionData']): The data available for the requested dimension.
        key (str): The unique keystring for the requested dimension.
    """

    data: list["AdminDimensionData"]
    key: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        data = []
        for data_item_data in self.data:
            data_item = data_item_data.to_dict()
            data.append(data_item)

        key = self.key

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "data": data,
                "key": key,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.admin_dimension_data import AdminDimensionData

        d = dict(src_dict)
        data = []
        _data = d.pop("data")
        for data_item_data in _data:
            data_item = AdminDimensionData.from_dict(data_item_data)

            data.append(data_item)

        key = d.pop("key")

        admin_dimension = cls(
            data=data,
            key=key,
        )

        admin_dimension.additional_properties = d
        return admin_dimension

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
