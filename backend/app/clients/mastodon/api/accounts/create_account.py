from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.create_account_body import CreateAccountBody
from ...models.error import Error
from ...models.token import Token
from ...models.validation_error import ValidationError
from ...types import Response


def _get_kwargs(
    *,
    body: CreateAccountBody,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/v1/accounts",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, Error, Token, ValidationError]]:
    if response.status_code == 200:
        response_200 = Token.from_dict(response.json())

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
) -> Response[Union[Any, Error, Token, ValidationError]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: CreateAccountBody,
) -> Response[Union[Any, Error, Token, ValidationError]]:
    r""" Register an account

     Creates a user and account records. Returns an account access token for the app that initiated the
    request. The app should save this token for later, and should wait for the user to confirm their
    account by clicking a link in their email inbox.

    Version history:

    2.7.0 - added\
    3.0.0 - added `reason` parameter\
    3.4.0 - added `details` to failure response\
    4.4.0 - added `date_of_birth` parameter

    Args:
        body (CreateAccountBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, Error, Token, ValidationError]]
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
    client: AuthenticatedClient,
    body: CreateAccountBody,
) -> Optional[Union[Any, Error, Token, ValidationError]]:
    r""" Register an account

     Creates a user and account records. Returns an account access token for the app that initiated the
    request. The app should save this token for later, and should wait for the user to confirm their
    account by clicking a link in their email inbox.

    Version history:

    2.7.0 - added\
    3.0.0 - added `reason` parameter\
    3.4.0 - added `details` to failure response\
    4.4.0 - added `date_of_birth` parameter

    Args:
        body (CreateAccountBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, Error, Token, ValidationError]
     """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: CreateAccountBody,
) -> Response[Union[Any, Error, Token, ValidationError]]:
    r""" Register an account

     Creates a user and account records. Returns an account access token for the app that initiated the
    request. The app should save this token for later, and should wait for the user to confirm their
    account by clicking a link in their email inbox.

    Version history:

    2.7.0 - added\
    3.0.0 - added `reason` parameter\
    3.4.0 - added `details` to failure response\
    4.4.0 - added `date_of_birth` parameter

    Args:
        body (CreateAccountBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, Error, Token, ValidationError]]
     """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    body: CreateAccountBody,
) -> Optional[Union[Any, Error, Token, ValidationError]]:
    r""" Register an account

     Creates a user and account records. Returns an account access token for the app that initiated the
    request. The app should save this token for later, and should wait for the user to confirm their
    account by clicking a link in their email inbox.

    Version history:

    2.7.0 - added\
    3.0.0 - added `reason` parameter\
    3.4.0 - added `details` to failure response\
    4.4.0 - added `date_of_birth` parameter

    Args:
        body (CreateAccountBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, Error, Token, ValidationError]
     """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
