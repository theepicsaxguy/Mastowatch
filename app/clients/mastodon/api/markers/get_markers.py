from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.get_markers_timeline_item import GetMarkersTimelineItem
from ...models.marker import Marker
from ...models.validation_error import ValidationError
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    timeline: Union[Unset, list[GetMarkersTimelineItem]] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_timeline: Union[Unset, list[str]] = UNSET
    if not isinstance(timeline, Unset):
        json_timeline = []
        for timeline_item_data in timeline:
            timeline_item = timeline_item_data.value
            json_timeline.append(timeline_item)

    params["timeline"] = json_timeline

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/v1/markers",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, Error, Marker, ValidationError]]:
    if response.status_code == 200:
        response_200 = Marker.from_dict(response.json())

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
) -> Response[Union[Any, Error, Marker, ValidationError]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    timeline: Union[Unset, list[GetMarkersTimelineItem]] = UNSET,
) -> Response[Union[Any, Error, Marker, ValidationError]]:
    """Get saved timeline positions

     Get current positions in timelines.

    Version history:

    3.0.0 - added

    Args:
        timeline (Union[Unset, list[GetMarkersTimelineItem]]): Specify the timeline(s) for which
            markers should be fetched. Possible values: `home`, `notifications`. If not provided, an
            empty object will be returned.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, Error, Marker, ValidationError]]
    """

    kwargs = _get_kwargs(
        timeline=timeline,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    timeline: Union[Unset, list[GetMarkersTimelineItem]] = UNSET,
) -> Optional[Union[Any, Error, Marker, ValidationError]]:
    """Get saved timeline positions

     Get current positions in timelines.

    Version history:

    3.0.0 - added

    Args:
        timeline (Union[Unset, list[GetMarkersTimelineItem]]): Specify the timeline(s) for which
            markers should be fetched. Possible values: `home`, `notifications`. If not provided, an
            empty object will be returned.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, Error, Marker, ValidationError]
    """

    return sync_detailed(
        client=client,
        timeline=timeline,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    timeline: Union[Unset, list[GetMarkersTimelineItem]] = UNSET,
) -> Response[Union[Any, Error, Marker, ValidationError]]:
    """Get saved timeline positions

     Get current positions in timelines.

    Version history:

    3.0.0 - added

    Args:
        timeline (Union[Unset, list[GetMarkersTimelineItem]]): Specify the timeline(s) for which
            markers should be fetched. Possible values: `home`, `notifications`. If not provided, an
            empty object will be returned.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, Error, Marker, ValidationError]]
    """

    kwargs = _get_kwargs(
        timeline=timeline,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    timeline: Union[Unset, list[GetMarkersTimelineItem]] = UNSET,
) -> Optional[Union[Any, Error, Marker, ValidationError]]:
    """Get saved timeline positions

     Get current positions in timelines.

    Version history:

    3.0.0 - added

    Args:
        timeline (Union[Unset, list[GetMarkersTimelineItem]]): Specify the timeline(s) for which
            markers should be fetched. Possible values: `home`, `notifications`. If not provided, an
            empty object will be returned.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, Error, Marker, ValidationError]
    """

    return (
        await asyncio_detailed(
            client=client,
            timeline=timeline,
        )
    ).parsed
