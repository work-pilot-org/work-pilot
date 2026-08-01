from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

# ---------- Workflow ----------

class WorkflowBase(BaseModel):
    name: str = Field(..., max_length=255)
    description: str | None = None
    is_active: bool = True


class WorkflowCreate(WorkflowBase):
    pass


class WorkflowUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    is_active: bool | None = None


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
    step_order: int | None = None
    step_name: str | None = None
    approver_role: str | None = None


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
    comments: str | None = None


class ApprovalDecision(BaseModel):
    decision: str
    comments: str | None = None


class ApprovalResponse(BaseModel):
    id: str
    execution_id: str
    approver_id: str
    decision: str
    comments: str | None
    decided_at: datetime | None

    model_config = ConfigDict(from_attributes=True)
