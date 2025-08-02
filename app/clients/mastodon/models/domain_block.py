from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.domain_block_severity import DomainBlockSeverity
from ..types import UNSET, Unset

T = TypeVar("T", bound="DomainBlock")


@_attrs_define
class DomainBlock:
    """Represents a domain that is blocked by the instance.

    Example:
        {'domain': 'daji******.com', 'digest': '3752f63a7079d60c2de5dceb8bd7608e86a15544eb78a494a482041c3684b37f',
            'severity': 'suspend', 'comment': 'Inappropriate content'}

    Attributes:
        digest (str): The SHA256 hash digest of the domain string.
        domain (str): The domain which is blocked. This may be obfuscated or partially censored.
        severity (DomainBlockSeverity): The level to which the domain is blocked.
        comment (Union[None, Unset, str]): An optional reason for the domain block.
    """

    digest: str
    domain: str
    severity: DomainBlockSeverity
    comment: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        digest = self.digest

        domain = self.domain

        severity = self.severity.value

        comment: Union[None, Unset, str]
        if isinstance(self.comment, Unset):
            comment = UNSET
        else:
            comment = self.comment

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "digest": digest,
                "domain": domain,
                "severity": severity,
            }
        )
        if comment is not UNSET:
            field_dict["comment"] = comment

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        digest = d.pop("digest")

        domain = d.pop("domain")

        severity = DomainBlockSeverity(d.pop("severity"))

        def _parse_comment(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        comment = _parse_comment(d.pop("comment", UNSET))

        domain_block = cls(
            digest=digest,
            domain=domain,
            severity=severity,
            comment=comment,
        )

        domain_block.additional_properties = d
        return domain_block

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
