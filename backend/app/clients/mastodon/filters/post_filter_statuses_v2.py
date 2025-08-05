from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.filter_status import FilterStatus
from ...models.post_filter_statuses_v2_body import PostFilterStatusesV2Body
from ...models.validation_error import ValidationError
from ...types import Response


def _get_kwargs(
    filter_id: str,
    *,
    body: PostFilterStatusesV2Body,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/v2/filters/{filter_id}/statuses".format(
            filter_id=filter_id,
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, Error, FilterStatus, ValidationError]]:
    if response.status_code == 200:
        response_200 = FilterStatus.from_dict(response.json())

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
) -> Response[Union[Any, Error, FilterStatus, ValidationError]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    filter_id: str,
    *,
    client: AuthenticatedClient,
    body: PostFilterStatusesV2Body,
) -> Response[Union[Any, Error, FilterStatus, ValidationError]]:
    """Add a status to a filter group

     Add a status filter to the current filter group.

    Version history:

    4.0.0 - added

    Args:
        filter_id (str):
        body (PostFilterStatusesV2Body):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, Error, FilterStatus, ValidationError]]
    """

    kwargs = _get_kwargs(
        filter_id=filter_id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    filter_id: str,
    *,
    client: AuthenticatedClient,
    body: PostFilterStatusesV2Body,
) -> Optional[Union[Any, Error, FilterStatus, ValidationError]]:
    """Add a status to a filter group

     Add a status filter to the current filter group.

    Version history:

    4.0.0 - added

    Args:
        filter_id (str):
        body (PostFilterStatusesV2Body):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, Error, FilterStatus, ValidationError]
    """

    return sync_detailed(
        filter_id=filter_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    filter_id: str,
    *,
    client: AuthenticatedClient,
    body: PostFilterStatusesV2Body,
) -> Response[Union[Any, Error, FilterStatus, ValidationError]]:
    """Add a status to a filter group

     Add a status filter to the current filter group.

    Version history:

    4.0.0 - added

    Args:
        filter_id (str):
        body (PostFilterStatusesV2Body):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, Error, FilterStatus, ValidationError]]
    """

    kwargs = _get_kwargs(
        filter_id=filter_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    filter_id: str,
    *,
    client: AuthenticatedClient,
    body: PostFilterStatusesV2Body,
) -> Optional[Union[Any, Error, FilterStatus, ValidationError]]:
    """Add a status to a filter group

     Add a status filter to the current filter group.

    Version history:

    4.0.0 - added

    Args:
        filter_id (str):
        body (PostFilterStatusesV2Body):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, Error, FilterStatus, ValidationError]
    """

    return (
        await asyncio_detailed(
            filter_id=filter_id,
            client=client,
            body=body,
        )
    ).parsed
