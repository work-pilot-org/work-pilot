import re

from sqlalchemy import text
from sqlalchemy.orm import Session


def set_tenant_schema(db: Session, schema_name: str) -> None:
    """
    Set the PostgreSQL search_path to the tenant schema.

    Example:
        SET search_path TO company_abc, public;
    """

    if not re.fullmatch(r"[a-z][a-z0-9_]*", schema_name):
        raise ValueError("Invalid tenant schema name.")

    db.execute(
        text(f'SET search_path TO "{schema_name}", public')
    )


def set_public_schema(db: Session) -> None:
    """
    Reset the PostgreSQL search_path back to the public schema.
    """

    db.execute(
        text('SET search_path TO "public"')
    )