from uuid import uuid4
from datetime import datetime

from sqlalchemy import String
from sqlalchemy import Boolean
from sqlalchemy import Integer
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Text

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from src.infrastructure.database.base import TenantBase


class Workflow(TenantBase):
    __tablename__ = "workflows"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid4()),
    )

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
    )

    created_by: Mapped[str] = mapped_column(
        String(36),
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )

    steps = relationship(
        "WorkflowStep",
        back_populates="workflow",
        cascade="all, delete-orphan",
    )


class WorkflowStep(TenantBase):
    __tablename__ = "workflow_steps"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid4()),
    )

    workflow_id: Mapped[str] = mapped_column(
        ForeignKey("workflows.id"),
    )

    step_order: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    step_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    approver_role: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    workflow = relationship(
        "Workflow",
        back_populates="steps",
    )


class WorkflowExecution(TenantBase):
    __tablename__ = "workflow_executions"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid4()),
    )

    workflow_id: Mapped[str] = mapped_column(
        ForeignKey("workflows.id"),
    )

    entity_type: Mapped[str] = mapped_column(
        String(100),
    )

    entity_id: Mapped[str] = mapped_column(
        String(36),
    )

    current_step: Mapped[int] = mapped_column(
        Integer,
        default=1,
    )

    status: Mapped[str] = mapped_column(
        String(50),
        default="pending",
    )

    started_by: Mapped[str] = mapped_column(
        String(36),
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )


class Approval(TenantBase):
    __tablename__ = "approvals"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid4()),
    )

    execution_id: Mapped[str] = mapped_column(
        ForeignKey("workflow_executions.id"),
    )

    approver_id: Mapped[str] = mapped_column(
        String(36),
    )

    decision: Mapped[str] = mapped_column(
        String(30),
        default="pending",
    )

    comments: Mapped[str | None] = mapped_column(
        Text,
    )

    decided_at: Mapped[datetime | None] = mapped_column(
        DateTime,
    )
