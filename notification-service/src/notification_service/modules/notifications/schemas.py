from pydantic import BaseModel, EmailStr, Field

from notification_service.modules.notifications.enums import (
    Channel,
    NotificationType,
)


class NotificationCreate(BaseModel):
    recipient_id: str
    recipient_email: EmailStr
    channel: Channel = Channel.EMAIL
    notification_type: NotificationType
    subject: str = Field(min_length=1, max_length=255)
    body: str = Field(min_length=1)


class NotificationResponse(BaseModel):
    id: str
    recipient_id: str
    channel: Channel
    notification_type: NotificationType
    subject: str
    status: str
    created_at: str
    sent_at: str | None = None