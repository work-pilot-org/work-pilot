from typing import Optional, Any
from uuid import UUID

from src.core.config import settings
from src.infrastructure.clients.base_client import BaseClient

class NotificationClient(BaseClient):
    def __init__(self):
        super().__init__(base_url=settings.NOTIFICATION_SERVICE_URL if hasattr(settings, "NOTIFICATION_SERVICE_URL") else "http://notification-service:8000")

    async def send_notification(self, user_id: str, message: str, token: Optional[str] = None) -> Any:
        """
        Send a notification to a user.
        """
        payload = {
            "user_id": user_id,
            "message": message,
            "type": "WORKFLOW_APPROVAL"
        }
        return await self.post("/api/v1/notifications", json=payload, token=token)

notification_client = NotificationClient()
