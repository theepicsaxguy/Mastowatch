from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.create_push_subscription_body import CreatePushSubscriptionBody
from ...models.error import Error
from ...models.validation_error import ValidationError
from ...models.web_push_subscription import WebPushSubscription
from ...types import Response


def _get_kwargs(
    *,
    body: CreatePushSubscriptionBody,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/v1/push/subscription",
    }

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, Error, ValidationError, WebPushSubscription]]:
    if response.status_code == 200:
        response_200 = WebPushSubscription.from_dict(response.json())

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
) -> Response[Union[Any, Error, ValidationError, WebPushSubscription]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: CreatePushSubscriptionBody,
) -> Response[Union[Any, Error, ValidationError, WebPushSubscription]]:
    r""" Subscribe to push notifications

     Add a Web Push API subscription to receive notifications. Each access token can have one push
    subscription. If you create a new subscription, the old subscription is deleted.

    Version history:

    2.4.0 - added\
    3.3.0 - added `data[alerts][status]`\
    3.4.0 - added `data[policy]`\
    3.5.0 - added `data[alerts][update]` and `data[alerts][admin.sign_up]`\
    4.0.0 - added `data[alerts][admin.report]`\
    4.3.0 - added stricter request parameter validation, invalid endpoint URLs and subscription keys
    will now result in an error, previously these would be accepted, but silently fail.\
    4.4.0 - added `subscription[standard]`

    Args:
        body (CreatePushSubscriptionBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, Error, ValidationError, WebPushSubscription]]
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
    body: CreatePushSubscriptionBody,
) -> Optional[Union[Any, Error, ValidationError, WebPushSubscription]]:
    r""" Subscribe to push notifications

     Add a Web Push API subscription to receive notifications. Each access token can have one push
    subscription. If you create a new subscription, the old subscription is deleted.

    Version history:

    2.4.0 - added\
    3.3.0 - added `data[alerts][status]`\
    3.4.0 - added `data[policy]`\
    3.5.0 - added `data[alerts][update]` and `data[alerts][admin.sign_up]`\
    4.0.0 - added `data[alerts][admin.report]`\
    4.3.0 - added stricter request parameter validation, invalid endpoint URLs and subscription keys
    will now result in an error, previously these would be accepted, but silently fail.\
    4.4.0 - added `subscription[standard]`

    Args:
        body (CreatePushSubscriptionBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, Error, ValidationError, WebPushSubscription]
     """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: CreatePushSubscriptionBody,
) -> Response[Union[Any, Error, ValidationError, WebPushSubscription]]:
    r""" Subscribe to push notifications

     Add a Web Push API subscription to receive notifications. Each access token can have one push
    subscription. If you create a new subscription, the old subscription is deleted.

    Version history:

    2.4.0 - added\
    3.3.0 - added `data[alerts][status]`\
    3.4.0 - added `data[policy]`\
    3.5.0 - added `data[alerts][update]` and `data[alerts][admin.sign_up]`\
    4.0.0 - added `data[alerts][admin.report]`\
    4.3.0 - added stricter request parameter validation, invalid endpoint URLs and subscription keys
    will now result in an error, previously these would be accepted, but silently fail.\
    4.4.0 - added `subscription[standard]`

    Args:
        body (CreatePushSubscriptionBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, Error, ValidationError, WebPushSubscription]]
     """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    body: CreatePushSubscriptionBody,
) -> Optional[Union[Any, Error, ValidationError, WebPushSubscription]]:
    r""" Subscribe to push notifications

     Add a Web Push API subscription to receive notifications. Each access token can have one push
    subscription. If you create a new subscription, the old subscription is deleted.

    Version history:

    2.4.0 - added\
    3.3.0 - added `data[alerts][status]`\
    3.4.0 - added `data[policy]`\
    3.5.0 - added `data[alerts][update]` and `data[alerts][admin.sign_up]`\
    4.0.0 - added `data[alerts][admin.report]`\
    4.3.0 - added stricter request parameter validation, invalid endpoint URLs and subscription keys
    will now result in an error, previously these would be accepted, but silently fail.\
    4.4.0 - added `subscription[standard]`

    Args:
        body (CreatePushSubscriptionBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, Error, ValidationError, WebPushSubscription]
     """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
