"""
Reusable HTTP client for communication with external microservices.
"""

from __future__ import annotations

from typing import Any

import httpx

from core.logger import get_logger
from infrastructure.exceptions import (
    AuthenticationError,
    AuthorizationError,
    BadRequestError,
    ConflictError,
    ExternalServiceError,
    RequestTimeoutError,
    ResourceNotFoundError,
    ServiceUnavailableError,
)
from infrastructure.providers.http_client import http_client_provider

logger = get_logger(__name__)


class BaseClient:
    """
    Base client responsible for communicating with external services.

    Service-specific clients (IT, HR, Workflow) should use this class
    instead of directly using httpx.AsyncClient.
    """

    async def get(
        self,
        url: str,
        headers: dict[str, str] | None = None,
        params: dict[str, Any] | None = None,
    ) -> Any:
        return await self._request(
            method="GET",
            url=url,
            headers=headers,
            params=params,
        )

    async def post(
        self,
        url: str,
        json: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
    ) -> Any:
        return await self._request(
            method="POST",
            url=url,
            json=json,
            headers=headers,
        )

    async def put(
        self,
        url: str,
        json: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
    ) -> Any:
        return await self._request(
            method="PUT",
            url=url,
            json=json,
            headers=headers,
        )

    async def patch(
        self,
        url: str,
        json: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
    ) -> Any:
        return await self._request(
            method="PATCH",
            url=url,
            json=json,
            headers=headers,
        )

    async def delete(
        self,
        url: str,
        headers: dict[str, str] | None = None,
    ) -> Any:
        return await self._request(
            method="DELETE",
            url=url,
            headers=headers,
        )

    async def _request(
        self,
        method: str,
        url: str,
        headers: dict[str, str] | None = None,
        params: dict[str, Any] | None = None,
        json: dict[str, Any] | None = None,
    ) -> Any:
        """
        Send an HTTP request using the shared AsyncClient.
        """

        client = http_client_provider.client

        logger.info(
            "Sending request",
            method=method,
            url=url,
        )

        try:
            response = await client.request(
                method=method,
                url=url,
                headers=headers,
                params=params,
                json=json,
            )

        except httpx.TimeoutException as exc:
            logger.error("Request timeout", url=url)
            raise RequestTimeoutError("Request timed out.") from exc

        except httpx.ConnectError as exc:
            logger.error("Unable to connect", url=url)
            raise ServiceUnavailableError(
                "Unable to connect to external service."
            ) from exc

        except httpx.HTTPError as exc:
            logger.error("HTTP error", url=url)
            raise ExternalServiceError(str(exc)) from exc

        self._handle_status_code(response)

        logger.info(
            "Request completed",
            method=method,
            url=url,
            status_code=response.status_code,
        )

        if response.status_code == 204:
            return None

        if response.content:
            return response.json()

        return None

    @staticmethod
    def _handle_status_code(response: httpx.Response) -> None:
        """
        Convert HTTP status codes into application exceptions.
        """

        match response.status_code:
            case status if 200 <= status < 300:
                return

            case 400:
                raise BadRequestError(response.text)

            case 401:
                raise AuthenticationError(response.text)

            case 403:
                raise AuthorizationError(response.text)

            case 404:
                raise ResourceNotFoundError(response.text)

            case 409:
                raise ConflictError(response.text)

            case 500 | 502 | 503 | 504:
                raise ServiceUnavailableError(response.text)

            case _:
                raise ExternalServiceError(response.text)