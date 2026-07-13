"""Add MFA fields

Revision ID: 87c9a88c0f32
Revises: b619e3ca6091
Create Date: 2026-07-11 11:48:48.762126

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '87c9a88c0f32'
down_revision: Union[str, Sequence[str], None] = 'b619e3ca6091'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('users', sa.Column('mfa_enabled_at', sa.DateTime(), nullable=True))
    op.add_column('users', sa.Column('mfa_last_used_at', sa.DateTime(), nullable=True))


def downgrade() -> None:
    op.drop_column('users', 'mfa_last_used_at')
    op.drop_column('users', 'mfa_enabled_at')
