import httpx
from typing import Optional, Dict, Any

class BaseClient:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip('/')

    def _get_headers(self, token: Optional[str] = None) -> Dict[str, str]:
        headers = {"Content-Type": "application/json"}
        if token:
            headers["Authorization"] = f"Bearer {token}"
        return headers

    async def _request(
        self, 
        method: str, 
        endpoint: str, 
        token: Optional[str] = None, 
        **kwargs
    ) -> Any:
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        headers = self._get_headers(token)
        
        if "headers" in kwargs:
            headers.update(kwargs.pop("headers"))

        async with httpx.AsyncClient() as client:
            response = await client.request(method, url, headers=headers, **kwargs)
            response.raise_for_status()
            
            # Return JSON if possible, else the raw text
            if response.headers.get("content-type", "").startswith("application/json"):
                return response.json()
            return response.text

    async def get(self, endpoint: str, token: Optional[str] = None, **kwargs) -> Any:
        return await self._request("GET", endpoint, token, **kwargs)

    async def post(self, endpoint: str, token: Optional[str] = None, **kwargs) -> Any:
        return await self._request("POST", endpoint, token, **kwargs)

    async def put(self, endpoint: str, token: Optional[str] = None, **kwargs) -> Any:
        return await self._request("PUT", endpoint, token, **kwargs)

    async def delete(self, endpoint: str, token: Optional[str] = None, **kwargs) -> Any:
        return await self._request("DELETE", endpoint, token, **kwargs)
