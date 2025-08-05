from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.terms_of_service import TermsOfService
from ...models.validation_error import ValidationError
from ...types import Response


def _get_kwargs(
    date: str,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/v1/instance/terms_of_service/{date}".format(
            date=date,
        ),
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, Error, TermsOfService, ValidationError]]:
    if response.status_code == 200:
        response_200 = TermsOfService.from_dict(response.json())

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
) -> Response[Union[Any, Error, TermsOfService, ValidationError]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    date: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[Union[Any, Error, TermsOfService, ValidationError]]:
    """View a specific version of the terms of service

     Obtain the contents of this server's terms of service, for a specified date, if configured.

    Version history:

    4.4.0 - added

    Args:
        date (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, Error, TermsOfService, ValidationError]]
    """

    kwargs = _get_kwargs(
        date=date,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    date: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[Union[Any, Error, TermsOfService, ValidationError]]:
    """View a specific version of the terms of service

     Obtain the contents of this server's terms of service, for a specified date, if configured.

    Version history:

    4.4.0 - added

    Args:
        date (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, Error, TermsOfService, ValidationError]
    """

    return sync_detailed(
        date=date,
        client=client,
    ).parsed


async def asyncio_detailed(
    date: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[Union[Any, Error, TermsOfService, ValidationError]]:
    """View a specific version of the terms of service

     Obtain the contents of this server's terms of service, for a specified date, if configured.

    Version history:

    4.4.0 - added

    Args:
        date (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, Error, TermsOfService, ValidationError]]
    """

    kwargs = _get_kwargs(
        date=date,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    date: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[Union[Any, Error, TermsOfService, ValidationError]]:
    """View a specific version of the terms of service

     Obtain the contents of this server's terms of service, for a specified date, if configured.

    Version history:

    4.4.0 - added

    Args:
        date (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, Error, TermsOfService, ValidationError]
    """

    return (
        await asyncio_detailed(
            date=date,
            client=client,
        )
    ).parsed
