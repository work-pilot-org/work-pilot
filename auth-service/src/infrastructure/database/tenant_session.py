import re

from sqlalchemy import text
from sqlalchemy.orm import Session


def set_tenant_schema(
    db: Session,
    schema_name: str,
) -> None:
    """
    Switch the current database session
    to the specified tenant schema.
    """

    if not re.fullmatch(
        r"[a-z][a-z0-9_]*",
        schema_name,
    ):
        raise ValueError("Invalid schema name.")

    db.execute(
        text(f'SET search_path TO "{schema_name}"')
    )


def set_public_schema(
    db: Session,
) -> None:
    """
    Switch the current database session
    back to the public schema.
    """

    db.execute(
        text('SET search_path TO "public"')
    )