from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.grouped_notifications_results import GroupedNotificationsResults
from ...models.validation_error import ValidationError
from ...types import Response


def _get_kwargs(
    group_key: str,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/v2/notifications/{group_key}".format(
            group_key=group_key,
        ),
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, Error, GroupedNotificationsResults, ValidationError]]:
    if response.status_code == 200:
        response_200 = GroupedNotificationsResults.from_dict(response.json())

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
) -> Response[Union[Any, Error, GroupedNotificationsResults, ValidationError]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    group_key: str,
    *,
    client: AuthenticatedClient,
) -> Response[Union[Any, Error, GroupedNotificationsResults, ValidationError]]:
    """Get a single notification group

     View information about a specific notification group with a given group key.

    Version history:

    4.3.0 (`mastodon` [API version] 2) - added

    Args:
        group_key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, Error, GroupedNotificationsResults, ValidationError]]
    """

    kwargs = _get_kwargs(
        group_key=group_key,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    group_key: str,
    *,
    client: AuthenticatedClient,
) -> Optional[Union[Any, Error, GroupedNotificationsResults, ValidationError]]:
    """Get a single notification group

     View information about a specific notification group with a given group key.

    Version history:

    4.3.0 (`mastodon` [API version] 2) - added

    Args:
        group_key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, Error, GroupedNotificationsResults, ValidationError]
    """

    return sync_detailed(
        group_key=group_key,
        client=client,
    ).parsed


async def asyncio_detailed(
    group_key: str,
    *,
    client: AuthenticatedClient,
) -> Response[Union[Any, Error, GroupedNotificationsResults, ValidationError]]:
    """Get a single notification group

     View information about a specific notification group with a given group key.

    Version history:

    4.3.0 (`mastodon` [API version] 2) - added

    Args:
        group_key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, Error, GroupedNotificationsResults, ValidationError]]
    """

    kwargs = _get_kwargs(
        group_key=group_key,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    group_key: str,
    *,
    client: AuthenticatedClient,
) -> Optional[Union[Any, Error, GroupedNotificationsResults, ValidationError]]:
    """Get a single notification group

     View information about a specific notification group with a given group key.

    Version history:

    4.3.0 (`mastodon` [API version] 2) - added

    Args:
        group_key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, Error, GroupedNotificationsResults, ValidationError]
    """

    return (
        await asyncio_detailed(
            group_key=group_key,
            client=client,
        )
    ).parsed
