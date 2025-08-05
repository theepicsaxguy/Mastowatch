from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
    cast,
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.o_auth_scope import OAuthScope

T = TypeVar("T", bound="DiscoverOauthServerConfigurationResponse")


@_attrs_define
class DiscoverOauthServerConfigurationResponse:
    """Response schema for Discover OAuth Server Configuration

    Example:
        {'issuer': 'https://social.example/', 'service_documentation': 'https://docs.joinmastodon.org/',
            'authorization_endpoint': 'https://social.example/oauth/authorize', 'token_endpoint':
            'https://social.example/oauth/token', 'app_registration_endpoint': 'https://social.example/api/v1/apps',
            'revocation_endpoint': 'https://social.example/oauth/revoke', 'userinfo_endpoint':
            'https://social.example/oauth/userinfo', 'scopes_supported': ['read', 'write', 'write:accounts', 'write:blocks',
            'write:bookmarks', 'write:conversations', 'write:favourites', 'write:filters', 'write:follows', 'write:lists',
            'write:media', 'write:mutes', 'write:notifications', 'write:reports', 'write:statuses', 'read:accounts',
            'read:blocks', 'read:bookmarks', 'read:favourites', 'read:filters', 'read:follows', 'read:lists', 'read:mutes',
            'read:notifications', 'read:search', 'read:statuses', 'follow', 'push', 'profile', 'admin:read',
            'admin:read:accounts', 'admin:read:reports', 'admin:read:domain_allows', 'admin:read:domain_blocks',
            'admin:read:ip_blocks', 'admin:read:email_domain_blocks', 'admin:read:canonical_email_blocks', 'admin:write',
            'admin:write:accounts', 'admin:write:reports', 'admin:write:domain_allows', 'admin:write:domain_blocks',
            'admin:write:ip_blocks', 'admin:write:email_domain_blocks', 'admin:write:canonical_email_blocks'],
            'response_types_supported': ['code'], 'response_modes_supported': ['query', 'fragment', 'form_post'],
            'code_challenge_methods_supported': ['S256'], 'grant_types_supported': ['authorization_code',
            'client_credentials'], 'token_endpoint_auth_methods_supported': ['client_secret_basic', 'client_secret_post']}

    Attributes:
        app_registration_endpoint (str): app_registration_endpoint field
        authorization_endpoint (str): authorization_endpoint field
        code_challenge_methods_supported (list[str]): Array of code_challenge_methods_supported
        grant_types_supported (list[str]): Array of grant_types_supported
        issuer (str): issuer field
        response_modes_supported (list[str]): Array of response_modes_supported
        response_types_supported (list[str]): Array of response_types_supported
        revocation_endpoint (str): revocation_endpoint field
        scopes_supported (list[OAuthScope]): Array of OAuth scopes
        service_documentation (str): service_documentation field
        token_endpoint (str): token_endpoint field
        token_endpoint_auth_methods_supported (list[str]): Array of token_endpoint_auth_methods_supported
        userinfo_endpoint (str): userinfo_endpoint field
    """

    app_registration_endpoint: str
    authorization_endpoint: str
    code_challenge_methods_supported: list[str]
    grant_types_supported: list[str]
    issuer: str
    response_modes_supported: list[str]
    response_types_supported: list[str]
    revocation_endpoint: str
    scopes_supported: list[OAuthScope]
    service_documentation: str
    token_endpoint: str
    token_endpoint_auth_methods_supported: list[str]
    userinfo_endpoint: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        app_registration_endpoint = self.app_registration_endpoint

        authorization_endpoint = self.authorization_endpoint

        code_challenge_methods_supported = self.code_challenge_methods_supported

        grant_types_supported = self.grant_types_supported

        issuer = self.issuer

        response_modes_supported = self.response_modes_supported

        response_types_supported = self.response_types_supported

        revocation_endpoint = self.revocation_endpoint

        scopes_supported = []
        for componentsschemas_o_auth_scopes_item_data in self.scopes_supported:
            componentsschemas_o_auth_scopes_item = (
                componentsschemas_o_auth_scopes_item_data.value
            )
            scopes_supported.append(componentsschemas_o_auth_scopes_item)

        service_documentation = self.service_documentation

        token_endpoint = self.token_endpoint

        token_endpoint_auth_methods_supported = (
            self.token_endpoint_auth_methods_supported
        )

        userinfo_endpoint = self.userinfo_endpoint

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "app_registration_endpoint": app_registration_endpoint,
                "authorization_endpoint": authorization_endpoint,
                "code_challenge_methods_supported": code_challenge_methods_supported,
                "grant_types_supported": grant_types_supported,
                "issuer": issuer,
                "response_modes_supported": response_modes_supported,
                "response_types_supported": response_types_supported,
                "revocation_endpoint": revocation_endpoint,
                "scopes_supported": scopes_supported,
                "service_documentation": service_documentation,
                "token_endpoint": token_endpoint,
                "token_endpoint_auth_methods_supported": token_endpoint_auth_methods_supported,
                "userinfo_endpoint": userinfo_endpoint,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        app_registration_endpoint = d.pop("app_registration_endpoint")

        authorization_endpoint = d.pop("authorization_endpoint")

        code_challenge_methods_supported = cast(
            list[str], d.pop("code_challenge_methods_supported")
        )

        grant_types_supported = cast(list[str], d.pop("grant_types_supported"))

        issuer = d.pop("issuer")

        response_modes_supported = cast(list[str], d.pop("response_modes_supported"))

        response_types_supported = cast(list[str], d.pop("response_types_supported"))

        revocation_endpoint = d.pop("revocation_endpoint")

        scopes_supported = []
        _scopes_supported = d.pop("scopes_supported")
        for componentsschemas_o_auth_scopes_item_data in _scopes_supported:
            componentsschemas_o_auth_scopes_item = OAuthScope(
                componentsschemas_o_auth_scopes_item_data
            )

            scopes_supported.append(componentsschemas_o_auth_scopes_item)

        service_documentation = d.pop("service_documentation")

        token_endpoint = d.pop("token_endpoint")

        token_endpoint_auth_methods_supported = cast(
            list[str], d.pop("token_endpoint_auth_methods_supported")
        )

        userinfo_endpoint = d.pop("userinfo_endpoint")

        discover_oauth_server_configuration_response = cls(
            app_registration_endpoint=app_registration_endpoint,
            authorization_endpoint=authorization_endpoint,
            code_challenge_methods_supported=code_challenge_methods_supported,
            grant_types_supported=grant_types_supported,
            issuer=issuer,
            response_modes_supported=response_modes_supported,
            response_types_supported=response_types_supported,
            revocation_endpoint=revocation_endpoint,
            scopes_supported=scopes_supported,
            service_documentation=service_documentation,
            token_endpoint=token_endpoint,
            token_endpoint_auth_methods_supported=token_endpoint_auth_methods_supported,
            userinfo_endpoint=userinfo_endpoint,
        )

        discover_oauth_server_configuration_response.additional_properties = d
        return discover_oauth_server_configuration_response

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
