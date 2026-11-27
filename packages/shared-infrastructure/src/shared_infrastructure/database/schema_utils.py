import re

def validate_schema_name(schema_name: str) -> str:
    """
    Validate that the schema name contains only letters, digits, and underscores.
    Prevents SQL injection when setting search_path or creating schemas.
    """
    if not re.fullmatch(r"^[A-Za-z0-9_]+$", schema_name):
        raise ValueError(f"Invalid schema name: {schema_name}")
    return schema_name
