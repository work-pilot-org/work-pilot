from uuid import UUID

from sqlalchemy import asc, desc, or_, select
from sqlalchemy.orm import Session

from it_service.modules.assets.enums import AssetCategory, AssetStatus
from it_service.modules.assets.models import Asset


class AssetRepository:
    def create(self, db: Session, asset: Asset) -> Asset:
        db.add(asset)
        db.commit()
        db.refresh(asset)
        return asset

    def get_by_id(self, db: Session, asset_id: UUID) -> Asset | None:
        statement = select(Asset).where(Asset.id == asset_id)
        return db.scalar(statement)

    def get_by_serial_number(self, db: Session, serial_number: str) -> Asset | None:
        statement = select(Asset).where(Asset.serial_number == serial_number)
        return db.scalar(statement)

    def list(
        self,
        db: Session,
        *,
        category: AssetCategory | None = None,
        status: AssetStatus | None = None,
        assigned_to: UUID | None = None,
        search: str | None = None,
        skip: int = 0,
        limit: int = 20,
        descending: bool = True,
    ) -> list[Asset]:
        statement = select(Asset)

        if category:
            statement = statement.where(Asset.category == category)
        if status:
            statement = statement.where(Asset.status == status)
        if assigned_to:
            statement = statement.where(Asset.assigned_to == assigned_to)
        if search:
            statement = statement.where(
                or_(
                    Asset.name.ilike(f"%{search}%"),
                    Asset.serial_number.ilike(f"%{search}%"),
                )
            )

        if descending:
            statement = statement.order_by(desc(Asset.created_at))
        else:
            statement = statement.order_by(asc(Asset.created_at))

        statement = statement.offset(skip).limit(limit)
        return list(db.scalars(statement).all())

    def save(self, db: Session, asset: Asset) -> Asset:
        db.commit()
        db.refresh(asset)
        return asset

    def delete(self, db: Session, asset: Asset) -> None:
        db.delete(asset)
        db.commit()