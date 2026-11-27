from pydantic import BaseModel, UUID4
from typing import Optional

class AttendancePayload(BaseModel):
    attendance_id: int
    employee_id: str
    check_in: Optional[str] = None
    check_out: Optional[str] = None
    attendance_date: str
    status: str
    working_minutes: Optional[int] = 0
    overtime_minutes: Optional[int] = 0

class LeavePayload(BaseModel):
    leave_request_id: str
    employee_id: str
    leave_type: str
    start_date: str
    end_date: str
    total_days: float
    status: str

class EmployeePayload(BaseModel):
    employee_id: str
    first_name: str
    last_name: str
    employment_type: str
    status: str

class TicketPayload(BaseModel):
    ticket_id: str
    requester_id: str
    assigned_to: Optional[str] = None
    category: str
    priority: str
    status: str
    created_at: str

class OrganizationPayload(BaseModel):
    entity_type: str
    id: str
    name: str
    status: str
    department_id: Optional[str] = None

class WorkflowEventPayload(BaseModel):
    workflow_id: str
    execution_id: str
    entity_type: str
    status: str
    
    # Present for step events
    step_id: Optional[str] = None
    step_order: Optional[int] = None
    approver_id: Optional[str] = None
    created_at: Optional[str] = None
    decided_at: Optional[str] = None
    decision: Optional[str] = None
    
    # Workflow template details (for DimWorkflow)
    workflow_name: Optional[str] = None

class AssetEventPayload(BaseModel):
    asset_id: UUID4
    category: Optional[str] = None
    status: Optional[str] = None
    name: Optional[str] = None
    employee_id: Optional[UUID4] = None
    assignment_id: Optional[UUID4] = None

