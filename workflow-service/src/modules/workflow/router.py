from shared_infrastructure.core.rbac import Permission
from shared_infrastructure.core.dependencies import require_permissions
from typing import List

from fastapi import APIRouter, Depends, Query, status, BackgroundTasks
from sqlalchemy.orm import Session

from shared_infrastructure.database.session import get_db
from shared_infrastructure.events import EventEnvelope
from shared_infrastructure.publisher import publish_event
from shared_infrastructure.core.dependencies import get_current_user_and_set_schema
from shared_infrastructure.core.security import get_current_user, security
from fastapi.security import HTTPAuthorizationCredentials

from .schemas import (
    WorkflowCreate,
    WorkflowUpdate,
    WorkflowResponse,
    WorkflowExecutionCreate,
    WorkflowExecutionResponse,
    ApprovalDecision,
    ApprovalResponse,
)
from .service import WorkflowService

router = APIRouter(
    prefix="",
    tags=["Workflows"],
)


# ---------------------------------------------------------
# Workflow Templates
# ---------------------------------------------------------
@router.post(
    "/workflows",
    response_model=WorkflowResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_workflow(
    data: WorkflowCreate,
    _rbac=Depends(require_permissions([Permission.WORKFLOW_MANAGE])),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    service = WorkflowService(db)
    return service.create_workflow(data, user_id=current_user.get("sub"))


@router.get(
    "/workflows",
    response_model=List[WorkflowResponse],
)
def get_all_workflows(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    service = WorkflowService(db)
    # Skipping pagination in service layer for brevity, but returning all here
    return service.get_all_workflows()[skip : skip + limit]


@router.get(
    "/workflows/{workflow_id}",
    response_model=WorkflowResponse,
)
def get_workflow(
    workflow_id: str,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    service = WorkflowService(db)
    return service.get_workflow(workflow_id)


@router.put(
    "/workflows/{workflow_id}",
    response_model=WorkflowResponse,
)
def update_workflow(
    workflow_id: str,
    data: WorkflowUpdate,
    _rbac=Depends(require_permissions([Permission.WORKFLOW_MANAGE])),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    service = WorkflowService(db)
    return service.update_workflow(workflow_id, data)


@router.delete(
    "/workflows/{workflow_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_workflow(
    workflow_id: str,
    _rbac=Depends(require_permissions([Permission.WORKFLOW_MANAGE])),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    service = WorkflowService(db)
    service.delete_workflow(workflow_id)


# ---------------------------------------------------------
# Workflow Executions & Tasks
# ---------------------------------------------------------
@router.post(
    "/workflow-executions",
    response_model=WorkflowExecutionResponse,
    status_code=status.HTTP_201_CREATED,
)
async def start_workflow_execution(
    data: WorkflowExecutionCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user_and_set_schema),
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    service = WorkflowService(db)
    execution = await service.start_workflow_execution(data, token=credentials.credentials)
    
    event_start = EventEnvelope[dict](
        event_type="workflow.execution.started",
        source="workflow-service",
        tenant_id=current_user.get("schema_name", "public"),
        payload={
            "workflow_id": execution.workflow_id,
            "execution_id": execution.id,
            "entity_type": execution.entity_type,
            "status": execution.status
        }
    )
    background_tasks.add_task(publish_event, "workflow.execution", event_start)
    
    history = service.get_history(execution.id)
    first_step = next((h for h in history if h.decision == "pending"), None)
    if first_step:
        event_step = EventEnvelope[dict](
            event_type="workflow.step.created",
            source="workflow-service",
            tenant_id=current_user.get("schema_name", "public"),
            payload={
                "workflow_id": execution.workflow_id,
                "execution_id": execution.id,
                "entity_type": execution.entity_type,
                "status": execution.status,
                "step_id": first_step.id,
                "approver_id": first_step.approver_id,
                "decision": first_step.decision,
                "step_order": execution.current_step
            }
        )
        background_tasks.add_task(publish_event, "workflow.execution", event_step)
        
    return execution


@router.get(
    "/workflow-executions",
    response_model=List[WorkflowExecutionResponse],
)
def get_workflow_executions(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    service = WorkflowService(db)
    return service.get_all_executions(skip=skip, limit=limit)

@router.get(
    "/workflow-executions/{execution_id}",
    response_model=WorkflowExecutionResponse,
)
def get_workflow_execution(
    execution_id: str,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    service = WorkflowService(db)
    return service.get_execution(execution_id)


@router.patch(
    "/tasks/{task_id}/approve",
    response_model=ApprovalResponse,
)
async def approve_task(
    task_id: str,
    data: ApprovalDecision,
    background_tasks: BackgroundTasks,
    _rbac=Depends(require_permissions([Permission.WORKFLOW_APPROVE])),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user_and_set_schema),
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    service = WorkflowService(db)
    approval = await service.approve_step(
        task_id=task_id,
        user_id=current_user.get("sub"),
        user_role=current_user.get("role", "EMPLOYEE"),
        decision_data=data,
        token=credentials.credentials,
    )
    execution = service.get_execution(approval.execution_id)
    
    event_step_decided = EventEnvelope[dict](
        event_type=f"workflow.step.{approval.decision}",
        source="workflow-service",
        tenant_id=current_user.get("schema_name", "public"),
        payload={
            "workflow_id": execution.workflow_id,
            "execution_id": execution.id,
            "entity_type": execution.entity_type,
            "status": execution.status,
            "step_id": approval.id,
            "approver_id": approval.approver_id,
            "decision": approval.decision,
            "decided_at": approval.decided_at.isoformat() if approval.decided_at else None,
            "step_order": execution.current_step
        }
    )
    background_tasks.add_task(publish_event, "workflow.execution", event_step_decided)
    
    if execution.status == "pending":
        history = service.get_history(execution.id)
        next_step = next((h for h in history if h.decision == "pending"), None)
        if next_step:
            event_next_step = EventEnvelope[dict](
                event_type="workflow.step.created",
                source="workflow-service",
                tenant_id=current_user.get("schema_name", "public"),
                payload={
                    "workflow_id": execution.workflow_id,
                    "execution_id": execution.id,
                    "entity_type": execution.entity_type,
                    "status": execution.status,
                    "step_id": next_step.id,
                    "approver_id": next_step.approver_id,
                    "decision": next_step.decision,
                    "step_order": execution.current_step
                }
            )
            background_tasks.add_task(publish_event, "workflow.execution", event_next_step)
    else:
        event_exec = EventEnvelope[dict](
            event_type=f"workflow.execution.{execution.status}",
            source="workflow-service",
            tenant_id=current_user.get("schema_name", "public"),
            payload={
                "workflow_id": execution.workflow_id,
                "execution_id": execution.id,
                "entity_type": execution.entity_type,
                "status": execution.status
            }
        )
        background_tasks.add_task(publish_event, "workflow.execution", event_exec)

    return approval


@router.patch(
    "/workflow-executions/{execution_id}/cancel",
    response_model=WorkflowExecutionResponse,
)
async def cancel_workflow(
    execution_id: str,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user_and_set_schema),
):
    service = WorkflowService(db)
    execution = await service.cancel_workflow(
        execution_id=execution_id,
        user_id=current_user.get("sub"),
    )
    event_exec = EventEnvelope[dict](
        event_type="workflow.execution.cancelled",
        source="workflow-service",
        tenant_id=current_user.get("schema_name", "public"),
        payload={
            "workflow_id": execution.workflow_id,
            "execution_id": execution.id,
            "entity_type": execution.entity_type,
            "status": execution.status
        }
    )
    background_tasks.add_task(publish_event, "workflow.execution", event_exec)
    return execution


@router.patch(
    "/workflow-executions/{execution_id}/restart",
    response_model=WorkflowExecutionResponse,
)
async def restart_workflow(
    execution_id: str,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user_and_set_schema),
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    service = WorkflowService(db)
    execution = await service.restart_workflow(
        execution_id=execution_id,
        user_id=current_user.get("sub"),
        token=credentials.credentials,
    )
    
    event_start = EventEnvelope[dict](
        event_type="workflow.execution.started",
        source="workflow-service",
        tenant_id=current_user.get("schema_name", "public"),
        payload={
            "workflow_id": execution.workflow_id,
            "execution_id": execution.id,
            "entity_type": execution.entity_type,
            "status": execution.status
        }
    )
    background_tasks.add_task(publish_event, "workflow.execution", event_start)
    
    history = service.get_history(execution.id)
    first_step = next((h for h in history if h.decision == "pending"), None)
    if first_step:
        event_step = EventEnvelope[dict](
            event_type="workflow.step.created",
            source="workflow-service",
            tenant_id=current_user.get("schema_name", "public"),
            payload={
                "workflow_id": execution.workflow_id,
                "execution_id": execution.id,
                "entity_type": execution.entity_type,
                "status": execution.status,
                "step_id": first_step.id,
                "approver_id": first_step.approver_id,
                "decision": first_step.decision,
                "step_order": execution.current_step
            }
        )
        background_tasks.add_task(publish_event, "workflow.execution", event_step)
        
    return execution

@router.get(
    "/workflow-executions/{execution_id}/history",
    response_model=List[ApprovalResponse],
)
def get_workflow_history(
    execution_id: str,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    service = WorkflowService(db)
    return service.get_history(execution_id)
