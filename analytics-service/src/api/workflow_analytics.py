from typing import Any

from fastapi import APIRouter, Depends, Query
from sqlalchemy import func
from sqlalchemy.orm import Session

from shared_infrastructure.core.dependencies import get_current_user_and_set_schema
from shared_infrastructure.database.session import get_db
from src.models.dimensions import DimWorkflow, DimDate, DimEmployee
from src.models.facts import FactWorkflowExecution, FactWorkflowStep

router = APIRouter(
    prefix="/workflows",
    tags=["Workflow Analytics"],
)

@router.get("/performance")
def get_workflow_performance(
    workflow_id: str | None = None,
    execution_status: str | None = None,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user_and_set_schema),
) -> Any:
    """
    Get aggregate metrics about workflow executions.
    """
    query = db.query(
        DimWorkflow.name.label("workflow_name"),
        DimWorkflow.workflow_type,
        FactWorkflowExecution.execution_status,
        func.count(FactWorkflowExecution.id).label("total_executions"),
        func.avg(FactWorkflowExecution.total_completion_minutes).label("avg_completion_minutes"),
        func.max(FactWorkflowExecution.total_completion_minutes).label("max_completion_minutes")
    ).join(
        DimWorkflow, FactWorkflowExecution.workflow_key == DimWorkflow.id
    )

    if workflow_id:
        query = query.filter(DimWorkflow.workflow_id == workflow_id)
    if execution_status:
        query = query.filter(FactWorkflowExecution.execution_status == execution_status)

    results = query.group_by(
        DimWorkflow.name,
        DimWorkflow.workflow_type,
        FactWorkflowExecution.execution_status
    ).all()

    return [
        {
            "workflow_name": r.workflow_name,
            "workflow_type": r.workflow_type,
            "execution_status": r.execution_status,
            "total_executions": r.total_executions,
            "avg_completion_minutes": round(r.avg_completion_minutes, 1) if r.avg_completion_minutes else 0,
            "max_completion_minutes": r.max_completion_minutes or 0,
        }
        for r in results
    ]


@router.get("/bottlenecks")
def get_workflow_bottlenecks(
    workflow_id: str | None = None,
    step_order: int | None = None,
    status: str | None = None,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user_and_set_schema),
) -> Any:
    """
    Identify bottlenecks at the individual step level.
    """
    query = db.query(
        DimWorkflow.name.label("workflow_name"),
        FactWorkflowStep.step_order,
        FactWorkflowStep.entity_type,
        FactWorkflowStep.status,
        func.count(FactWorkflowStep.id).label("total_steps"),
        func.avg(FactWorkflowStep.decision_duration_seconds).label("avg_duration_seconds"),
        func.max(FactWorkflowStep.decision_duration_seconds).label("max_duration_seconds")
    ).join(
        DimWorkflow, FactWorkflowStep.workflow_key == DimWorkflow.id
    )

    if workflow_id:
        query = query.filter(DimWorkflow.workflow_id == workflow_id)
    if step_order:
        query = query.filter(FactWorkflowStep.step_order == step_order)
    if status:
        query = query.filter(FactWorkflowStep.status == status)

    results = query.group_by(
        DimWorkflow.name,
        FactWorkflowStep.step_order,
        FactWorkflowStep.entity_type,
        FactWorkflowStep.status
    ).order_by(
        FactWorkflowStep.step_order
    ).all()

    return [
        {
            "workflow_name": r.workflow_name,
            "step_order": r.step_order,
            "entity_type": r.entity_type,
            "status": r.status,
            "total_steps": r.total_steps,
            "avg_duration_minutes": round(r.avg_duration_seconds / 60.0, 1) if r.avg_duration_seconds else 0,
            "max_duration_minutes": round(r.max_duration_seconds / 60.0, 1) if r.max_duration_seconds else 0,
        }
        for r in results
    ]
