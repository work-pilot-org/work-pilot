import uuid

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from it_service.infrastructure.database.session import get_db
from it_service.modules.assets.enums import AssetCategory, AssetStatus
from it_service.modules.assets.repository import AssetRepository
from it_service.modules.assets.schemas import (
    AssetResponse,
    AssignAssetRequest,
    CreateAssetRequest,
    UpdateAssetRequest,
)
from it_service.modules.assets.service import AssetService

router = APIRouter(
    prefix="/assets",
    tags=["Assets"],
)


def get_asset_service() -> AssetService:
    return AssetService(repository=AssetRepository())


@router.post("", response_model=AssetResponse, status_code=status.HTTP_201_CREATED)
def create_asset(
    payload: CreateAssetRequest,
    db: Session = Depends(get_db),
    service: AssetService = Depends(get_asset_service),
):
    return service.create_asset(db, payload)


@router.get("", response_model=list[AssetResponse])
def list_assets(
    category: AssetCategory | None = Query(None),
    status: AssetStatus | None = Query(None),
    assigned_to: uuid.UUID | None = Query(None),
    search: str | None = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    service: AssetService = Depends(get_asset_service),
):
    return service.list_assets(
        db,
        category=category,
        status=status,
        assigned_to=assigned_to,
        search=search,
        skip=skip,
        limit=limit,
    )


@router.get("/{asset_id}", response_model=AssetResponse)
def get_asset(
    asset_id: uuid.UUID,
    db: Session = Depends(get_db),
    service: AssetService = Depends(get_asset_service),
):
    return service.get_asset(db, asset_id)


@router.put("/{asset_id}", response_model=AssetResponse)
def update_asset(
    asset_id: uuid.UUID,
    payload: UpdateAssetRequest,
    db: Session = Depends(get_db),
    service: AssetService = Depends(get_asset_service),
):
    return service.update_asset(db, asset_id, payload)


@router.post("/{asset_id}/assign", response_model=AssetResponse)
def assign_asset(
    asset_id: uuid.UUID,
    payload: AssignAssetRequest,
    db: Session = Depends(get_db),
    service: AssetService = Depends(get_asset_service),
):
    return service.assign_asset(db, asset_id, payload)


@router.post("/{asset_id}/return", response_model=AssetResponse)
def return_asset(
    asset_id: uuid.UUID,
    db: Session = Depends(get_db),
    service: AssetService = Depends(get_asset_service),
):
    return service.return_asset(db, asset_id)


@router.delete("/{asset_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_asset(
    asset_id: uuid.UUID,
    db: Session = Depends(get_db),
    service: AssetService = Depends(get_asset_service),
):
    service.delete_asset(db, asset_id)