"""Add ETL correctness constraints and timestamps

Revision ID: bfa247182103
Revises: 47eb78b373b5
Create Date: 2026-08-18 02:42:10.496808

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'bfa247182103'
down_revision: Union[str, Sequence[str], None] = '47eb78b373b5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    # fact_workflow_execution
    op.add_column('fact_workflow_execution', sa.Column('execution_id', sa.UUID(), nullable=True))
    # Fill existing rows with source_event_id for backwards compat, then alter to non-null
    op.execute("UPDATE fact_workflow_execution SET execution_id = source_event_id")
    op.alter_column('fact_workflow_execution', 'execution_id', nullable=False)
    
    op.add_column('fact_workflow_execution', sa.Column('last_event_occurred_at', sa.DateTime(), nullable=True))
    op.create_index(op.f('ix_fact_workflow_execution_execution_id'), 'fact_workflow_execution', ['execution_id'], unique=False)
    op.create_unique_constraint('uq_tenant_execution', 'fact_workflow_execution', ['tenant_key', 'execution_id'])
    
    # fact_workflow_step
    op.create_table(
        'fact_workflow_step',
        sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column('execution_id', sa.UUID(), nullable=False),
        sa.Column('workflow_step_id', sa.UUID(), nullable=False),
        sa.Column('tenant_key', sa.BigInteger(), nullable=False),
        sa.Column('date_key', sa.Integer(), nullable=False),
        sa.Column('workflow_key', sa.BigInteger(), nullable=False),
        sa.Column('approver_key', sa.BigInteger(), nullable=True),
        sa.Column('source_event_id', sa.UUID(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('last_event_occurred_at', sa.DateTime(), nullable=True),
        sa.Column('step_order', sa.Integer(), nullable=False),
        sa.Column('entity_type', sa.String(length=100), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('decided_at', sa.DateTime(), nullable=True),
        sa.Column('decision_duration_seconds', sa.Integer(), nullable=True),
        sa.Column('status', sa.String(length=50), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('tenant_key', 'execution_id', 'workflow_step_id', name='uq_tenant_execution_step')
    )
    op.create_index(op.f('ix_fact_workflow_step_approver_key'), 'fact_workflow_step', ['approver_key'], unique=False)
    op.create_index(op.f('ix_fact_workflow_step_date_key'), 'fact_workflow_step', ['date_key'], unique=False)
    op.create_index(op.f('ix_fact_workflow_step_execution_id'), 'fact_workflow_step', ['execution_id'], unique=False)
    op.create_index(op.f('ix_fact_workflow_step_source_event_id'), 'fact_workflow_step', ['source_event_id'], unique=False)
    op.create_index(op.f('ix_fact_workflow_step_tenant_key'), 'fact_workflow_step', ['tenant_key'], unique=False)
    op.create_index(op.f('ix_fact_workflow_step_workflow_key'), 'fact_workflow_step', ['workflow_key'], unique=False)
    op.create_index(op.f('ix_fact_workflow_step_workflow_step_id'), 'fact_workflow_step', ['workflow_step_id'], unique=False)
    
    # fact_asset_assignment
    op.create_unique_constraint('uq_tenant_assignment', 'fact_asset_assignment', ['tenant_key', 'assignment_id'])


def downgrade() -> None:
    # fact_asset_assignment
    op.drop_constraint('uq_tenant_assignment', 'fact_asset_assignment', type_='unique')
    
    # fact_workflow_step
    op.drop_constraint('uq_tenant_execution_step', 'fact_workflow_step', type_='unique')
    op.drop_column('fact_workflow_step', 'last_event_occurred_at')
    
    # fact_workflow_execution
    op.drop_constraint('uq_tenant_execution', 'fact_workflow_execution', type_='unique')
    op.drop_index(op.f('ix_fact_workflow_execution_execution_id'), table_name='fact_workflow_execution')
    op.drop_column('fact_workflow_execution', 'last_event_occurred_at')
    op.drop_column('fact_workflow_execution', 'execution_id')
