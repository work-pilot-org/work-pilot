from uuid import UUID

from sqlalchemy import desc, select
from sqlalchemy.orm import Session

from it_service.modules.access.enums import AccessRequestStatus, AccessRequestType
from it_service.modules.access.models import AccessRequest


class AccessRequestRepository:
    def create(self, db: Session, request: AccessRequest) -> AccessRequest:
        db.add(request)
        db.commit()
        db.refresh(request)
        return request

    def get_by_id(self, db: Session, request_id: UUID) -> AccessRequest | None:
        statement = select(AccessRequest).where(AccessRequest.id == request_id)
        return db.scalar(statement)

    def list(
        self,
        db: Session,
        *,
        request_type: AccessRequestType | None = None,
        status: AccessRequestStatus | None = None,
        requested_by: UUID | None = None,
        skip: int = 0,
        limit: int = 20,
    ) -> list[AccessRequest]:
        statement = select(AccessRequest)

        if request_type:
            statement = statement.where(AccessRequest.request_type == request_type)
        if status:
            statement = statement.where(AccessRequest.status == status)
        if requested_by:
            statement = statement.where(AccessRequest.requested_by == requested_by)

        statement = (
            statement.order_by(desc(AccessRequest.created_at))
            .offset(skip)
            .limit(limit)
        )
        return list(db.scalars(statement).all())

    def save(self, db: Session, request: AccessRequest) -> AccessRequest:
        db.commit()
        db.refresh(request)
        return request

    def delete(self, db: Session, request: AccessRequest) -> None:
        db.delete(request)
        db.commit()