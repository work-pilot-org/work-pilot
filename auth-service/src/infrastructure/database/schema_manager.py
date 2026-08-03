from sqlalchemy import text
from sqlalchemy.orm import Session

from shared_infrastructure.database.base import TenantBase

# Import tenant models to register them with TenantBase.metadata before create_all
from src.modules.rbac.models import Role, UserRole
from src.modules.employee.models import Employee

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
        schema_name: str,
    ) -> None:
        """
        Create all tenant-specific tables
        in the currently selected schema.
        """

        connection = db.connection()
        
        # Temporarily isolate search_path so SQLAlchemy doesn't see tables in public and skip them
        connection.execute(text(f'SET search_path TO "{schema_name}"'))
        
        TenantBase.metadata.create_all(
            bind=connection,
        )
        
        # Restore normal tenant search_path
        connection.execute(text(f'SET search_path TO "{schema_name}", public'))