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

from ..models.admin_domain_block_severity import AdminDomainBlockSeverity
from ..types import UNSET, Unset

T = TypeVar("T", bound="AdminDomainBlock")


@_attrs_define
class AdminDomainBlock:
    """Represents a domain limited from federating.

    Example:
        {'id': '1', 'domain': 'example.com', 'digest':
            'a379a6f6eeafb9a55e378c118034e2751e682fab9f2d30ab13d2125586ce1947', 'created_at': '2022-11-16T08:15:34.238Z',
            'severity': 'noop', 'reject_media': False, 'reject_reports': False, 'private_comment': None, 'public_comment':
            None, 'obfuscate': False}

    Attributes:
        created_at (datetime.datetime): When the domain was blocked from federating.
        digest (str): The sha256 hex digest of the domain that is not allowed to federated.
        domain (str): The domain that is not allowed to federate.
        id (str): The ID of the DomainBlock in the database.
        obfuscate (bool): Whether to obfuscate public displays of this domain block
        reject_media (bool): Whether to reject media attachments from this domain
        reject_reports (bool): Whether to reject reports from this domain
        severity (AdminDomainBlockSeverity): The policy to be applied by this domain block.
        private_comment (Union[None, Unset, str]):
        public_comment (Union[None, Unset, str]):
    """

    created_at: datetime.datetime
    digest: str
    domain: str
    id: str
    obfuscate: bool
    reject_media: bool
    reject_reports: bool
    severity: AdminDomainBlockSeverity
    private_comment: Union[None, Unset, str] = UNSET
    public_comment: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        created_at = self.created_at.isoformat()

        digest = self.digest

        domain = self.domain

        id = self.id

        obfuscate = self.obfuscate

        reject_media = self.reject_media

        reject_reports = self.reject_reports

        severity = self.severity.value

        private_comment: Union[None, Unset, str]
        if isinstance(self.private_comment, Unset):
            private_comment = UNSET
        else:
            private_comment = self.private_comment

        public_comment: Union[None, Unset, str]
        if isinstance(self.public_comment, Unset):
            public_comment = UNSET
        else:
            public_comment = self.public_comment

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "created_at": created_at,
                "digest": digest,
                "domain": domain,
                "id": id,
                "obfuscate": obfuscate,
                "reject_media": reject_media,
                "reject_reports": reject_reports,
                "severity": severity,
            }
        )
        if private_comment is not UNSET:
            field_dict["private_comment"] = private_comment
        if public_comment is not UNSET:
            field_dict["public_comment"] = public_comment

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        created_at = isoparse(d.pop("created_at"))

        digest = d.pop("digest")

        domain = d.pop("domain")

        id = d.pop("id")

        obfuscate = d.pop("obfuscate")

        reject_media = d.pop("reject_media")

        reject_reports = d.pop("reject_reports")

        severity = AdminDomainBlockSeverity(d.pop("severity"))

        def _parse_private_comment(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        private_comment = _parse_private_comment(d.pop("private_comment", UNSET))

        def _parse_public_comment(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        public_comment = _parse_public_comment(d.pop("public_comment", UNSET))

        admin_domain_block = cls(
            created_at=created_at,
            digest=digest,
            domain=domain,
            id=id,
            obfuscate=obfuscate,
            reject_media=reject_media,
            reject_reports=reject_reports,
            severity=severity,
            private_comment=private_comment,
            public_comment=public_comment,
        )

        admin_domain_block.additional_properties = d
        return admin_domain_block

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
