import uuid

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from it_service.modules.assets.enums import AssetStatus
from it_service.modules.assets.models import Asset
from it_service.modules.assets.repository import AssetRepository
from it_service.modules.assets.schemas import (
    AssignAssetRequest,
    CreateAssetRequest,
    UpdateAssetRequest,
)


class AssetService:
    def __init__(self, repository: AssetRepository):
        self.repository = repository

    def _get_asset(self, db: Session, asset_id: uuid.UUID) -> Asset:
        asset = self.repository.get_by_id(db, asset_id)
        if not asset:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Asset not found.",
            )
        return asset

    def create_asset(self, db: Session, payload: CreateAssetRequest) -> Asset:
        existing = self.repository.get_by_serial_number(db, payload.serial_number)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Asset with this serial number already exists.",
            )
        asset = Asset(
            name=payload.name,
            serial_number=payload.serial_number,
            category=payload.category,
            status=payload.status,
        )
        return self.repository.create(db, asset)

    def get_asset(self, db: Session, asset_id: uuid.UUID) -> Asset:
        return self._get_asset(db, asset_id)

    def list_assets(self, db: Session, **filters) -> list[Asset]:
        return self.repository.list(db, **filters)

    def update_asset(self, db: Session, asset_id: uuid.UUID, payload: UpdateAssetRequest) -> Asset:
        asset = self._get_asset(db, asset_id)
        
        if payload.serial_number and payload.serial_number != asset.serial_number:
            existing = self.repository.get_by_serial_number(db, payload.serial_number)
            if existing:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Asset with this serial number already exists.",
                )

        updates = payload.model_dump(exclude_unset=True)
        for field, value in updates.items():
            setattr(asset, field, value)

        return self.repository.save(db, asset)

    def assign_asset(self, db: Session, asset_id: uuid.UUID, payload: AssignAssetRequest) -> Asset:
        asset = self._get_asset(db, asset_id)
        if asset.status != AssetStatus.AVAILABLE:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Asset is not available for assignment. Current status: {asset.status.value}",
            )
        asset.assigned_to = payload.assigned_to
        asset.status = AssetStatus.ASSIGNED
        return self.repository.save(db, asset)

    def return_asset(self, db: Session, asset_id: uuid.UUID) -> Asset:
        asset = self._get_asset(db, asset_id)
        if asset.status != AssetStatus.ASSIGNED:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Asset is not currently assigned. Current status: {asset.status.value}",
            )
        asset.assigned_to = None
        asset.status = AssetStatus.AVAILABLE
        return self.repository.save(db, asset)

    def delete_asset(self, db: Session, asset_id: uuid.UUID) -> None:
        asset = self._get_asset(db, asset_id)
        self.repository.delete(db, asset)