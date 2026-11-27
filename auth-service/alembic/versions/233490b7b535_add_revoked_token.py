"""add_revoked_token

Revision ID: 233490b7b535
Revises: d25950c48ae4
Create Date: 2026-08-04 19:56:40.684155

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '233490b7b535'
down_revision: Union[str, Sequence[str], None] = 'd25950c48ae4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    op.create_table('revoked_tokens',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('token', sa.String(length=1024), nullable=False),
    sa.Column('revoked_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_revoked_tokens_token'), 'revoked_tokens', ['token'], unique=True)

def downgrade() -> None:
    op.drop_index(op.f('ix_revoked_tokens_token'), table_name='revoked_tokens')
    op.drop_table('revoked_tokens')
