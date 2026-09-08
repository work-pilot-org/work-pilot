import uuid

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from shared_infrastructure.core.security import get_current_user
from shared_infrastructure.core.rbac import Permission

from shared_infrastructure.core.dependencies import require_permissions, verify_access_request_ownership
from shared_infrastructure.database.session import get_db
from it_service.modules.access.enums import AccessRequestStatus, AccessRequestType
from it_service.modules.access.repository import AccessRequestRepository
from it_service.modules.access.schemas import (
    AccessRequestResponse,
    AccessRequestStatusUpdate,
    CreateAccessRequest,
    UpdateAccessRequest,
)
from it_service.modules.access.service import AccessService

router = APIRouter(
    prefix="/access",
    tags=["Access"],
    dependencies=[Depends(get_current_user)],
)


def get_access_service() -> AccessService:
    return AccessService(repository=AccessRequestRepository())


@router.post("", response_model=AccessRequestResponse, status_code=status.HTTP_201_CREATED)
def create_request(
    payload: CreateAccessRequest,
    db: Session = Depends(get_db),
    service: AccessService = Depends(get_access_service),
    current_user: dict = Depends(get_current_user),
):
    from shared_infrastructure.core.rbac import Permission, get_permissions_for_roles
    roles = current_user.get("roles", [])
    user_perms = get_permissions_for_roles(roles)
    if Permission.ADMIN_ALL not in user_perms and Permission.IT_MANAGE not in user_perms:
        payload.requested_by = uuid.UUID(current_user.get("sub"))
    return service.create_request(db, payload)


@router.get("", response_model=list[AccessRequestResponse], dependencies=[Depends(require_permissions([Permission.IT_MANAGE]))])
def list_requests(
    request_type: AccessRequestType | None = Query(None),
    status: AccessRequestStatus | None = Query(None),
    requested_by: uuid.UUID | None = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    service: AccessService = Depends(get_access_service),
):
    return service.list_requests(
        db,
        request_type=request_type,
        status=status,
        requested_by=requested_by,
        skip=skip,
        limit=limit,
    )

@router.get("/my", response_model=list[AccessRequestResponse])
def list_my_requests(
    request_type: AccessRequestType | None = Query(None),
    status: AccessRequestStatus | None = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    service: AccessService = Depends(get_access_service),
    current_user: dict = Depends(get_current_user),
):
    requested_by = uuid.UUID(current_user.get("sub"))
    return service.list_requests(
        db,
        request_type=request_type,
        status=status,
        requested_by=requested_by,
        skip=skip,
        limit=limit,
    )


@router.get("/{request_id}", response_model=AccessRequestResponse)
def get_request(
    request_id: uuid.UUID,
    db: Session = Depends(get_db),
    service: AccessService = Depends(get_access_service),
    current_user: dict = Depends(get_current_user),
):
    verify_access_request_ownership(request_id, current_user, db, bypass_permissions=[Permission.IT_MANAGE])
    return service.get_request(db, request_id)


@router.put("/{request_id}", response_model=AccessRequestResponse, dependencies=[Depends(require_permissions([Permission.IT_MANAGE]))])
def update_request(
    request_id: uuid.UUID,
    payload: UpdateAccessRequest,
    db: Session = Depends(get_db),
    service: AccessService = Depends(get_access_service),
):
    return service.update_request(db, request_id, payload)


@router.patch("/{request_id}/status", response_model=AccessRequestResponse, dependencies=[Depends(require_permissions([Permission.IT_MANAGE]))])
def update_request_status(
    request_id: uuid.UUID,
    payload: AccessRequestStatusUpdate,
    db: Session = Depends(get_db),
    service: AccessService = Depends(get_access_service),
):
    return service.update_request_status(db, request_id, payload.status)


@router.delete("/{request_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(require_permissions([Permission.IT_MANAGE]))])
def delete_request(
    request_id: uuid.UUID,
    db: Session = Depends(get_db),
    service: AccessService = Depends(get_access_service),
):
    service.delete_request(db, request_id)