from typing import List

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from src.infrastructure.database.session import get_db
from src.core.dependencies import get_current_user, security
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
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    service = WorkflowService(db)
    return await service.start_workflow_execution(data, token=credentials.credentials)


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
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    service = WorkflowService(db)
    return await service.approve_step(
        task_id=task_id,
        user_id=current_user.get("sub"),
        user_role=current_user.get("role", "EMPLOYEE"),
        decision_data=data,
        token=credentials.credentials,
    )


@router.patch(
    "/workflow-executions/{execution_id}/cancel",
    response_model=WorkflowExecutionResponse,
)
async def cancel_workflow(
    execution_id: str,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    service = WorkflowService(db)
    return await service.cancel_workflow(
        execution_id=execution_id,
        user_id=current_user.get("sub"),
    )


@router.patch(
    "/workflow-executions/{execution_id}/restart",
    response_model=WorkflowExecutionResponse,
)
async def restart_workflow(
    execution_id: str,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    service = WorkflowService(db)
    return await service.restart_workflow(
        execution_id=execution_id,
        user_id=current_user.get("sub"),
        token=credentials.credentials,
    )

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
