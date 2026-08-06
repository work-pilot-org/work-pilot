from sqlalchemy.orm import Session
from sqlalchemy import text

from shared_infrastructure.database.schema_utils import validate_schema_name

def set_tenant_schema(
    db: Session,
    schema_name: str,
) -> None:
    """
    Switch the current database session
    to the specified tenant schema.
    """
    schema_name = validate_schema_name(schema_name)
    db.connection().exec_driver_sql(f'SET search_path TO "{schema_name}", public')


def set_public_schema(
    db: Session,
) -> None:
    """
    Switch the current database session
    back to the public schema.
    """
    db.connection().exec_driver_sql('SET search_path TO "public"')