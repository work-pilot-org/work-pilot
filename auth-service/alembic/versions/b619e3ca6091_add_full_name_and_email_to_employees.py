"""Add full_name and email to employees

Revision ID: b619e3ca6091
Revises: 7b9352dd17b6
Create Date: 2026-07-05 11:27:15.911594

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'b619e3ca6091'
down_revision: Union[str, Sequence[str], None] = '7b9352dd17b6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
