import datetime
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="CreateAccountBody")


@_attrs_define
class CreateAccountBody:
    """
    Attributes:
        agreement (bool): Whether the user agrees to the local rules, terms, and policies. These should be presented to
            the user in order to allow them to consent before setting this parameter to TRUE.
        email (str): The email address to be used for login
        locale (str): The language of the confirmation email that will be sent.
        password (str): The password to be used for login
        username (str): The desired username for the account
        date_of_birth (Union[Unset, datetime.date]): String ([Date]), required if the server has a minimum age
            requirement.
        reason (Union[Unset, str]): If registrations require manual approval, this text will be reviewed by moderators.
    """

    agreement: bool
    email: str
    locale: str
    password: str
    username: str
    date_of_birth: Union[Unset, datetime.date] = UNSET
    reason: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        agreement = self.agreement

        email = self.email

        locale = self.locale

        password = self.password

        username = self.username

        date_of_birth: Union[Unset, str] = UNSET
        if not isinstance(self.date_of_birth, Unset):
            date_of_birth = self.date_of_birth.isoformat()

        reason = self.reason

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "agreement": agreement,
                "email": email,
                "locale": locale,
                "password": password,
                "username": username,
            }
        )
        if date_of_birth is not UNSET:
            field_dict["date_of_birth"] = date_of_birth
        if reason is not UNSET:
            field_dict["reason"] = reason

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        agreement = d.pop("agreement")

        email = d.pop("email")

        locale = d.pop("locale")

        password = d.pop("password")

        username = d.pop("username")

        _date_of_birth = d.pop("date_of_birth", UNSET)
        date_of_birth: Union[Unset, datetime.date]
        if isinstance(_date_of_birth, Unset):
            date_of_birth = UNSET
        else:
            date_of_birth = isoparse(_date_of_birth).date()

        reason = d.pop("reason", UNSET)

        create_account_body = cls(
            agreement=agreement,
            email=email,
            locale=locale,
            password=password,
            username=username,
            date_of_birth=date_of_birth,
            reason=reason,
        )

        create_account_body.additional_properties = d
        return create_account_body

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
