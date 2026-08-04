"""Add Invitation Model

Revision ID: 1dbf2b75cd07
Revises: d25950c48ae4
Create Date: 2026-08-01 11:46:13.048952

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '1dbf2b75cd07'
down_revision: Union[str, Sequence[str], None] = 'd25950c48ae4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Safely create enum types in PostgreSQL if they don't already exist
    op.execute("DO $$ BEGIN CREATE TYPE role AS ENUM ('ORG_ADMIN', 'HR_ADMIN', 'IT_ADMIN', 'MANAGER', 'EMPLOYEE'); EXCEPTION WHEN duplicate_object THEN null; END $$;")
    op.execute("DO $$ BEGIN CREATE TYPE invitationstatus AS ENUM ('PENDING', 'ACCEPTED', 'EXPIRED', 'REVOKED'); EXCEPTION WHEN duplicate_object THEN null; END $$;")

    # Check if table already exists before attempting creation
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    if not inspector.has_table('invitations'):
        op.create_table('invitations',
            sa.Column('id', sa.UUID(), nullable=False),
            sa.Column('tenant_id', sa.Integer(), nullable=False),
            sa.Column('email', sa.String(length=255), nullable=False),
            sa.Column('role', postgresql.ENUM('ORG_ADMIN', 'HR_ADMIN', 'IT_ADMIN', 'MANAGER', 'EMPLOYEE', name='role', create_type=False), nullable=False),
            sa.Column('token_hash', sa.String(length=64), nullable=False),
            sa.Column('status', postgresql.ENUM('PENDING', 'ACCEPTED', 'EXPIRED', 'REVOKED', name='invitationstatus', create_type=False), nullable=False),
            sa.Column('expires_at', sa.DateTime(), nullable=False),
            sa.Column('created_at', sa.DateTime(), nullable=False),
            sa.Column('updated_at', sa.DateTime(), nullable=False),
            sa.Column('created_by', sa.UUID(), nullable=True),
            sa.Column('accepted_by_user_id', sa.UUID(), nullable=True),
            sa.Column('revoked_at', sa.DateTime(), nullable=True),
            sa.Column('last_sent_at', sa.DateTime(), nullable=True),
            sa.ForeignKeyConstraint(['accepted_by_user_id'], ['users.id'], ondelete='SET NULL'),
            sa.ForeignKeyConstraint(['created_by'], ['users.id'], ondelete='SET NULL'),
            sa.ForeignKeyConstraint(['tenant_id'], ['tenants.id'], ondelete='CASCADE'),
            sa.PrimaryKeyConstraint('id')
        )
        op.create_index(op.f('ix_invitations_expires_at'), 'invitations', ['expires_at'], unique=False)
        op.create_index(op.f('ix_invitations_status'), 'invitations', ['status'], unique=False)
        op.create_index('ix_invitations_tenant_email', 'invitations', ['tenant_id', 'email'], unique=False)
        op.create_index(op.f('ix_invitations_token_hash'), 'invitations', ['token_hash'], unique=True)


def downgrade() -> None:
    """Downgrade schema."""
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    if inspector.has_table('invitations'):
        op.drop_index(op.f('ix_invitations_token_hash'), table_name='invitations')
        op.drop_index('ix_invitations_tenant_email', table_name='invitations')
        op.drop_index(op.f('ix_invitations_status'), table_name='invitations')
        op.drop_index(op.f('ix_invitations_expires_at'), table_name='invitations')
        op.drop_table('invitations')
