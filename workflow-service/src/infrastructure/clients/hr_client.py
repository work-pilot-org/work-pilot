from typing import Optional, Any
from uuid import UUID

from src.core.config import settings
from src.infrastructure.clients.base_client import BaseClient

class HRClient(BaseClient):
    def __init__(self):
        super().__init__(base_url=settings.HR_SERVICE_URL)

    async def get_employee_details(self, employee_id: UUID, token: Optional[str] = None) -> Any:
        """
        Fetch details for a specific employee from the HR Service.
        """
        return await self.get(f"/employees/{employee_id}", token=token)

hr_client = HRClient()
