"""add employee_id to invitation

Revision ID: d25950c48ae4
Revises: b619e3ca6091
Create Date: 2026-08-03 17:01:40.540191

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'd25950c48ae4'
down_revision = ('1dbf2b75cd07', 'b619e3ca6091')
branch_labels = None
depends_on = None

from sqlalchemy.engine.reflection import Inspector

def upgrade() -> None:
    conn = op.get_bind()
    inspector = Inspector.from_engine(conn)
    columns = [c['name'] for c in inspector.get_columns('invitations')]
    if 'employee_id' not in columns:
        op.add_column('invitations', sa.Column('employee_id', postgresql.UUID(as_uuid=True), nullable=True))

def downgrade() -> None:
    op.drop_column('invitations', 'employee_id')
