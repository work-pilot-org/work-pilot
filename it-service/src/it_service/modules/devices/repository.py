from uuid import UUID

from sqlalchemy import asc, desc, or_, select
from sqlalchemy.orm import Session

from it_service.modules.devices.enums import DeviceStatus
from it_service.modules.devices.models import Device, DeviceMaintenanceHistory


class DeviceRepository:
    def create(self, db: Session, device: Device) -> Device:
        db.add(device)
        db.commit()
        db.refresh(device)
        return device

    def get_by_id(self, db: Session, device_id: UUID) -> Device | None:
        statement = select(Device).where(Device.id == device_id)
        return db.scalar(statement)

    def list(
        self,
        db: Session,
        *,
        status: DeviceStatus | None = None,
        assigned_to: UUID | None = None,
        search: str | None = None,
        skip: int = 0,
        limit: int = 20,
        descending: bool = True,
    ) -> list[Device]:
        statement = select(Device)

        if status:
            statement = statement.where(Device.status == status)
        if assigned_to:
            statement = statement.where(Device.assigned_to == assigned_to)
        if search:
            statement = statement.where(
                or_(
                    Device.name.ilike(f"%{search}%"),
                    Device.model.ilike(f"%{search}%"),
                )
            )

        if descending:
            statement = statement.order_by(desc(Device.created_at))
        else:
            statement = statement.order_by(asc(Device.created_at))

        statement = statement.offset(skip).limit(limit)
        return list(db.scalars(statement).all())

    def save(self, db: Session, device: Device) -> Device:
        db.commit()
        db.refresh(device)
        return device

    def delete(self, db: Session, device: Device) -> None:
        db.delete(device)
        db.commit()


class DeviceMaintenanceHistoryRepository:
    def create(
        self, db: Session, history: DeviceMaintenanceHistory
    ) -> DeviceMaintenanceHistory:
        db.add(history)
        db.commit()
        db.refresh(history)
        return history

    def list_by_device(
        self, db: Session, device_id: UUID
    ) -> list[DeviceMaintenanceHistory]:
        statement = (
            select(DeviceMaintenanceHistory)
            .where(DeviceMaintenanceHistory.device_id == device_id)
            .order_by(desc(DeviceMaintenanceHistory.maintenance_date))
        )
        return list(db.scalars(statement).all())