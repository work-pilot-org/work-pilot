from sqlalchemy.orm import Session

from shared_infrastructure.database.base import TenantBase
from shared_infrastructure.database.schema_utils import validate_schema_name

# Import tenant models to register them with TenantBase.metadata before create_all
from src.modules.rbac.models import Role, UserRole

class SchemaManager:

    @staticmethod
    def create_schema(
        db: Session,
        schema_name: str,
    ) -> None:
        """
        Create a new PostgreSQL schema.
        """
        schema_name = validate_schema_name(schema_name)
        db.connection().exec_driver_sql(f'CREATE SCHEMA "{schema_name}"')

    @staticmethod
    def create_tenant_tables(
        db: Session,
        schema_name: str,
    ) -> None:
        """
        Create all tenant-specific tables
        in the currently selected schema.
        """
        schema_name = validate_schema_name(schema_name)
        connection = db.connection()
        
        # Temporarily isolate search_path so SQLAlchemy doesn't see tables in public and skip them
        connection.exec_driver_sql(f'SET search_path TO "{schema_name}"')
        
        TenantBase.metadata.create_all(
            bind=connection,
        )
        
        # Restore normal tenant search_path
        connection.exec_driver_sql(f'SET search_path TO "{schema_name}", public')