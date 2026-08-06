from sqlalchemy import text
from sqlalchemy.orm import Session


def set_schema(
    db: Session,
    schema_name: str,
) -> None:
    """
    Switch PostgreSQL search_path
    """
    from shared_infrastructure.database.schema_utils import validate_schema_name
    schema_name = validate_schema_name(schema_name)
    db.connection().exec_driver_sql(f'SET search_path TO "{schema_name}", public')


def get_current_schema(
    db: Session,
) -> str:

    result = db.execute(
        text("SELECT current_schema();")
    )

    return result.scalar_one()
