from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from notification_service.modules.notifications.schemas import (
    NotificationCreate,
    NotificationResponse,
)
from notification_service.modules.notifications.service import NotificationService
from shared_infrastructure.core.dependencies import (
    get_current_user_and_set_schema,
)
from shared_infrastructure.database.session import get_db


router = APIRouter(
    prefix="/notifications",
    tags=["Notifications"],
)


def get_notification_service() -> NotificationService:
    return NotificationService()


@router.post(
    "",
    response_model=NotificationResponse,
    status_code=status.HTTP_201_CREATED,
)
def send_notification(
    notification: NotificationCreate,
    current_user: dict = Depends(get_current_user_and_set_schema),
    db: Session = Depends(get_db),
    notification_service: NotificationService = Depends(
        get_notification_service
    ),
) -> NotificationResponse:
    """
    Create and deliver a notification.

    Tenant identity comes exclusively from the validated JWT.
    The request body cannot provide or override tenant_id.
    """

    tenant_id = current_user.get("tenant_id")

    if not tenant_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Tenant ID is missing from credentials.",
        )

    try:
        return notification_service.send_notification(
            db=db,
            notification=notification,
            tenant_id=str(tenant_id),
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc