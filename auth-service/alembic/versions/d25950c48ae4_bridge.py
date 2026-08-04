"""Bridge migration for legacy revision

Revision ID: d25950c48ae4
Revises: 87c9a88c0f32
Create Date: 2026-07-15 12:00:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd25950c48ae4'
down_revision: Union[str, Sequence[str], None] = '87c9a88c0f32'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
