"""
Pydantic schemas for the Analytics Agent tools.
"""

from pydantic import BaseModel, Field
from typing import Optional


class GetAttendanceSummarySchema(BaseModel):
    """Schema for getting attendance summary metrics."""
    pass


class GetLeaveUtilizationSchema(BaseModel):
    """Schema for getting leave utilization metrics."""
    period: Optional[str] = Field(None, description="Time period (e.g., 'this_month', 'last_month')")
    department: Optional[str] = Field(None, description="Department name to filter by")


class GetHeadcountSchema(BaseModel):
    """Schema for getting employee headcount."""
    department: Optional[str] = Field(None, description="Department name to filter by")
    employment_type: Optional[str] = Field(None, description="Employment type to filter by (e.g., 'FULL_TIME')")


class GetTicketSummarySchema(BaseModel):
    """Schema for getting IT ticket summary."""
    period: Optional[str] = Field(None, description="Time period")
    category: Optional[str] = Field(None, description="Ticket category to filter by (e.g., 'HARDWARE')")


class GetAssetAssignmentsSchema(BaseModel):
    """Schema for getting IT asset assignment analytics."""
    status: Optional[str] = Field(None, description="Asset assignment status (e.g., 'ASSIGNED')")
    category: Optional[str] = Field(None, description="Asset category to filter by")


class GetWorkflowPerformanceSchema(BaseModel):
    """Schema for getting workflow performance metrics."""
    workflow_id: Optional[str] = Field(None, description="Specific workflow ID to filter by")
    execution_status: Optional[str] = Field(None, description="Workflow execution status (e.g., 'COMPLETED', 'FAILED')")


class GetWorkflowBottlenecksSchema(BaseModel):
    """Schema for getting workflow bottlenecks."""
    workflow_id: Optional[str] = Field(None, description="Specific workflow ID to filter by")
    step_order: Optional[int] = Field(None, description="Specific step order to filter by")
    status: Optional[str] = Field(None, description="Status of the step (e.g., 'PENDING')")
