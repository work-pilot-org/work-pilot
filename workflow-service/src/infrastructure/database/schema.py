from sqlalchemy import text
from sqlalchemy.orm import Session


def set_schema(
    db: Session,
    schema_name: str,
) -> None:
    """
    Switch PostgreSQL search_path
    """

    db.execute(
        text("SET search_path TO :schema"),
        {"schema": schema_name},
    )


def get_current_schema(
    db: Session,
) -> str:

    result = db.execute(
        text("SELECT current_schema();")
    )

    return result.scalar_one()
