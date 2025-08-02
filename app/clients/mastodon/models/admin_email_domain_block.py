import datetime
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

if TYPE_CHECKING:
    from ..models.admin_email_domain_block_history import \
        AdminEmailDomainBlockHistory


T = TypeVar("T", bound="AdminEmailDomainBlock")


@_attrs_define
class AdminEmailDomainBlock:
    """Represents an email domain that cannot be used to sign up.

    Example:
        {'id': '1', 'domain': 'foo', 'created_at': '2022-11-16T06:09:36.176Z', 'history': [{'day': '1668556800',
            'accounts': '0', 'uses': '0'}, {'day': '1668470400', 'accounts': '0', 'uses': '0'}, {'day': '1668384000',
            'accounts': '0', 'uses': '0'}, {'day': '1668297600', 'accounts': '0', 'uses': '0'}, {'day': '1668211200',
            'accounts': '0', 'uses': '0'}, {'day': '1668124800', 'accounts': '0', 'uses': '0'}, {'day': '1668038400',
            'accounts': '0', 'uses': '0'}]}

    Attributes:
        created_at (datetime.datetime): When the email domain was disallowed from signups.
        domain (str): The email domain that is not allowed to be used for signups.
        history (list['AdminEmailDomainBlockHistory']): Usage statistics for given days (typically the past week).
        id (str): The ID of the EmailDomainBlock in the database.
    """

    created_at: datetime.datetime
    domain: str
    history: list["AdminEmailDomainBlockHistory"]
    id: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        created_at = self.created_at.isoformat()

        domain = self.domain

        history = []
        for history_item_data in self.history:
            history_item = history_item_data.to_dict()
            history.append(history_item)

        id = self.id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "created_at": created_at,
                "domain": domain,
                "history": history,
                "id": id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.admin_email_domain_block_history import \
            AdminEmailDomainBlockHistory

        d = src_dict.copy()
        created_at = isoparse(d.pop("created_at"))

        domain = d.pop("domain")

        history = []
        _history = d.pop("history")
        for history_item_data in _history:
            history_item = AdminEmailDomainBlockHistory.from_dict(history_item_data)

            history.append(history_item)

        id = d.pop("id")

        admin_email_domain_block = cls(
            created_at=created_at,
            domain=domain,
            history=history,
            id=id,
        )

        admin_email_domain_block.additional_properties = d
        return admin_email_domain_block

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
