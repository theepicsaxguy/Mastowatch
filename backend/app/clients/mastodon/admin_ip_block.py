import datetime
from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
    Union,
    cast,
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.admin_ip_block_severity import AdminIpBlockSeverity
from ..types import UNSET, Unset

T = TypeVar("T", bound="AdminIpBlock")


@_attrs_define
class AdminIpBlock:
    """Represents an IP address range that cannot be used to sign up.

    Attributes:
        comment (str): The recorded reason for this IP block.
        created_at (datetime.datetime): When the IP block was created.
        id (str): The ID of the DomainBlock in the database.
        ip (str): The IP address range that is not allowed to federate.
        severity (AdminIpBlockSeverity): The associated policy with this IP block.
        expires_at (Union[None, Unset, datetime.datetime]): When the IP block will expire.
    """

    comment: str
    created_at: datetime.datetime
    id: str
    ip: str
    severity: AdminIpBlockSeverity
    expires_at: Union[None, Unset, datetime.datetime] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        comment = self.comment

        created_at = self.created_at.isoformat()

        id = self.id

        ip = self.ip

        severity = self.severity.value

        expires_at: Union[None, Unset, str]
        if isinstance(self.expires_at, Unset):
            expires_at = UNSET
        elif isinstance(self.expires_at, datetime.datetime):
            expires_at = self.expires_at.isoformat()
        else:
            expires_at = self.expires_at

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "comment": comment,
                "created_at": created_at,
                "id": id,
                "ip": ip,
                "severity": severity,
            }
        )
        if expires_at is not UNSET:
            field_dict["expires_at"] = expires_at

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        comment = d.pop("comment")

        created_at = isoparse(d.pop("created_at"))

        id = d.pop("id")

        ip = d.pop("ip")

        severity = AdminIpBlockSeverity(d.pop("severity"))

        def _parse_expires_at(data: object) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                expires_at_type_0 = isoparse(data)

                return expires_at_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

        expires_at = _parse_expires_at(d.pop("expires_at", UNSET))

        admin_ip_block = cls(
            comment=comment,
            created_at=created_at,
            id=id,
            ip=ip,
            severity=severity,
            expires_at=expires_at,
        )

        admin_ip_block.additional_properties = d
        return admin_ip_block

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
