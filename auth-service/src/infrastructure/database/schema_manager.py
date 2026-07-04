from sqlalchemy import text
from sqlalchemy.orm import Session

from src.infrastructure.database.base import TenantBase


class SchemaManager:

    @staticmethod
    def create_schema(
        db: Session,
        schema_name: str,
    ) -> None:
        """
        Create a new PostgreSQL schema.
        """

        db.execute(
            text(f'CREATE SCHEMA "{schema_name}"')
        )

    @staticmethod
    def create_tenant_tables(
        db: Session,
    ) -> None:
        """
        Create all tenant-specific tables
        in the currently selected schema.
        """

        connection = db.connection()

        TenantBase.metadata.create_all(
            bind=connection,
        )