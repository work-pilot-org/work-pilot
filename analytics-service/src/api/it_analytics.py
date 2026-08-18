from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from shared_infrastructure.database.session import get_db
from shared_infrastructure.core.dependencies import get_current_user_and_set_schema
from src.models.facts import FactITTicket, FactAssetAssignment
from src.models.dimensions import DimAsset, DimEmployee

router = APIRouter(
    prefix="/analytics/it",
    tags=["IT Analytics"],
    dependencies=[Depends(get_current_user_and_set_schema)],
)

@router.get("/ticket-summary")
def get_ticket_summary(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user_and_set_schema),
    period: str = None,
    category: str = None,
):
    """
    Returns aggregated IT ticket data (e.g. counts by status, priority) scoped to the current tenant.
    """
    
    query = db.query(
        FactITTicket.ticket_status,
        FactITTicket.ticket_priority,
        func.count(FactITTicket.id).label("total_tickets")
    )
    
    if category:
        query = query.filter(FactITTicket.ticket_category == category)
        
    summary = query.group_by(FactITTicket.ticket_status, FactITTicket.ticket_priority).all()
    
    return {
        "tenant_id": current_user.get("schema_name"),
        "summary": [
            {
                "status": row.ticket_status,
                "priority": row.ticket_priority,
                "tickets": row.total_tickets
            }
            for row in summary
        ]
    }

@router.get("/asset-assignments")
def get_asset_assignments(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user_and_set_schema),
    status: str = None,
    category: str = None,
):
    """
    Returns asset assignment analytics (current active assignments and historical assignment stats).
    """
    
    query = db.query(
        FactAssetAssignment.assignment_id,
        FactAssetAssignment.assignment_status,
        FactAssetAssignment.assigned_at,
        FactAssetAssignment.returned_at,
        FactAssetAssignment.assignment_duration_days,
        DimAsset.name.label("asset_name"),
        DimAsset.category.label("asset_category"),
        DimAsset.status.label("current_asset_status"),
        DimEmployee.name.label("employee_name"),
        DimEmployee.email.label("employee_email"),
    ).join(
        DimAsset, FactAssetAssignment.asset_key == DimAsset.id
    ).outerjoin(
        DimEmployee, FactAssetAssignment.employee_key == DimEmployee.id
    )
    
    if status:
        query = query.filter(FactAssetAssignment.assignment_status == status.upper())
        
    if category:
        query = query.filter(DimAsset.category == category)
        
    results = query.all()
    
    return {
        "tenant_id": current_user.get("schema_name"),
        "assignments": [
            {
                "assignment_id": str(row.assignment_id),
                "status": row.assignment_status,
                "assigned_at": row.assigned_at,
                "returned_at": row.returned_at,
                "duration_days": row.assignment_duration_days,
                "asset_name": row.asset_name,
                "asset_category": row.asset_category,
                "asset_current_status": row.current_asset_status,
                "employee_name": row.employee_name,
                "employee_email": row.employee_email
            }
            for row in results
        ]
    }
