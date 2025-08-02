import datetime
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

T = TypeVar("T", bound="CohortData")


@_attrs_define
class CohortData:
    """Additional entity definition for CohortData

    Attributes:
        date (datetime.datetime): The timestamp for the start of the bucket, at midnight.
        rate (float): The percentage rate of users who registered in the specified `period` and were active for the
            given `date` bucket.
        value (str): How many users registered in the specified `period` and were active for the given `date` bucket.
    """

    date: datetime.datetime
    rate: float
    value: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        date = self.date.isoformat()

        rate = self.rate

        value = self.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "date": date,
                "rate": rate,
                "value": value,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        date = isoparse(d.pop("date"))

        rate = d.pop("rate")

        value = d.pop("value")

        cohort_data = cls(
            date=date,
            rate=rate,
            value=value,
        )

        cohort_data.additional_properties = d
        return cohort_data

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
