from sqlalchemy.orm import Session

from .models import (
    Workflow,
    WorkflowStep,
    WorkflowExecution,
    Approval,
)


class WorkflowRepository:

    def __init__(self, db: Session):
        self.db = db

    # ---------------- Workflow ----------------

    def create_workflow(self, workflow: Workflow):

        self.db.add(workflow)
        self.db.commit()
        self.db.refresh(workflow)

        return workflow

    def get_workflow(self, workflow_id: str):

        return (
            self.db.query(Workflow)
            .filter(Workflow.id == workflow_id)
            .first()
        )

    def get_all_workflows(self):

        return (
            self.db.query(Workflow)
            .all()
        )

    def update_workflow(self, workflow):

        self.db.commit()
        self.db.refresh(workflow)

        return workflow

    def delete_workflow(self, workflow):

        self.db.delete(workflow)
        self.db.commit()

    # ---------------- Workflow Step ----------------

    def create_step(self, step: WorkflowStep):

        self.db.add(step)
        self.db.commit()
        self.db.refresh(step)

        return step

    def get_steps(self, workflow_id: str):

        return (
            self.db.query(WorkflowStep)
            .filter(
                WorkflowStep.workflow_id == workflow_id
            )
            .order_by(
                WorkflowStep.step_order
            )
            .all()
        )

    # ---------------- Workflow Execution ----------------

    def create_execution(
        self,
        execution: WorkflowExecution,
    ):

        self.db.add(execution)
        self.db.commit()
        self.db.refresh(execution)

        return execution

    def get_execution(
        self,
        execution_id: str,
    ):

        return (
            self.db.query(WorkflowExecution)
            .filter(
                WorkflowExecution.id == execution_id
            )
            .first()
        )

    def update_execution(
        self,
        execution,
    ):

        self.db.commit()
        self.db.refresh(execution)

        return execution

    # ---------------- Approval ----------------

    def create_approval(
        self,
        approval: Approval,
    ):

        self.db.add(approval)
        self.db.commit()
        self.db.refresh(approval)

        return approval

    def get_approvals(
        self,
        execution_id: str,
    ):

        return (
            self.db.query(Approval)
            .filter(
                Approval.execution_id == execution_id
            )
            .all()
        )

    def update_approval(
        self,
        approval,
    ):

        self.db.commit()
        self.db.refresh(approval)

        return approval
