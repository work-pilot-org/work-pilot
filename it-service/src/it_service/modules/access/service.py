import uuid

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from it_service.modules.access.enums import AccessRequestStatus
from it_service.modules.access.models import AccessRequest
from it_service.modules.access.repository import AccessRequestRepository
from it_service.modules.access.schemas import (
    CreateAccessRequest,
    UpdateAccessRequest,
)


class AccessService:
    def __init__(self, repository: AccessRequestRepository):
        self.repository = repository

    def _get_request(self, db: Session, request_id: uuid.UUID) -> AccessRequest:
        request = self.repository.get_by_id(db, request_id)
        if not request:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Access request not found.",
            )
        return request

    def create_request(self, db: Session, payload: CreateAccessRequest) -> AccessRequest:
        request = AccessRequest(
            request_type=payload.request_type,
            target_resource=payload.target_resource,
            requested_by=payload.requested_by,
            reason=payload.reason,
            status=AccessRequestStatus.PENDING,
        )
        return self.repository.create(db, request)

    def get_request(self, db: Session, request_id: uuid.UUID) -> AccessRequest:
        return self._get_request(db, request_id)

    def list_requests(self, db: Session, **filters) -> list[AccessRequest]:
        return self.repository.list(db, **filters)

    def update_request(
        self, db: Session, request_id: uuid.UUID, payload: UpdateAccessRequest
    ) -> AccessRequest:
        request = self._get_request(db, request_id)
        if request.status != AccessRequestStatus.PENDING:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Cannot update request with status: {request.status.value}",
            )
        
        updates = payload.model_dump(exclude_unset=True)
        for field, value in updates.items():
            setattr(request, field, value)
            
        return self.repository.save(db, request)


    def delete_request(self, db: Session, request_id: uuid.UUID) -> None:
        request = self._get_request(db, request_id)
        self.repository.delete(db, request)