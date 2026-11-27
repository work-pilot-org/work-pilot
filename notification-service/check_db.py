from sqlalchemy import create_engine, text
from shared_infrastructure.core.config import settings

engine = create_engine(settings.DATABASE_URL)

with engine.connect() as connection:
    print("\n=== SCHEMAS ===")
    rows = connection.execute(
        text("""
            SELECT schema_name
            FROM information_schema.schemata
            ORDER BY schema_name
        """)
    ).fetchall()

    for row in rows:
        print(row[0])

    print("\n=== NOTIFICATION LOGS ===")
    rows = connection.execute(
        text("""
            SELECT table_schema, table_name
            FROM information_schema.tables
            WHERE table_name = 'notification_logs'
            ORDER BY table_schema
        """)
    ).fetchall()

    for row in rows:
        print(f"{row[0]}.{row[1]}")

    print("\n=== ALEMBIC VERSION TABLES ===")
    rows = connection.execute(
        text("""
            SELECT table_schema, table_name
            FROM information_schema.tables
            WHERE table_name LIKE 'alembic_version%'
            ORDER BY table_schema, table_name
        """)
    ).fetchall()

    for row in rows:
        print(f"{row[0]}.{row[1]}")
