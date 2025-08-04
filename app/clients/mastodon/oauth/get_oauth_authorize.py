from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.validation_error import ValidationError
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client_id: str,
    redirect_uri: str,
    response_type: str,
    code_challenge: Union[Unset, str] = UNSET,
    code_challenge_method: Union[Unset, str] = UNSET,
    force_login: Union[Unset, bool] = UNSET,
    lang: Union[Unset, str] = UNSET,
    scope: Union[Unset, str] = "read",
    state: Union[Unset, str] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["client_id"] = client_id

    params["redirect_uri"] = redirect_uri

    params["response_type"] = response_type

    params["code_challenge"] = code_challenge

    params["code_challenge_method"] = code_challenge_method

    params["force_login"] = force_login

    params["lang"] = lang

    params["scope"] = scope

    params["state"] = state

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/oauth/authorize",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, Error, ValidationError]]:
    if response.status_code == 200:
        response_200 = cast(Any, None)
        return response_200
    if response.status_code == 401:
        response_401 = Error.from_dict(response.json())

        return response_401
    if response.status_code == 404:
        response_404 = Error.from_dict(response.json())

        return response_404
    if response.status_code == 410:
        response_410 = cast(Any, None)
        return response_410
    if response.status_code == 422:
        response_422 = ValidationError.from_dict(response.json())

        return response_422
    if response.status_code == 429:
        response_429 = Error.from_dict(response.json())

        return response_429
    if response.status_code == 503:
        response_503 = Error.from_dict(response.json())

        return response_503
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[Any, Error, ValidationError]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    client_id: str,
    redirect_uri: str,
    response_type: str,
    code_challenge: Union[Unset, str] = UNSET,
    code_challenge_method: Union[Unset, str] = UNSET,
    force_login: Union[Unset, bool] = UNSET,
    lang: Union[Unset, str] = UNSET,
    scope: Union[Unset, str] = "read",
    state: Union[Unset, str] = UNSET,
) -> Response[Union[Any, Error, ValidationError]]:
    r""" Authorize a user

     Displays an authorization form to the user. If approved, it will create and return an authorization
    code, then redirect to the desired `redirect_uri`, or show the authorization code if
    `urn:ietf:wg:oauth:2.0:oob` was requested. The authorization code can be used while requesting a
    token to obtain access to user-level methods.

    Version history:

    0.1.0 - added\
    2.6.0 - added `force_login`\
    3.5.0 - added `lang`\
    4.3.0 - added support for PKCE parameters

    Args:
        client_id (str): The client ID, obtained during app registration.
        redirect_uri (str): Set a URI to redirect the user to. If this parameter is set to
            `urn:ietf:wg:oauth:2.0:oob` then the authorization code will be shown instead. Must match
            one of the `redirect_uris` declared during app registration.
        response_type (str): Should be set equal to `code`.
        code_challenge (Union[Unset, str]): The [PKCE code challenge] for the authorization
            request.
        code_challenge_method (Union[Unset, str]): Must be `S256`, as this is the only code
            challenge method that is supported by Mastodon for PKCE.
        force_login (Union[Unset, bool]): Forces the user to re-login, which is necessary for
            authorizing with multiple accounts from the same instance.
        lang (Union[Unset, str]): The ISO 639-1 two-letter language code to use while rendering
            the authorization form.
        scope (Union[Unset, str]): List of requested [OAuth scopes], separated by spaces (or by
            pluses, if using query parameters). Must be a subset of `scopes` declared during app
            registration. If not provided, defaults to `read`. Default: 'read'.
        state (Union[Unset, str]): Arbitrary value to passthrough to your server when the user
            authorizes or rejects the authorization request.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, Error, ValidationError]]
     """

    kwargs = _get_kwargs(
        client_id=client_id,
        redirect_uri=redirect_uri,
        response_type=response_type,
        code_challenge=code_challenge,
        code_challenge_method=code_challenge_method,
        force_login=force_login,
        lang=lang,
        scope=scope,
        state=state,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    client_id: str,
    redirect_uri: str,
    response_type: str,
    code_challenge: Union[Unset, str] = UNSET,
    code_challenge_method: Union[Unset, str] = UNSET,
    force_login: Union[Unset, bool] = UNSET,
    lang: Union[Unset, str] = UNSET,
    scope: Union[Unset, str] = "read",
    state: Union[Unset, str] = UNSET,
) -> Optional[Union[Any, Error, ValidationError]]:
    r""" Authorize a user

     Displays an authorization form to the user. If approved, it will create and return an authorization
    code, then redirect to the desired `redirect_uri`, or show the authorization code if
    `urn:ietf:wg:oauth:2.0:oob` was requested. The authorization code can be used while requesting a
    token to obtain access to user-level methods.

    Version history:

    0.1.0 - added\
    2.6.0 - added `force_login`\
    3.5.0 - added `lang`\
    4.3.0 - added support for PKCE parameters

    Args:
        client_id (str): The client ID, obtained during app registration.
        redirect_uri (str): Set a URI to redirect the user to. If this parameter is set to
            `urn:ietf:wg:oauth:2.0:oob` then the authorization code will be shown instead. Must match
            one of the `redirect_uris` declared during app registration.
        response_type (str): Should be set equal to `code`.
        code_challenge (Union[Unset, str]): The [PKCE code challenge] for the authorization
            request.
        code_challenge_method (Union[Unset, str]): Must be `S256`, as this is the only code
            challenge method that is supported by Mastodon for PKCE.
        force_login (Union[Unset, bool]): Forces the user to re-login, which is necessary for
            authorizing with multiple accounts from the same instance.
        lang (Union[Unset, str]): The ISO 639-1 two-letter language code to use while rendering
            the authorization form.
        scope (Union[Unset, str]): List of requested [OAuth scopes], separated by spaces (or by
            pluses, if using query parameters). Must be a subset of `scopes` declared during app
            registration. If not provided, defaults to `read`. Default: 'read'.
        state (Union[Unset, str]): Arbitrary value to passthrough to your server when the user
            authorizes or rejects the authorization request.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, Error, ValidationError]
     """

    return sync_detailed(
        client=client,
        client_id=client_id,
        redirect_uri=redirect_uri,
        response_type=response_type,
        code_challenge=code_challenge,
        code_challenge_method=code_challenge_method,
        force_login=force_login,
        lang=lang,
        scope=scope,
        state=state,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    client_id: str,
    redirect_uri: str,
    response_type: str,
    code_challenge: Union[Unset, str] = UNSET,
    code_challenge_method: Union[Unset, str] = UNSET,
    force_login: Union[Unset, bool] = UNSET,
    lang: Union[Unset, str] = UNSET,
    scope: Union[Unset, str] = "read",
    state: Union[Unset, str] = UNSET,
) -> Response[Union[Any, Error, ValidationError]]:
    r""" Authorize a user

     Displays an authorization form to the user. If approved, it will create and return an authorization
    code, then redirect to the desired `redirect_uri`, or show the authorization code if
    `urn:ietf:wg:oauth:2.0:oob` was requested. The authorization code can be used while requesting a
    token to obtain access to user-level methods.

    Version history:

    0.1.0 - added\
    2.6.0 - added `force_login`\
    3.5.0 - added `lang`\
    4.3.0 - added support for PKCE parameters

    Args:
        client_id (str): The client ID, obtained during app registration.
        redirect_uri (str): Set a URI to redirect the user to. If this parameter is set to
            `urn:ietf:wg:oauth:2.0:oob` then the authorization code will be shown instead. Must match
            one of the `redirect_uris` declared during app registration.
        response_type (str): Should be set equal to `code`.
        code_challenge (Union[Unset, str]): The [PKCE code challenge] for the authorization
            request.
        code_challenge_method (Union[Unset, str]): Must be `S256`, as this is the only code
            challenge method that is supported by Mastodon for PKCE.
        force_login (Union[Unset, bool]): Forces the user to re-login, which is necessary for
            authorizing with multiple accounts from the same instance.
        lang (Union[Unset, str]): The ISO 639-1 two-letter language code to use while rendering
            the authorization form.
        scope (Union[Unset, str]): List of requested [OAuth scopes], separated by spaces (or by
            pluses, if using query parameters). Must be a subset of `scopes` declared during app
            registration. If not provided, defaults to `read`. Default: 'read'.
        state (Union[Unset, str]): Arbitrary value to passthrough to your server when the user
            authorizes or rejects the authorization request.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, Error, ValidationError]]
     """

    kwargs = _get_kwargs(
        client_id=client_id,
        redirect_uri=redirect_uri,
        response_type=response_type,
        code_challenge=code_challenge,
        code_challenge_method=code_challenge_method,
        force_login=force_login,
        lang=lang,
        scope=scope,
        state=state,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    client_id: str,
    redirect_uri: str,
    response_type: str,
    code_challenge: Union[Unset, str] = UNSET,
    code_challenge_method: Union[Unset, str] = UNSET,
    force_login: Union[Unset, bool] = UNSET,
    lang: Union[Unset, str] = UNSET,
    scope: Union[Unset, str] = "read",
    state: Union[Unset, str] = UNSET,
) -> Optional[Union[Any, Error, ValidationError]]:
    r""" Authorize a user

     Displays an authorization form to the user. If approved, it will create and return an authorization
    code, then redirect to the desired `redirect_uri`, or show the authorization code if
    `urn:ietf:wg:oauth:2.0:oob` was requested. The authorization code can be used while requesting a
    token to obtain access to user-level methods.

    Version history:

    0.1.0 - added\
    2.6.0 - added `force_login`\
    3.5.0 - added `lang`\
    4.3.0 - added support for PKCE parameters

    Args:
        client_id (str): The client ID, obtained during app registration.
        redirect_uri (str): Set a URI to redirect the user to. If this parameter is set to
            `urn:ietf:wg:oauth:2.0:oob` then the authorization code will be shown instead. Must match
            one of the `redirect_uris` declared during app registration.
        response_type (str): Should be set equal to `code`.
        code_challenge (Union[Unset, str]): The [PKCE code challenge] for the authorization
            request.
        code_challenge_method (Union[Unset, str]): Must be `S256`, as this is the only code
            challenge method that is supported by Mastodon for PKCE.
        force_login (Union[Unset, bool]): Forces the user to re-login, which is necessary for
            authorizing with multiple accounts from the same instance.
        lang (Union[Unset, str]): The ISO 639-1 two-letter language code to use while rendering
            the authorization form.
        scope (Union[Unset, str]): List of requested [OAuth scopes], separated by spaces (or by
            pluses, if using query parameters). Must be a subset of `scopes` declared during app
            registration. If not provided, defaults to `read`. Default: 'read'.
        state (Union[Unset, str]): Arbitrary value to passthrough to your server when the user
            authorizes or rejects the authorization request.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, Error, ValidationError]
     """

    return (
        await asyncio_detailed(
            client=client,
            client_id=client_id,
            redirect_uri=redirect_uri,
            response_type=response_type,
            code_challenge=code_challenge,
            code_challenge_method=code_challenge_method,
            force_login=force_login,
            lang=lang,
            scope=scope,
            state=state,
        )
    ).parsed
