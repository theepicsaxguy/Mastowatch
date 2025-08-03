from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="CreateAppBody")


@_attrs_define
class CreateAppBody:
    """
    Attributes:
        client_name (str): A name for your application
        redirect_uris (list[str]): Where the user should be redirected after authorization. To display the authorization
            code to the user instead of redirecting to a web page, use `urn:ietf:wg:oauth:2.0:oob` in this parameter.
        scopes (Union[Unset, str]): Space separated list of scopes. If none is provided, defaults to `read`. See [OAuth
            Scopes] for a list of possible scopes. Default: 'read'.
        website (Union[Unset, str]): A URL to the homepage of your app

    """

    client_name: str
    redirect_uris: list[str]
    scopes: Unset | str = "read"
    website: Unset | str = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        client_name = self.client_name

        redirect_uris = self.redirect_uris

        scopes = self.scopes

        website = self.website

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "client_name": client_name,
                "redirect_uris": redirect_uris,
            }
        )
        if scopes is not UNSET:
            field_dict["scopes"] = scopes
        if website is not UNSET:
            field_dict["website"] = website

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        client_name = d.pop("client_name")

        redirect_uris = cast(list[str], d.pop("redirect_uris"))

        scopes = d.pop("scopes", UNSET)

        website = d.pop("website", UNSET)

        create_app_body = cls(
            client_name=client_name,
            redirect_uris=redirect_uris,
            scopes=scopes,
            website=website,
        )

        create_app_body.additional_properties = d
        return create_app_body

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
