"""
Shared HTTP client provider for the AI Service.

This module manages a single AsyncClient instance that is reused
across all service clients.
"""

from __future__ import annotations

import httpx


class HTTPClientProvider:
    """
    Manages the lifecycle of a shared httpx.AsyncClient.
    """

    def __init__(self) -> None:
        self._client: httpx.AsyncClient | None = None

    async def startup(self) -> None:
        """
        Create the shared AsyncClient.
        """
        self._client = httpx.AsyncClient(
            timeout=httpx.Timeout(30.0),
            follow_redirects=True,
        )

    async def shutdown(self) -> None:
        """
        Close the shared AsyncClient.
        """
        if self._client is not None:
            await self._client.aclose()
            self._client = None

    @property
    def client(self) -> httpx.AsyncClient:
        """
        Return the shared AsyncClient instance.
        """
        if self._client is None:
            raise RuntimeError(
                "HTTP client has not been initialized. "
                "Call startup() before accessing the client."
            )

        return self._client


http_client_provider = HTTPClientProvider()