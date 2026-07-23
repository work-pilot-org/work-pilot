from typing import List, Optional
from datetime import datetime

from sqlalchemy.orm import Session

from .models import Workflow, WorkflowStep, WorkflowExecution, Approval
from .schemas import (
    WorkflowCreate,
    WorkflowUpdate,
    WorkflowStepCreate,
    WorkflowStepUpdate,
    WorkflowExecutionCreate,
    ApprovalDecision,
)
from .repository import WorkflowRepository
from .exceptions import (
    WorkflowNotFoundException,
    WorkflowStepNotFoundException,
    WorkflowExecutionNotFoundException,
    TaskNotFoundException,
    InvalidWorkflowStateException,
    UnauthorizedApproverException,
)
from src.infrastructure.clients.hr_client import hr_client
from src.infrastructure.clients.it_client import it_client
from src.infrastructure.clients.notification_client import notification_client


class WorkflowService:
    def __init__(self, db: Session):
        self.db = db
        self.repository = WorkflowRepository(db)

    # ---------------------------------------------------------
    # Workflow Templates
    # ---------------------------------------------------------
    def create_workflow(self, data: WorkflowCreate, user_id: str) -> Workflow:
        workflow = Workflow(
            name=data.name,
            description=data.description,
            is_active=data.is_active,
            created_by=user_id,
        )
        self.repository.create_workflow(workflow)
        self.db.commit()
        return workflow

    def get_workflow(self, workflow_id: str) -> Workflow:
        workflow = self.repository.get_workflow(workflow_id)
        if not workflow:
            raise WorkflowNotFoundException()
        return workflow

    def get_all_workflows(self) -> List[Workflow]:
        return self.repository.get_all_workflows()

    def update_workflow(self, workflow_id: str, data: WorkflowUpdate) -> Workflow:
        workflow = self.get_workflow(workflow_id)
        if data.name is not None:
            workflow.name = data.name
        if data.description is not None:
            workflow.description = data.description
        if data.is_active is not None:
            workflow.is_active = data.is_active

        self.repository.update_workflow(workflow)
        self.db.commit()
        return workflow

    def delete_workflow(self, workflow_id: str) -> None:
        workflow = self.get_workflow(workflow_id)
        self.repository.delete_workflow(workflow)
        self.db.commit()

    # ---------------------------------------------------------
    # Workflow Steps
    # ---------------------------------------------------------
    def add_workflow_step(self, data: WorkflowStepCreate) -> WorkflowStep:
        self.get_workflow(data.workflow_id)  # Validate workflow exists
        step = WorkflowStep(
            workflow_id=data.workflow_id,
            step_order=data.step_order,
            step_name=data.step_name,
            approver_role=data.approver_role,
        )
        self.repository.create_step(step)
        self.db.commit()
        return step

    def get_workflow_steps(self, workflow_id: str) -> List[WorkflowStep]:
        self.get_workflow(workflow_id)
        return self.repository.get_steps(workflow_id)

    # ---------------------------------------------------------
    # Engine / Execution Operations
    # ---------------------------------------------------------
    async def start_workflow_execution(
        self, data: WorkflowExecutionCreate, token: Optional[str] = None
    ) -> WorkflowExecution:
        # 1. Validate workflow and get steps
        workflow = self.get_workflow(data.workflow_id)
        if not workflow.is_active:
            raise InvalidWorkflowStateException("Cannot start an inactive workflow")

        steps = self.repository.get_steps(data.workflow_id)
        if not steps:
            raise InvalidWorkflowStateException("Workflow has no steps")

        # 2. Create Execution
        execution = WorkflowExecution(
            workflow_id=data.workflow_id,
            entity_type=data.entity_type,
            entity_id=data.entity_id,
            current_step=1,
            status="pending",
            started_by=data.started_by,
        )
        self.repository.create_execution(execution)

        # 3. Create first approval task
        first_step = next((s for s in steps if s.step_order == 1), None)
        if not first_step:
            # Should never happen if steps exist, but safeguard
            self.db.rollback()
            raise InvalidWorkflowStateException("Missing step order 1")

        approval = Approval(
            execution_id=execution.id,
            approver_id=first_step.approver_role,  # role-based for now, or could map to an ID
            decision="pending",
        )
        self.repository.create_approval(approval)

        self.db.commit()

        # 4. Notify Approver
        await notification_client.send_notification(
            user_id=approval.approver_id,
            message=f"Action Required: {first_step.step_name} for {execution.entity_type}",
            token=token
        )

        return execution

    def get_execution(self, execution_id: str) -> WorkflowExecution:
        execution = self.repository.get_execution(execution_id)
        if not execution:
            raise WorkflowExecutionNotFoundException()
        return execution
        
    def get_history(self, execution_id: str) -> List[Approval]:
        self.get_execution(execution_id)
        return self.repository.get_approvals(execution_id)

    async def approve_step(
        self, task_id: str, user_id: str, user_role: str, decision_data: ApprovalDecision, token: Optional[str] = None
    ) -> Approval:
        
        # We lookup the task directly by approval ID
        # Since repository only has get_approvals by execution, let's implement get_approval manually or rely on filtering
        approval = self.db.query(Approval).filter(Approval.id == task_id).first()
        if not approval:
            raise TaskNotFoundException()
            
        execution = self.repository.get_execution(approval.execution_id)
        if not execution:
            raise WorkflowExecutionNotFoundException()

        if execution.status != "pending":
            raise InvalidWorkflowStateException("Workflow is not in a pending state")

        if approval.decision != "pending":
            raise InvalidWorkflowStateException("Task already processed")

        # Basic role/user validation (assuming approver_id holds a role requirement for now)
        if approval.approver_id not in [user_id, user_role, "ORG_ADMIN"]:
             raise UnauthorizedApproverException()

        # Update Approval
        approval.decision = "approved" if decision_data.decision.lower() == "approve" else "rejected"
        approval.comments = decision_data.comments
        approval.decided_at = datetime.utcnow()
        self.repository.update_approval(approval)

        if approval.decision == "rejected":
            execution.status = "rejected"
            self.repository.update_execution(execution)
            self.db.commit()
            
            # Notify starter
            await notification_client.send_notification(
                user_id=execution.started_by,
                message=f"Workflow Rejected: {execution.entity_type}",
                token=token
            )
            return approval

        # It was approved. Find next step.
        steps = self.repository.get_steps(execution.workflow_id)
        next_step_order = execution.current_step + 1
        next_step = next((s for s in steps if s.step_order == next_step_order), None)

        if next_step:
            # Advance to next step
            execution.current_step = next_step_order
            self.repository.update_execution(execution)
            
            new_approval = Approval(
                execution_id=execution.id,
                approver_id=next_step.approver_role,
                decision="pending",
            )
            self.repository.create_approval(new_approval)
            self.db.commit()
            
            # Notify next approver
            await notification_client.send_notification(
                user_id=new_approval.approver_id,
                message=f"Action Required: {next_step.step_name} for {execution.entity_type}",
                token=token
            )
        else:
            # Workflow completed
            execution.status = "completed"
            self.repository.update_execution(execution)
            self.db.commit()
            
            # Notify starter
            await notification_client.send_notification(
                user_id=execution.started_by,
                message=f"Workflow Completed: {execution.entity_type}",
                token=token
            )
            
            # Trigger downstream actions
            await self._handle_workflow_completion(execution, token)

        return approval

    async def cancel_workflow(self, execution_id: str, user_id: str) -> WorkflowExecution:
        execution = self.get_execution(execution_id)
        if execution.status not in ["pending"]:
            raise InvalidWorkflowStateException("Only pending workflows can be cancelled")
            
        if execution.started_by != user_id:
            raise UnauthorizedApproverException()
            
        execution.status = "cancelled"
        self.repository.update_execution(execution)
        
        # Mark pending approvals as cancelled
        approvals = self.repository.get_approvals(execution_id)
        for app in approvals:
            if app.decision == "pending":
                app.decision = "cancelled"
                app.decided_at = datetime.utcnow()
                self.repository.update_approval(app)
                
        self.db.commit()
        return execution

    async def restart_workflow(self, execution_id: str, user_id: str, token: Optional[str] = None) -> WorkflowExecution:
        execution = self.get_execution(execution_id)
        if execution.status not in ["cancelled", "rejected"]:
            raise InvalidWorkflowStateException("Only cancelled or rejected workflows can be restarted")
            
        if execution.started_by != user_id:
            raise UnauthorizedApproverException()
            
        execution.status = "pending"
        execution.current_step = 1
        self.repository.update_execution(execution)
        
        steps = self.repository.get_steps(execution.workflow_id)
        first_step = next((s for s in steps if s.step_order == 1), None)
        
        if first_step:
            new_approval = Approval(
                execution_id=execution.id,
                approver_id=first_step.approver_role,
                decision="pending",
            )
            self.repository.create_approval(new_approval)
            
        self.db.commit()
        
        if first_step:
            await notification_client.send_notification(
                user_id=new_approval.approver_id,
                message=f"Action Required (Restarted): {first_step.step_name} for {execution.entity_type}",
                token=token
            )
            
        return execution

    async def _handle_workflow_completion(self, execution: WorkflowExecution, token: Optional[str] = None):
        """
        Generic dispatch to external services upon workflow completion.
        """
        # We catch exceptions here to ensure the transaction isn't rolled back 
        # after it's already committed in the main flow, or we rely on the fact 
        # that it is a separate network call.
        try:
            if execution.entity_type.lower() == "leave_request":
                # Changed to target the correct HR service endpoint for leave requests
                await hr_client.patch(f"/leave-requests/{execution.entity_id}/status", json={"status": "APPROVED"}, token=token)
            elif execution.entity_type.lower() == "asset_request" or execution.entity_type.lower() == "access_request":
                # Changed to target the correct IT service endpoint for access requests
                await it_client.patch(f"/access/{execution.entity_id}/status", json={"status": "APPROVED"}, token=token)
        except Exception as e:
            # Log failure to notify downstream, but workflow remains completed
            # In a production system, this might use a message queue
            print(f"Failed to notify downstream service for {execution.entity_type}: {e}")
