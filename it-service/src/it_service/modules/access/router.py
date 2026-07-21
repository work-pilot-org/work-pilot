import uuid

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from it_service.infrastructure.database.session import get_db
from it_service.modules.access.enums import AccessRequestStatus, AccessRequestType
from it_service.modules.access.repository import AccessRequestRepository
from it_service.modules.access.schemas import (
    AccessRequestResponse,
    CreateAccessRequest,
    UpdateAccessRequest,
)
from it_service.modules.access.service import AccessService

router = APIRouter(
    prefix="/access",
    tags=["Access"],
)


def get_access_service() -> AccessService:
    return AccessService(repository=AccessRequestRepository())


@router.post("", response_model=AccessRequestResponse, status_code=status.HTTP_201_CREATED)
def create_request(
    payload: CreateAccessRequest,
    db: Session = Depends(get_db),
    service: AccessService = Depends(get_access_service),
):
    return service.create_request(db, payload)


@router.get("", response_model=list[AccessRequestResponse])
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


@router.get("/{request_id}", response_model=AccessRequestResponse)
def get_request(
    request_id: uuid.UUID,
    db: Session = Depends(get_db),
    service: AccessService = Depends(get_access_service),
):
    return service.get_request(db, request_id)


@router.put("/{request_id}", response_model=AccessRequestResponse)
def update_request(
    request_id: uuid.UUID,
    payload: UpdateAccessRequest,
    db: Session = Depends(get_db),
    service: AccessService = Depends(get_access_service),
):
    return service.update_request(db, request_id, payload)


@router.delete("/{request_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_request(
    request_id: uuid.UUID,
    db: Session = Depends(get_db),
    service: AccessService = Depends(get_access_service),
):
    service.delete_request(db, request_id)