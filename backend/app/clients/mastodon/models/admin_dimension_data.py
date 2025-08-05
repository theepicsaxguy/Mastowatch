from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
    Union,
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="AdminDimensionData")


@_attrs_define
class AdminDimensionData:
    """Nested entity extracted from Admin::Dimension.data

    Attributes:
        human_key (str): A human-readable key for this data item.
        key (str): The unique keystring for this data item.
        value (str): The value for this data item.
        human_value (Union[Unset, str]): A human-readable formatted value for this data item.
        unit (Union[Unset, str]): The units associated with this data item's value, if applicable.
    """

    human_key: str
    key: str
    value: str
    human_value: Union[Unset, str] = UNSET
    unit: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        human_key = self.human_key

        key = self.key

        value = self.value

        human_value = self.human_value

        unit = self.unit

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "human_key": human_key,
                "key": key,
                "value": value,
            }
        )
        if human_value is not UNSET:
            field_dict["human_value"] = human_value
        if unit is not UNSET:
            field_dict["unit"] = unit

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        human_key = d.pop("human_key")

        key = d.pop("key")

        value = d.pop("value")

        human_value = d.pop("human_value", UNSET)

        unit = d.pop("unit", UNSET)

        admin_dimension_data = cls(
            human_key=human_key,
            key=key,
            value=value,
            human_value=human_value,
            unit=unit,
        )

        admin_dimension_data.additional_properties = d
        return admin_dimension_data

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
