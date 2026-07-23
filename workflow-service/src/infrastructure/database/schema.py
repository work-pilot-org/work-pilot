from sqlalchemy import text
from sqlalchemy.orm import Session


def set_schema(
    db: Session,
    schema_name: str,
) -> None:
    """
    Switch PostgreSQL search_path
    """

    import re
    if not re.fullmatch(r"[a-z][a-z0-9_]*", schema_name):
        raise ValueError("Invalid schema name.")

    db.execute(
        text(f'SET search_path TO "{schema_name}", public')
    )


def get_current_schema(
    db: Session,
) -> str:

    result = db.execute(
        text("SELECT current_schema();")
    )

    return result.scalar_one()
