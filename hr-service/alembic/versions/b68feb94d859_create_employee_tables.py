"""Create employee tables

Revision ID: b68feb94d859
Revises:
Create Date: 2026-07-16 23:01:15.154674

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID


# revision identifiers, used by Alembic.
revision: str = "b68feb94d859"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "employees",
        sa.Column(
            "id",
            UUID(as_uuid=True),
            primary_key=True,
            nullable=False,
        ),
        sa.Column(
            "auth_user_id",
            UUID(as_uuid=True),
            nullable=False,
        ),
        sa.Column(
            "employee_code",
            sa.String(length=30),
            nullable=False,
        ),
        sa.Column("first_name", sa.String(length=100), nullable=False),
        sa.Column("last_name", sa.String(length=100), nullable=False),
        sa.Column("phone", sa.String(length=20), nullable=True),
        sa.Column("gender", sa.String(length=20), nullable=True),
        sa.Column("date_of_birth", sa.Date(), nullable=True),
        sa.Column("joining_date", sa.Date(), nullable=False),
        sa.Column("employment_type", sa.String(length=50), nullable=False),
        sa.Column(
            "employment_status",
            sa.String(length=50),
            nullable=False,
            server_default=sa.text("'ACTIVE'"),
        ),
        sa.Column(
            "department_id",
            UUID(as_uuid=True),
            nullable=True,
        ),
        sa.Column(
            "designation_id",
            UUID(as_uuid=True),
            nullable=True,
        ),
        sa.Column(
            "manager_id",
            UUID(as_uuid=True),
            nullable=True,
        ),
        sa.Column("work_location", sa.String(length=150), nullable=True),
        sa.Column("profile_photo", sa.Text(), nullable=True),
        sa.Column(
            "is_active",
            sa.Boolean(),
            nullable=False,
            server_default=sa.text("true"),
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("now()"),
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("now()"),
        ),
        sa.ForeignKeyConstraint(
            ["manager_id"],
            ["employees.id"],
            name="fk_employees_manager_id_employees",
        ),
    )
    op.create_index(
        "uq_employees_auth_user_id_active",
        "employees",
        ["auth_user_id"],
        unique=True,
        postgresql_where=sa.text("is_active = true"),
    )
    op.create_index(
        "uq_employees_employee_code_active",
        "employees",
        ["employee_code"],
        unique=True,
        postgresql_where=sa.text("is_active = true"),
    )

    op.create_table(
        "employee_profiles",
        sa.Column(
            "id",
            UUID(as_uuid=True),
            primary_key=True,
            nullable=False,
        ),
        sa.Column(
            "employee_id",
            UUID(as_uuid=True),
            nullable=False,
        ),
        sa.Column("address", sa.Text(), nullable=True),
        sa.Column("city", sa.String(length=100), nullable=True),
        sa.Column("state", sa.String(length=100), nullable=True),
        sa.Column("country", sa.String(length=100), nullable=True),
        sa.Column("postal_code", sa.String(length=20), nullable=True),
        sa.Column(
            "emergency_contact_name",
            sa.String(length=100),
            nullable=True,
        ),
        sa.Column(
            "emergency_contact_phone",
            sa.String(length=20),
            nullable=True,
        ),
        sa.Column(
            "emergency_contact_relation",
            sa.String(length=50),
            nullable=True,
        ),
        sa.Column("blood_group", sa.String(length=10), nullable=True),
        sa.Column("marital_status", sa.String(length=30), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("now()"),
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("now()"),
        ),
        sa.ForeignKeyConstraint(
            ["employee_id"],
            ["employees.id"],
            name="fk_employee_profiles_employee_id_employees",
            ondelete="CASCADE",
        ),
        sa.UniqueConstraint(
            "employee_id",
            name="uq_employee_profiles_employee_id",
        ),
    )

    op.create_table(
        "employee_documents",
        sa.Column(
            "id",
            UUID(as_uuid=True),
            primary_key=True,
            nullable=False,
        ),
        sa.Column(
            "employee_id",
            UUID(as_uuid=True),
            nullable=False,
        ),
        sa.Column(
            "document_name",
            sa.String(length=150),
            nullable=False,
        ),
        sa.Column(
            "document_type",
            sa.String(length=100),
            nullable=True,
        ),
        sa.Column("file_url", sa.Text(), nullable=False),
        sa.Column(
            "uploaded_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("now()"),
        ),
        sa.ForeignKeyConstraint(
            ["employee_id"],
            ["employees.id"],
            name="fk_employee_documents_employee_id_employees",
            ondelete="CASCADE",
        ),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("employee_documents")
    op.drop_table("employee_profiles")
    op.drop_index("uq_employees_employee_code_active", table_name="employees")
    op.drop_index("uq_employees_auth_user_id_active", table_name="employees")
    op.drop_table("employees")
