from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...types import UNSET, Response


def _get_kwargs(
    *,
    source_address_id: UUID,
    target_address_id: UUID,
) -> Dict[str, Any]:
    params: Dict[str, Any] = {}

    json_source_address_id = str(source_address_id)
    params["source_address_id"] = json_source_address_id

    json_target_address_id = str(target_address_id)
    params["target_address_id"] = json_target_address_id

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": "/api/v1/math/distance",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[HTTPValidationError, float]]:
    if response.status_code == 200:
        response_200 = cast(float, response.json())
        return response_200
    if response.status_code == 422:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[HTTPValidationError, float]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    source_address_id: UUID,
    target_address_id: UUID,
) -> Response[Union[HTTPValidationError, float]]:
    """Get Distance

     Получить расстояние между двумя адресами.

    Args:
        source_address_id (UUID):
        target_address_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, float]]
    """

    kwargs = _get_kwargs(
        source_address_id=source_address_id,
        target_address_id=target_address_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    source_address_id: UUID,
    target_address_id: UUID,
) -> Optional[Union[HTTPValidationError, float]]:
    """Get Distance

     Получить расстояние между двумя адресами.

    Args:
        source_address_id (UUID):
        target_address_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, float]
    """

    return sync_detailed(
        client=client,
        source_address_id=source_address_id,
        target_address_id=target_address_id,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    source_address_id: UUID,
    target_address_id: UUID,
) -> Response[Union[HTTPValidationError, float]]:
    """Get Distance

     Получить расстояние между двумя адресами.

    Args:
        source_address_id (UUID):
        target_address_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, float]]
    """

    kwargs = _get_kwargs(
        source_address_id=source_address_id,
        target_address_id=target_address_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    source_address_id: UUID,
    target_address_id: UUID,
) -> Optional[Union[HTTPValidationError, float]]:
    """Get Distance

     Получить расстояние между двумя адресами.

    Args:
        source_address_id (UUID):
        target_address_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, float]
    """

    return (
        await asyncio_detailed(
            client=client,
            source_address_id=source_address_id,
            target_address_id=target_address_id,
        )
    ).parsed
