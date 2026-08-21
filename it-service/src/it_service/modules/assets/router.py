import uuid

from shared_infrastructure.core.security import get_current_user
from fastapi import APIRouter, Depends, Query, status, BackgroundTasks
from sqlalchemy.orm import Session

from shared_infrastructure.core.dependencies import require_permissions
from shared_infrastructure.core.rbac import Permission
from shared_infrastructure.database.session import get_db
from shared_infrastructure.publisher import publish_event
from shared_infrastructure.events import EventEnvelope

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
    dependencies=[
        Depends(get_current_user),
        Depends(require_permissions([Permission.ASSETS_MANAGE]))
    ],
)


def get_asset_service() -> AssetService:
    return AssetService(repository=AssetRepository())


@router.post("", response_model=AssetResponse, status_code=status.HTTP_201_CREATED)
def create_asset(
    payload: CreateAssetRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    service: AssetService = Depends(get_asset_service),
    current_user: dict = Depends(get_current_user),
):
    asset = service.create_asset(db, payload)
    
    event = EventEnvelope[dict](
        event_type="it.asset.created",
        tenant_id=current_user["tenant_id"],
        source="it-service",
        payload={
            "asset_id": str(asset.id),
            "category": asset.category.value,
            "status": asset.status.value,
            "name": asset.name,
        }
    )
    background_tasks.add_task(publish_event, "it.asset", event)
    
    return asset


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
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    service: AssetService = Depends(get_asset_service),
    current_user: dict = Depends(get_current_user),
):
    asset = service.update_asset(db, asset_id, payload)
    
    event = EventEnvelope[dict](
        event_type="it.asset.updated",
        tenant_id=current_user["tenant_id"],
        source="it-service",
        payload={
            "asset_id": str(asset.id),
            "category": asset.category.value,
            "status": asset.status.value,
            "name": asset.name,
        }
    )
    background_tasks.add_task(publish_event, "it.asset", event)
    
    return asset


@router.post("/{asset_id}/assign", response_model=AssetResponse)
def assign_asset(
    asset_id: uuid.UUID,
    payload: AssignAssetRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    service: AssetService = Depends(get_asset_service),
    current_user: dict = Depends(get_current_user),
):
    asset = service.assign_asset(db, asset_id, payload)
    
    event = EventEnvelope[dict](
        event_type="it.asset.assigned",
        tenant_id=current_user["tenant_id"],
        source="it-service",
        payload={
            "asset_id": str(asset.id),
            "employee_id": str(asset.assigned_to),
            "assignment_id": str(asset.assignment_id),
        }
    )
    background_tasks.add_task(publish_event, "it.asset", event)
    
    return asset


@router.post("/{asset_id}/return", response_model=AssetResponse)
def return_asset(
    asset_id: uuid.UUID,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    service: AssetService = Depends(get_asset_service),
    current_user: dict = Depends(get_current_user),
):
    # Retrieve the assignment_id BEFORE returning, so we can emit it.
    asset_before = service.get_asset(db, asset_id)
    assignment_id = str(asset_before.assignment_id) if asset_before.assignment_id else None
    employee_id = str(asset_before.assigned_to) if asset_before.assigned_to else None
    
    asset = service.return_asset(db, asset_id)
    
    if assignment_id:
        event = EventEnvelope[dict](
            event_type="it.asset.returned",
            tenant_id=current_user["tenant_id"],
            source="it-service",
            payload={
                "asset_id": str(asset.id),
                "employee_id": employee_id,
                "assignment_id": assignment_id,
            }
        )
        background_tasks.add_task(publish_event, "it.asset", event)
        
    return asset


@router.delete("/{asset_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_asset(
    asset_id: uuid.UUID,
    db: Session = Depends(get_db),
    service: AssetService = Depends(get_asset_service),
):
    service.delete_asset(db, asset_id)