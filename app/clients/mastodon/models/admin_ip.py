import datetime
from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

T = TypeVar("T", bound="AdminIp")


@_attrs_define
class AdminIp:
    """Represents an IP address associated with a user.

    Example:
        {'ip': '192.168.42.1', 'used_at': '2022-09-15T01:38:58.851Z'}

    Attributes:
        ip (str): The IP address.
        used_at (datetime.datetime): The timestamp of when the IP address was last used for this account.

    """

    ip: str
    used_at: datetime.datetime
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        ip = self.ip

        used_at = self.used_at.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "ip": ip,
                "used_at": used_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        ip = d.pop("ip")

        used_at = isoparse(d.pop("used_at"))

        admin_ip = cls(
            ip=ip,
            used_at=used_at,
        )

        admin_ip.additional_properties = d
        return admin_ip

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
