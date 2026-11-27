"""make auth_user_id nullable and add invitation_status

Revision ID: b5435ba6cd1b
Revises: 21a410172480
Create Date: 2026-08-03 22:34:25.745066

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'b5435ba6cd1b'
down_revision = '21a410172480'
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.add_column('employees', sa.Column('invitation_status', sa.String(length=20), nullable=True))
    op.alter_column('employees', 'auth_user_id',
               existing_type=sa.UUID(),
               nullable=True)

def downgrade() -> None:
    op.alter_column('employees', 'auth_user_id',
               existing_type=sa.UUID(),
               nullable=False)
    op.drop_column('employees', 'invitation_status')
