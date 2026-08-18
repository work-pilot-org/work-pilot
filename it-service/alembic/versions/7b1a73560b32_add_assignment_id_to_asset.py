"""add assignment_id to asset

Revision ID: 7b1a73560b32
Revises: 7a2a73560b31
Create Date: 2026-08-17 11:39:58.572135

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '7b1a73560b32'
down_revision: str | Sequence[str] | None = '7a2a73560b31'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column('assets', sa.Column('assignment_id', sa.UUID(), nullable=True))


def downgrade() -> None:
    op.drop_column('assets', 'assignment_id')
