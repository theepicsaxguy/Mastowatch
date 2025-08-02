from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.create_app_body import CreateAppBody
from ...models.credential_application import CredentialApplication
from ...models.error import Error
from ...types import Response


def _get_kwargs(
    *,
    body: CreateAppBody,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/v1/apps",
    }

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, CredentialApplication, Error]]:
    if response.status_code == 200:
        response_200 = CredentialApplication.from_dict(response.json())

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
        response_422 = Error.from_dict(response.json())

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
) -> Response[Union[Any, CredentialApplication, Error]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: CreateAppBody,
) -> Response[Union[Any, CredentialApplication, Error]]:
    r""" Create an application

     Create a new application to obtain OAuth2 credentials.

    Version history:

    0.0.0 - added\
    2.7.2 - now returns `vapid_key`\
    4.3.0 - deprecated `vapid_key`, please see [api/v2/instance]\
    4.3.0 - added support for multiple `redirect_uris` in Form data parameters\
    4.3.0 - added `redirect_uris` response property\
    4.3.0 - deprecated `redirect_uri` response property, since this can be a non-URI if multiple
    `redirect_uris` are registered, use `redirect_uris` instead\
    4.3.0 - changed entity type from [Application] to [CredentialApplication]

    Args:
        body (CreateAppBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, CredentialApplication, Error]]
     """

    kwargs = _get_kwargs(
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    body: CreateAppBody,
) -> Optional[Union[Any, CredentialApplication, Error]]:
    r""" Create an application

     Create a new application to obtain OAuth2 credentials.

    Version history:

    0.0.0 - added\
    2.7.2 - now returns `vapid_key`\
    4.3.0 - deprecated `vapid_key`, please see [api/v2/instance]\
    4.3.0 - added support for multiple `redirect_uris` in Form data parameters\
    4.3.0 - added `redirect_uris` response property\
    4.3.0 - deprecated `redirect_uri` response property, since this can be a non-URI if multiple
    `redirect_uris` are registered, use `redirect_uris` instead\
    4.3.0 - changed entity type from [Application] to [CredentialApplication]

    Args:
        body (CreateAppBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, CredentialApplication, Error]
     """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: CreateAppBody,
) -> Response[Union[Any, CredentialApplication, Error]]:
    r""" Create an application

     Create a new application to obtain OAuth2 credentials.

    Version history:

    0.0.0 - added\
    2.7.2 - now returns `vapid_key`\
    4.3.0 - deprecated `vapid_key`, please see [api/v2/instance]\
    4.3.0 - added support for multiple `redirect_uris` in Form data parameters\
    4.3.0 - added `redirect_uris` response property\
    4.3.0 - deprecated `redirect_uri` response property, since this can be a non-URI if multiple
    `redirect_uris` are registered, use `redirect_uris` instead\
    4.3.0 - changed entity type from [Application] to [CredentialApplication]

    Args:
        body (CreateAppBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, CredentialApplication, Error]]
     """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    body: CreateAppBody,
) -> Optional[Union[Any, CredentialApplication, Error]]:
    r""" Create an application

     Create a new application to obtain OAuth2 credentials.

    Version history:

    0.0.0 - added\
    2.7.2 - now returns `vapid_key`\
    4.3.0 - deprecated `vapid_key`, please see [api/v2/instance]\
    4.3.0 - added support for multiple `redirect_uris` in Form data parameters\
    4.3.0 - added `redirect_uris` response property\
    4.3.0 - deprecated `redirect_uri` response property, since this can be a non-URI if multiple
    `redirect_uris` are registered, use `redirect_uris` instead\
    4.3.0 - changed entity type from [Application] to [CredentialApplication]

    Args:
        body (CreateAppBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, CredentialApplication, Error]
     """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
