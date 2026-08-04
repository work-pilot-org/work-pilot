from shared_infrastructure.database.session import engine
from sqlalchemy import text
with engine.connect() as conn:
    conn.execute(text('DROP SCHEMA IF EXISTS tenant_gb CASCADE'))
    conn.commit()
