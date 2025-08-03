from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.admin_measure_data import AdminMeasureData


T = TypeVar("T", bound="AdminMeasure")


@_attrs_define
class AdminMeasure:
    """Represents quantitative data about the server.

    Attributes:
        data (list['AdminMeasureData']): The data available for the requested measure, split into daily buckets.
        key (str): The unique keystring for the requested measure.
        total (str): The numeric total associated with the requested measure.
        human_value (Union[None, Unset, str]): A human-readable formatted value for this data item.
        previous_total (Union[None, Unset, str]): The numeric total associated with the requested measure, in the
            previous period. Previous period is calculated by subtracting the start_at and end_at dates, then offsetting
            both start and end dates backwards by the length of the time period.
        unit (Union[None, Unset, str]): The units associated with this data item's value, if applicable.

    """

    data: list["AdminMeasureData"]
    key: str
    total: str
    human_value: None | Unset | str = UNSET
    previous_total: None | Unset | str = UNSET
    unit: None | Unset | str = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        data = []
        for data_item_data in self.data:
            data_item = data_item_data.to_dict()
            data.append(data_item)

        key = self.key

        total = self.total

        human_value: None | Unset | str
        if isinstance(self.human_value, Unset):
            human_value = UNSET
        else:
            human_value = self.human_value

        previous_total: None | Unset | str
        if isinstance(self.previous_total, Unset):
            previous_total = UNSET
        else:
            previous_total = self.previous_total

        unit: None | Unset | str
        if isinstance(self.unit, Unset):
            unit = UNSET
        else:
            unit = self.unit

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "data": data,
                "key": key,
                "total": total,
            }
        )
        if human_value is not UNSET:
            field_dict["human_value"] = human_value
        if previous_total is not UNSET:
            field_dict["previous_total"] = previous_total
        if unit is not UNSET:
            field_dict["unit"] = unit

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.admin_measure_data import AdminMeasureData

        d = dict(src_dict)
        data = []
        _data = d.pop("data")
        for data_item_data in _data:
            data_item = AdminMeasureData.from_dict(data_item_data)

            data.append(data_item)

        key = d.pop("key")

        total = d.pop("total")

        def _parse_human_value(data: object) -> None | Unset | str:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | Unset | str, data)

        human_value = _parse_human_value(d.pop("human_value", UNSET))

        def _parse_previous_total(data: object) -> None | Unset | str:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | Unset | str, data)

        previous_total = _parse_previous_total(d.pop("previous_total", UNSET))

        def _parse_unit(data: object) -> None | Unset | str:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | Unset | str, data)

        unit = _parse_unit(d.pop("unit", UNSET))

        admin_measure = cls(
            data=data,
            key=key,
            total=total,
            human_value=human_value,
            previous_total=previous_total,
            unit=unit,
        )

        admin_measure.additional_properties = d
        return admin_measure

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
