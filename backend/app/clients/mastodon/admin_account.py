import datetime
from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    TypeVar,
    Union,
    cast,
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.account import Account
    from ..models.admin_ip import AdminIp
    from ..models.role import Role


T = TypeVar("T", bound="AdminAccount")


@_attrs_define
class AdminAccount:
    """Admin-level information about a given account.

    Attributes:
        account (Account): Represents a user of Mastodon and their associated profile.
        approved (bool): Whether the account is currently approved.
        confirmed (bool): Whether the account has confirmed their email address.
        created_at (datetime.datetime): When the account was first discovered.
        disabled (bool): Whether the account is currently disabled.
        email (str): The email address associated with the account.
        id (str): The ID of the account in the database.
        ips (list['AdminIp']): All known IP addresses associated with this account.
        locale (str): The locale of the account.
        role (Role): Represents a custom user role that grants permissions.
        silenced (bool): Whether the account is currently silenced.
        suspended (bool): Whether the account is currently suspended.
        username (str): The username of the account.
        created_by_application_id (Union[None, Unset, str]): The ID of the [Application]({{< relref
            "entities/application" >}}) that created this account, if applicable.
        domain (Union[None, Unset, str]): The domain of the account, if it is remote.
        invite_request (Union[None, Unset, str]): The reason given when requesting an invite (for instances that require
            manual approval of registrations)
        invited_by_account_id (Union[None, Unset, str]): The ID of the [Account]({{< relref "entities/account" >}}) that
            invited this user, if applicable.
        ip (Union[None, Unset, str]): The IP address last used to login to this account.
    """

    account: "Account"
    approved: bool
    confirmed: bool
    created_at: datetime.datetime
    disabled: bool
    email: str
    id: str
    ips: list["AdminIp"]
    locale: str
    role: "Role"
    silenced: bool
    suspended: bool
    username: str
    created_by_application_id: Union[None, Unset, str] = UNSET
    domain: Union[None, Unset, str] = UNSET
    invite_request: Union[None, Unset, str] = UNSET
    invited_by_account_id: Union[None, Unset, str] = UNSET
    ip: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        account = self.account.to_dict()

        approved = self.approved

        confirmed = self.confirmed

        created_at = self.created_at.isoformat()

        disabled = self.disabled

        email = self.email

        id = self.id

        ips = []
        for ips_item_data in self.ips:
            ips_item = ips_item_data.to_dict()
            ips.append(ips_item)

        locale = self.locale

        role = self.role.to_dict()

        silenced = self.silenced

        suspended = self.suspended

        username = self.username

        created_by_application_id: Union[None, Unset, str]
        if isinstance(self.created_by_application_id, Unset):
            created_by_application_id = UNSET
        else:
            created_by_application_id = self.created_by_application_id

        domain: Union[None, Unset, str]
        if isinstance(self.domain, Unset):
            domain = UNSET
        else:
            domain = self.domain

        invite_request: Union[None, Unset, str]
        if isinstance(self.invite_request, Unset):
            invite_request = UNSET
        else:
            invite_request = self.invite_request

        invited_by_account_id: Union[None, Unset, str]
        if isinstance(self.invited_by_account_id, Unset):
            invited_by_account_id = UNSET
        else:
            invited_by_account_id = self.invited_by_account_id

        ip: Union[None, Unset, str]
        if isinstance(self.ip, Unset):
            ip = UNSET
        else:
            ip = self.ip

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "account": account,
                "approved": approved,
                "confirmed": confirmed,
                "created_at": created_at,
                "disabled": disabled,
                "email": email,
                "id": id,
                "ips": ips,
                "locale": locale,
                "role": role,
                "silenced": silenced,
                "suspended": suspended,
                "username": username,
            }
        )
        if created_by_application_id is not UNSET:
            field_dict["created_by_application_id"] = created_by_application_id
        if domain is not UNSET:
            field_dict["domain"] = domain
        if invite_request is not UNSET:
            field_dict["invite_request"] = invite_request
        if invited_by_account_id is not UNSET:
            field_dict["invited_by_account_id"] = invited_by_account_id
        if ip is not UNSET:
            field_dict["ip"] = ip

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.account import Account
        from ..models.admin_ip import AdminIp
        from ..models.role import Role

        d = dict(src_dict)
        account = Account.from_dict(d.pop("account"))

        approved = d.pop("approved")

        confirmed = d.pop("confirmed")

        created_at = isoparse(d.pop("created_at"))

        disabled = d.pop("disabled")

        email = d.pop("email")

        id = d.pop("id")

        ips = []
        _ips = d.pop("ips")
        for ips_item_data in _ips:
            ips_item = AdminIp.from_dict(ips_item_data)

            ips.append(ips_item)

        locale = d.pop("locale")

        role = Role.from_dict(d.pop("role"))

        silenced = d.pop("silenced")

        suspended = d.pop("suspended")

        username = d.pop("username")

        def _parse_created_by_application_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        created_by_application_id = _parse_created_by_application_id(
            d.pop("created_by_application_id", UNSET)
        )

        def _parse_domain(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        domain = _parse_domain(d.pop("domain", UNSET))

        def _parse_invite_request(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        invite_request = _parse_invite_request(d.pop("invite_request", UNSET))

        def _parse_invited_by_account_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        invited_by_account_id = _parse_invited_by_account_id(
            d.pop("invited_by_account_id", UNSET)
        )

        def _parse_ip(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        ip = _parse_ip(d.pop("ip", UNSET))

        admin_account = cls(
            account=account,
            approved=approved,
            confirmed=confirmed,
            created_at=created_at,
            disabled=disabled,
            email=email,
            id=id,
            ips=ips,
            locale=locale,
            role=role,
            silenced=silenced,
            suspended=suspended,
            username=username,
            created_by_application_id=created_by_application_id,
            domain=domain,
            invite_request=invite_request,
            invited_by_account_id=invited_by_account_id,
            ip=ip,
        )

        admin_account.additional_properties = d
        return admin_account

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
