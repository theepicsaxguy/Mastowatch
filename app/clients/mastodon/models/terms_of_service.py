import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="TermsOfService")


@_attrs_define
class TermsOfService:
    r"""Represents the terms of service of the instance.

    Example:
        {'effective_date': '2025-04-15', 'effective': True, 'content': '<p>Foo bar newer</p>\n', 'succeeded_by': None}

    Attributes:
        content (str): The rendered HTML content of the terms of service.
        effective (bool): Whether these terms of service are currently in effect.
        effective_date (datetime.date): The date these terms of service are coming or have come in effect.
        succeeded_by (Union[None, Unset, datetime.date]): If there are newer terms of service, their effective date.

    """

    content: str
    effective: bool
    effective_date: datetime.date
    succeeded_by: None | Unset | datetime.date = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        content = self.content

        effective = self.effective

        effective_date = self.effective_date.isoformat()

        succeeded_by: None | Unset | str
        if isinstance(self.succeeded_by, Unset):
            succeeded_by = UNSET
        elif isinstance(self.succeeded_by, datetime.date):
            succeeded_by = self.succeeded_by.isoformat()
        else:
            succeeded_by = self.succeeded_by

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "content": content,
                "effective": effective,
                "effective_date": effective_date,
            }
        )
        if succeeded_by is not UNSET:
            field_dict["succeeded_by"] = succeeded_by

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        content = d.pop("content")

        effective = d.pop("effective")

        effective_date = isoparse(d.pop("effective_date")).date()

        def _parse_succeeded_by(data: object) -> None | Unset | datetime.date:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                succeeded_by_type_0 = isoparse(data).date()

                return succeeded_by_type_0
            except:  # noqa: E722
                pass
            return cast(None | Unset | datetime.date, data)

        succeeded_by = _parse_succeeded_by(d.pop("succeeded_by", UNSET))

        terms_of_service = cls(
            content=content,
            effective=effective,
            effective_date=effective_date,
            succeeded_by=succeeded_by,
        )

        terms_of_service.additional_properties = d
        return terms_of_service

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
