from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from shared_infrastructure.database.session import get_db
from shared_infrastructure.core.dependencies import get_current_user_and_set_schema
from src.models.facts import FactAttendance, FactLeave
from src.models.dimensions import DimEmployee

router = APIRouter(
    prefix="/analytics/hr",
    tags=["HR Analytics"],
    dependencies=[Depends(get_current_user_and_set_schema)],
)

@router.get("/attendance-summary")
def get_attendance_summary(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user_and_set_schema),
):
    """
    Returns aggregated attendance data (e.g. total worked hours) scoped to the current tenant.
    """
    
    summary = db.query(
        FactAttendance.attendance_status,
        func.sum(FactAttendance.worked_minutes).label("total_worked_minutes"),
        func.sum(FactAttendance.overtime_minutes).label("total_overtime_minutes"),
        func.count(FactAttendance.id).label("total_records")
    ).group_by(FactAttendance.attendance_status).all()
    
    return {
        "tenant_id": current_user.get("schema_name"),
        "summary": [
            {
                "status": row.attendance_status,
                "worked_hours": round((row.total_worked_minutes or 0) / 60, 2),
                "overtime_hours": round((row.total_overtime_minutes or 0) / 60, 2),
                "records": row.total_records
            }
            for row in summary
        ]
    }


@router.get("/leave-utilization")
def get_leave_utilization(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user_and_set_schema),
    period: str = None,
    department: str = None,
):
    """
    Returns aggregated leave utilization (e.g. total days requested, pending, approved) scoped to the current tenant.
    """
    
    query = db.query(
        FactLeave.leave_status,
        func.sum(FactLeave.leave_days_requested).label("total_days"),
        func.count(FactLeave.id).label("total_requests")
    )
    
    # We could add joins to DimDepartment or DimDate based on filters here
    # e.g., if department: query = query.join(DimDepartment).filter(DimDepartment.name == department)
    
    summary = query.group_by(FactLeave.leave_status).all()
    
    return {
        "tenant_id": current_user.get("schema_name"),
        "summary": [
            {
                "status": row.leave_status,
                "total_days": row.total_days or 0,
                "requests": row.total_requests
            }
            for row in summary
        ]
    }


@router.get("/headcount")
def get_headcount(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user_and_set_schema),
    department: str = None,
    employment_type: str = None,
):
    """
    Returns current active/inactive employee counts based on the DimEmployee table.
    Note: For historical headcount trends, a snapshot fact table (FactHeadcount) is required.
    """
    
    query = db.query(
        DimEmployee.status,
        func.count(DimEmployee.id).label("count")
    )
    
    if employment_type:
        query = query.filter(DimEmployee.employment_type == employment_type)
        
    # We could add joins to DimDepartment based on filters here
    # e.g., if department: query = query.join(DimDepartment).filter(DimDepartment.name == department)
    
    summary = query.group_by(DimEmployee.status).all()
    
    return {
        "tenant_id": current_user.get("schema_name"),
        "summary": [
            {
                "status": row.status,
                "count": row.count
            }
            for row in summary
        ]
    }
