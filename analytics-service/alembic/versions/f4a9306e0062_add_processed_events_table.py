"""Add processed_events table

Revision ID: f4a9306e0062
Revises: d0398e5af1af
Create Date: 2026-08-17 21:39:49.162823

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f4a9306e0062'
down_revision: Union[str, Sequence[str], None] = 'd0398e5af1af'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'processed_events',
        sa.Column('event_id', sa.String(), nullable=False),
        sa.Column('event_type', sa.String(), nullable=False),
        sa.Column('processed_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint('event_id')
    )
    op.create_index(op.f('ix_processed_events_event_type'), 'processed_events', ['event_type'], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f('ix_processed_events_event_type'), table_name='processed_events')
    op.drop_table('processed_events')
