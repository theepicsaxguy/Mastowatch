from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="PostOauthTokenBody")


@_attrs_define
class PostOauthTokenBody:
    """
    Attributes:
        client_id (str): The client ID, obtained during app registration.
        client_secret (str): The client secret, obtained during app registration.
        code (str): A user authorization code, obtained from the redirect after an [Authorization request] is approved.
            May alternatively be displayed to the user if `urn:ietf:wg:oauth:2.0:oob` is used as the `redirect_uri`.
        grant_type (str): Set equal to `authorization_code` if `code` is provided in order to gain user-level access.
            Otherwise, set equal to `client_credentials` to obtain app-level access only.
        redirect_uri (str): Must match the `redirect_uri` used during the [Authorization request].
        code_verifier (Union[Unset, str]): Required if [PKCE] is used during the authorization request. This is the code
            verifier which was used to create the `code_challenge` using the `code_challenge_method` for the authorization
            request.
        scope (Union[Unset, str]): When `grant_type` is set to `client_credentials`, the list of requested OAuth scopes,
            separated by spaces (or pluses, if using query parameters). Must be a subset of the scopes requested at the time
            the application was created. If omitted, it defaults to `read`. Has no effect when `grant_type` is
            `authorization_code`. Default: 'read'.

    """

    client_id: str
    client_secret: str
    code: str
    grant_type: str
    redirect_uri: str
    code_verifier: Unset | str = UNSET
    scope: Unset | str = "read"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        client_id = self.client_id

        client_secret = self.client_secret

        code = self.code

        grant_type = self.grant_type

        redirect_uri = self.redirect_uri

        code_verifier = self.code_verifier

        scope = self.scope

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "client_id": client_id,
                "client_secret": client_secret,
                "code": code,
                "grant_type": grant_type,
                "redirect_uri": redirect_uri,
            }
        )
        if code_verifier is not UNSET:
            field_dict["code_verifier"] = code_verifier
        if scope is not UNSET:
            field_dict["scope"] = scope

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        client_id = d.pop("client_id")

        client_secret = d.pop("client_secret")

        code = d.pop("code")

        grant_type = d.pop("grant_type")

        redirect_uri = d.pop("redirect_uri")

        code_verifier = d.pop("code_verifier", UNSET)

        scope = d.pop("scope", UNSET)

        post_oauth_token_body = cls(
            client_id=client_id,
            client_secret=client_secret,
            code=code,
            grant_type=grant_type,
            redirect_uri=redirect_uri,
            code_verifier=code_verifier,
            scope=scope,
        )

        post_oauth_token_body.additional_properties = d
        return post_oauth_token_body

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
