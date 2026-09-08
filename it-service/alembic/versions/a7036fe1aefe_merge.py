"""merge

Revision ID: a7036fe1aefe
Revises: 097f17259a78, 7b1a73560b32
Create Date: 2026-09-07 23:03:32.252849

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa



# revision identifiers, used by Alembic.
revision: str = 'a7036fe1aefe'
down_revision: Union[str, Sequence[str], None] = ('097f17259a78', '7b1a73560b32')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass