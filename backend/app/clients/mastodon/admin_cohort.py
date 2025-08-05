import datetime
from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    TypeVar,
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.admin_cohort_frequency import AdminCohortFrequency

if TYPE_CHECKING:
    from ..models.cohort_data import CohortData


T = TypeVar("T", bound="AdminCohort")


@_attrs_define
class AdminCohort:
    """Represents a retention metric.

    Attributes:
        data (list['CohortData']): Retention data for users who registered during the given period.
        frequency (AdminCohortFrequency): The size of the bucket for the returned data.
        period (datetime.datetime): The timestamp for the start of the period, at midnight.
    """

    data: list["CohortData"]
    frequency: AdminCohortFrequency
    period: datetime.datetime
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        data = []
        for data_item_data in self.data:
            data_item = data_item_data.to_dict()
            data.append(data_item)

        frequency = self.frequency.value

        period = self.period.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "data": data,
                "frequency": frequency,
                "period": period,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.cohort_data import CohortData

        d = dict(src_dict)
        data = []
        _data = d.pop("data")
        for data_item_data in _data:
            data_item = CohortData.from_dict(data_item_data)

            data.append(data_item)

        frequency = AdminCohortFrequency(d.pop("frequency"))

        period = isoparse(d.pop("period"))

        admin_cohort = cls(
            data=data,
            frequency=frequency,
            period=period,
        )

        admin_cohort.additional_properties = d
        return admin_cohort

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
