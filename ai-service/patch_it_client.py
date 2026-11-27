import re
import os

CLIENT_PATH = r"d:\work-pilot-clone\ai-service\src\infrastructure\integrations\it_client.py"

with open(CLIENT_PATH, 'r') as f:
    content = f.read()

# Add list_my_tickets after list_tickets
if "async def list_my_tickets" not in content:
    ticket_replacement = """        return await self._client.get(
            f"{self._base_url}/tickets",
            headers=headers,
        )

    async def list_my_tickets(
        self,
        headers: dict[str, str] | None = None,
    ) -> Any:
        return await self._client.get(
            f"{self._base_url}/tickets/my",
            headers=headers,
        )"""
    content = re.sub(
        r'        return await self\._client\.get\(\s*f"\{self\._base_url\}/tickets",\s*headers=headers,\s*\)',
        ticket_replacement,
        content
    )

# Add list_my_access_requests after list_access_requests
if "async def list_my_access_requests" not in content:
    access_replacement = """        return await self._client.get(
            f"{self._base_url}/access",
            headers=headers,
        )

    async def list_my_access_requests(
        self,
        headers: dict[str, str] | None = None,
    ) -> Any:
        return await self._client.get(
            f"{self._base_url}/access/my",
            headers=headers,
        )"""
    content = re.sub(
        r'        return await self\._client\.get\(\s*f"\{self\._base_url\}/access",\s*headers=headers,\s*\)',
        access_replacement,
        content
    )

with open(CLIENT_PATH, 'w') as f:
    f.write(content)
print("it_client.py updated")
