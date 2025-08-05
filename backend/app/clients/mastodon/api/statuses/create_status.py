from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.media_status import MediaStatus
from ...models.poll_status import PollStatus
from ...models.scheduled_status import ScheduledStatus
from ...models.status import Status
from ...models.text_status import TextStatus
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    body: Union["MediaStatus", "PollStatus", "TextStatus"],
    idempotency_key: Union[Unset, str] = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(idempotency_key, Unset):
        headers["Idempotency-Key"] = idempotency_key

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/v1/statuses",
    }

    _kwargs["json"]: dict[str, Any]
    if isinstance(body, TextStatus):
        _kwargs["json"] = body.to_dict()
    elif isinstance(body, MediaStatus):
        _kwargs["json"] = body.to_dict()
    else:
        _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, Error, Union["ScheduledStatus", "Status"]]]:
    if response.status_code == 200:

        def _parse_response_200(data: object) -> Union["ScheduledStatus", "Status"]:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                response_200_type_0 = Status.from_dict(data)

                return response_200_type_0
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            response_200_type_1 = ScheduledStatus.from_dict(data)

            return response_200_type_1

        response_200 = _parse_response_200(response.json())

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
) -> Response[Union[Any, Error, Union["ScheduledStatus", "Status"]]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: Union["MediaStatus", "PollStatus", "TextStatus"],
    idempotency_key: Union[Unset, str] = UNSET,
) -> Response[Union[Any, Error, Union["ScheduledStatus", "Status"]]]:
    r""" Post a new status

     Publish a status with the given parameters.

    Version history:

    0.0.0 - added\
    2.7.0 - `scheduled_at` added\
    2.8.0 - `poll` added

    Args:
        idempotency_key (Union[Unset, str]):
        body (Union['MediaStatus', 'PollStatus', 'TextStatus']):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, Error, Union['ScheduledStatus', 'Status']]]
     """

    kwargs = _get_kwargs(
        body=body,
        idempotency_key=idempotency_key,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    body: Union["MediaStatus", "PollStatus", "TextStatus"],
    idempotency_key: Union[Unset, str] = UNSET,
) -> Optional[Union[Any, Error, Union["ScheduledStatus", "Status"]]]:
    r""" Post a new status

     Publish a status with the given parameters.

    Version history:

    0.0.0 - added\
    2.7.0 - `scheduled_at` added\
    2.8.0 - `poll` added

    Args:
        idempotency_key (Union[Unset, str]):
        body (Union['MediaStatus', 'PollStatus', 'TextStatus']):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, Error, Union['ScheduledStatus', 'Status']]
     """

    return sync_detailed(
        client=client,
        body=body,
        idempotency_key=idempotency_key,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: Union["MediaStatus", "PollStatus", "TextStatus"],
    idempotency_key: Union[Unset, str] = UNSET,
) -> Response[Union[Any, Error, Union["ScheduledStatus", "Status"]]]:
    r""" Post a new status

     Publish a status with the given parameters.

    Version history:

    0.0.0 - added\
    2.7.0 - `scheduled_at` added\
    2.8.0 - `poll` added

    Args:
        idempotency_key (Union[Unset, str]):
        body (Union['MediaStatus', 'PollStatus', 'TextStatus']):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, Error, Union['ScheduledStatus', 'Status']]]
     """

    kwargs = _get_kwargs(
        body=body,
        idempotency_key=idempotency_key,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    body: Union["MediaStatus", "PollStatus", "TextStatus"],
    idempotency_key: Union[Unset, str] = UNSET,
) -> Optional[Union[Any, Error, Union["ScheduledStatus", "Status"]]]:
    r""" Post a new status

     Publish a status with the given parameters.

    Version history:

    0.0.0 - added\
    2.7.0 - `scheduled_at` added\
    2.8.0 - `poll` added

    Args:
        idempotency_key (Union[Unset, str]):
        body (Union['MediaStatus', 'PollStatus', 'TextStatus']):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, Error, Union['ScheduledStatus', 'Status']]
     """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
            idempotency_key=idempotency_key,
        )
    ).parsed
