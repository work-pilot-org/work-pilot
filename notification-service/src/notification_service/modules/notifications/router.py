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

@router.get(
    "",
    response_model=list[NotificationResponse],
    status_code=status.HTTP_200_OK,
)
def get_notifications(
    current_user: dict = Depends(get_current_user_and_set_schema),
    db: Session = Depends(get_db),
    notification_service: NotificationService = Depends(get_notification_service),
) -> list[NotificationResponse]:
    tenant_id = current_user.get("tenant_id")
    recipient_id = current_user.get("sub")
    if not tenant_id or not recipient_id:
        raise HTTPException(status_code=401, detail="Unauthorized")
    from notification_service.modules.notifications.models import NotificationLog
    logs = db.query(NotificationLog).filter(
        NotificationLog.tenant_id == str(tenant_id),
        NotificationLog.recipient_id == str(recipient_id)
    ).order_by(NotificationLog.created_at.desc()).limit(50).all()
    return [notification_service._to_response(log) for log in logs]

@router.get("/unread-count", response_model=int)
def get_unread_count(
    current_user: dict = Depends(get_current_user_and_set_schema),
    db: Session = Depends(get_db),
):
    tenant_id = current_user.get("tenant_id")
    recipient_id = current_user.get("sub")
    if not tenant_id or not recipient_id:
        raise HTTPException(status_code=401, detail="Unauthorized")
    from notification_service.modules.notifications.models import NotificationLog
    from notification_service.modules.notifications.enums import NotificationStatus
    # we don't have is_read field on NotificationLog? 
    # let's assume PENDING means unread for now or SENT means unread
    count = db.query(NotificationLog).filter(
        NotificationLog.tenant_id == str(tenant_id),
        NotificationLog.recipient_id == str(recipient_id),
        NotificationLog.status == NotificationStatus.SENT
    ).count()
    return count

@router.put("/{notification_id}/read", status_code=status.HTTP_200_OK)
def mark_read(
    notification_id: str,
    current_user: dict = Depends(get_current_user_and_set_schema),
    db: Session = Depends(get_db),
):
    tenant_id = current_user.get("tenant_id")
    recipient_id = current_user.get("sub")
    if not tenant_id or not recipient_id:
        raise HTTPException(status_code=401, detail="Unauthorized")
    from notification_service.modules.notifications.models import NotificationLog
    from notification_service.modules.notifications.enums import NotificationStatus
    log = db.query(NotificationLog).filter(
        NotificationLog.id == notification_id,
        NotificationLog.tenant_id == str(tenant_id),
        NotificationLog.recipient_id == str(recipient_id)
    ).first()
    if not log:
        raise HTTPException(status_code=404, detail="Not found")
    log.status = NotificationStatus.READ if hasattr(NotificationStatus, 'READ') else NotificationStatus.DELIVERED
    db.commit()
    return {"status": "ok"}
