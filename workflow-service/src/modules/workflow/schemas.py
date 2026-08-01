from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


# ---------- Workflow ----------

class WorkflowBase(BaseModel):
    name: str = Field(..., max_length=255)
    description: Optional[str] = None
    is_active: bool = True


class WorkflowCreate(WorkflowBase):
    pass


class WorkflowUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None


class WorkflowResponse(WorkflowBase):
    id: str
    created_by: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


# ---------- Workflow Step ----------

class WorkflowStepBase(BaseModel):
    step_order: int
    step_name: str
    approver_role: str


class WorkflowStepCreate(WorkflowStepBase):
    workflow_id: str


class WorkflowStepUpdate(BaseModel):
    step_order: Optional[int] = None
    step_name: Optional[str] = None
    approver_role: Optional[str] = None


class WorkflowStepResponse(WorkflowStepBase):
    id: str
    workflow_id: str

    model_config = ConfigDict(from_attributes=True)


# ---------- Workflow Execution ----------

class WorkflowExecutionCreate(BaseModel):
    workflow_id: str
    entity_type: str
    entity_id: str
    started_by: str


class WorkflowExecutionResponse(BaseModel):
    id: str
    workflow_id: str
    entity_type: str
    entity_id: str
    current_step: int
    status: str
    started_by: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# ---------- Approval ----------

class ApprovalCreate(BaseModel):
    execution_id: str
    approver_id: str
    comments: Optional[str] = None


class ApprovalDecision(BaseModel):
    decision: str
    comments: Optional[str] = None


class ApprovalResponse(BaseModel):
    id: str
    execution_id: str
    approver_id: str
    decision: str
    comments: Optional[str]
    decided_at: Optional[datetime]

    model_config = ConfigDict(from_attributes=True)
