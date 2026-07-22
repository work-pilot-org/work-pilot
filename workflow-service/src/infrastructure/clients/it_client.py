from typing import Optional, Any
from uuid import UUID

from src.core.config import settings
from src.infrastructure.clients.base_client import BaseClient

class ITClient(BaseClient):
    def __init__(self):
        super().__init__(base_url=settings.IT_SERVICE_URL)

    async def get_user_equipment(self, user_id: UUID, token: Optional[str] = None) -> Any:
        """
        Fetch equipment assigned to a specific user from the IT Service.
        """
        return await self.get(f"/api/v1/equipment/user/{user_id}", token=token)

it_client = ITClient()
