"""add FactAssetAssignment and DimAsset name

Revision ID: 47eb78b373b5
Revises: f4a9306e0062
Create Date: 2026-08-18 02:10:56.196545

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '47eb78b373b5'
down_revision: Union[str, Sequence[str], None] = 'f4a9306e0062'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add name to dim_asset
    op.add_column('dim_asset', sa.Column('name', sa.String(length=150), server_default='Unknown', nullable=False))
    
    # Create fact_asset_assignment
    op.create_table('fact_asset_assignment',
    sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
    sa.Column('assignment_id', sa.UUID(), nullable=False),
    sa.Column('tenant_key', sa.BigInteger(), nullable=False),
    sa.Column('date_key', sa.Integer(), nullable=False),
    sa.Column('asset_key', sa.BigInteger(), nullable=False),
    sa.Column('employee_key', sa.BigInteger(), nullable=False),
    sa.Column('source_event_id', sa.UUID(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('last_event_occurred_at', sa.DateTime(), nullable=False),
    sa.Column('assigned_at', sa.DateTime(), nullable=False),
    sa.Column('returned_at', sa.DateTime(), nullable=True),
    sa.Column('assignment_duration_days', sa.Integer(), nullable=True),
    sa.Column('assignment_status', sa.String(length=50), nullable=False),
    sa.ForeignKeyConstraint(['asset_key'], ['dim_asset.id'], ),
    sa.ForeignKeyConstraint(['date_key'], ['dim_date.id'], ),
    sa.ForeignKeyConstraint(['employee_key'], ['dim_employee.id'], ),
    sa.ForeignKeyConstraint(['tenant_key'], ['dim_tenant.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_fact_asset_assignment_asset_key'), 'fact_asset_assignment', ['asset_key'], unique=False)
    op.create_index(op.f('ix_fact_asset_assignment_assignment_id'), 'fact_asset_assignment', ['assignment_id'], unique=False)
    op.create_index(op.f('ix_fact_asset_assignment_date_key'), 'fact_asset_assignment', ['date_key'], unique=False)
    op.create_index(op.f('ix_fact_asset_assignment_employee_key'), 'fact_asset_assignment', ['employee_key'], unique=False)
    op.create_index(op.f('ix_fact_asset_assignment_source_event_id'), 'fact_asset_assignment', ['source_event_id'], unique=False)
    op.create_index(op.f('ix_fact_asset_assignment_tenant_key'), 'fact_asset_assignment', ['tenant_key'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_fact_asset_assignment_tenant_key'), table_name='fact_asset_assignment')
    op.drop_index(op.f('ix_fact_asset_assignment_source_event_id'), table_name='fact_asset_assignment')
    op.drop_index(op.f('ix_fact_asset_assignment_employee_key'), table_name='fact_asset_assignment')
    op.drop_index(op.f('ix_fact_asset_assignment_date_key'), table_name='fact_asset_assignment')
    op.drop_index(op.f('ix_fact_asset_assignment_assignment_id'), table_name='fact_asset_assignment')
    op.drop_index(op.f('ix_fact_asset_assignment_asset_key'), table_name='fact_asset_assignment')
    op.drop_table('fact_asset_assignment')
    op.drop_column('dim_asset', 'name')
