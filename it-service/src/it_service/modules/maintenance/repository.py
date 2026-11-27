from uuid import UUID

from sqlalchemy import desc, select
from sqlalchemy.orm import Session

from it_service.modules.maintenance.enums import MaintenanceStatus, MaintenanceType
from it_service.modules.maintenance.models import MaintenanceRecord


class MaintenanceRepository:
    def create(self, db: Session, record: MaintenanceRecord) -> MaintenanceRecord:
        db.add(record)
        db.commit()
        db.refresh(record)
        return record

    def get_by_id(self, db: Session, record_id: UUID) -> MaintenanceRecord | None:
        statement = select(MaintenanceRecord).where(MaintenanceRecord.id == record_id)
        return db.scalar(statement)

    def list(
        self,
        db: Session,
        *,
        device_id: UUID | None = None,
        maintenance_type: MaintenanceType | None = None,
        status: MaintenanceStatus | None = None,
        skip: int = 0,
        limit: int = 20,
    ) -> list[MaintenanceRecord]:
        statement = select(MaintenanceRecord)

        if device_id:
            statement = statement.where(MaintenanceRecord.device_id == device_id)
        if maintenance_type:
            statement = statement.where(MaintenanceRecord.maintenance_type == maintenance_type)
        if status:
            statement = statement.where(MaintenanceRecord.status == status)

        statement = (
            statement.order_by(desc(MaintenanceRecord.scheduled_date))
            .offset(skip)
            .limit(limit)
        )
        return list(db.scalars(statement).all())

    def save(self, db: Session, record: MaintenanceRecord) -> MaintenanceRecord:
        db.commit()
        db.refresh(record)
        return record

    def delete(self, db: Session, record: MaintenanceRecord) -> None:
        db.delete(record)
        db.commit()