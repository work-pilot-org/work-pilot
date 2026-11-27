from shared_infrastructure.database.session import SessionLocal
from sqlalchemy import text

db = SessionLocal()
schemas = [r[0] for r in db.execute(text("SELECT schema_name FROM information_schema.schemata WHERE schema_name LIKE 'tenant_%'")).fetchall()]
for s in schemas:
    db.execute(text(f'SET search_path TO "{s}"; DROP TABLE IF EXISTS alembic_version_hr CASCADE;'))
db.commit()
print("Dropped.")
