"""merge

Revision ID: f82b305bd0a2
Revises: bfa247182103
Create Date: 2026-08-18 20:06:42.547185

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f82b305bd0a2'
down_revision: Union[str, Sequence[str], None] = 'bfa247182103'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
