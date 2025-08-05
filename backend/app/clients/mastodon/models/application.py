from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
    Union,
    cast,
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.o_auth_scope import OAuthScope
from ..types import UNSET, Unset

T = TypeVar("T", bound="Application")


@_attrs_define
class Application:
    r"""Represents an application that interfaces with the REST API, for example to access account information or post
    statuses.

        Example:
            {'id': '12348', 'name': 'Test Application', 'website': 'https://app.example', 'scopes': ['read', 'write',
                'push'], 'redirect_uri': 'https://app.example/callback\nhttps://app.example/register', 'redirect_uris':
                ['https://app.example/callback', 'https://app.example/register']}

        Attributes:
            id (str): The numeric ID of the application.
            name (str): The name of the application.
            redirect_uri (str): The registered redirection URI(s) for the application.
            redirect_uris (list[str]): The registered redirection URI(s) for the application.
            scopes (list[OAuthScope]): Array of OAuth scopes
            vapid_key (str): Used for Push Streaming API. Returned with [POST /api/v1/apps]({{< relref "methods/apps#create"
                >}}). Equivalent to [WebPushSubscription#server_key]({{< relref "entities/WebPushSubscription#server_key" >}})
                and [Instance#vapid_public_key]({{< relref "entities/Instance#vapid_public_key" >}})
            website (Union[None, Unset, str]): The website associated with the application.
    """

    id: str
    name: str
    redirect_uri: str
    redirect_uris: list[str]
    scopes: list[OAuthScope]
    vapid_key: str
    website: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        name = self.name

        redirect_uri = self.redirect_uri

        redirect_uris = self.redirect_uris

        scopes = []
        for componentsschemas_o_auth_scopes_item_data in self.scopes:
            componentsschemas_o_auth_scopes_item = (
                componentsschemas_o_auth_scopes_item_data.value
            )
            scopes.append(componentsschemas_o_auth_scopes_item)

        vapid_key = self.vapid_key

        website: Union[None, Unset, str]
        if isinstance(self.website, Unset):
            website = UNSET
        else:
            website = self.website

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "name": name,
                "redirect_uri": redirect_uri,
                "redirect_uris": redirect_uris,
                "scopes": scopes,
                "vapid_key": vapid_key,
            }
        )
        if website is not UNSET:
            field_dict["website"] = website

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        name = d.pop("name")

        redirect_uri = d.pop("redirect_uri")

        redirect_uris = cast(list[str], d.pop("redirect_uris"))

        scopes = []
        _scopes = d.pop("scopes")
        for componentsschemas_o_auth_scopes_item_data in _scopes:
            componentsschemas_o_auth_scopes_item = OAuthScope(
                componentsschemas_o_auth_scopes_item_data
            )

            scopes.append(componentsschemas_o_auth_scopes_item)

        vapid_key = d.pop("vapid_key")

        def _parse_website(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        website = _parse_website(d.pop("website", UNSET))

        application = cls(
            id=id,
            name=name,
            redirect_uri=redirect_uri,
            redirect_uris=redirect_uris,
            scopes=scopes,
            vapid_key=vapid_key,
            website=website,
        )

        application.additional_properties = d
        return application

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
