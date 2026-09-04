from shared_infrastructure.database.session import SessionLocal
from sqlalchemy import text

db = SessionLocal()
db.execute(text('SET search_path TO "tenant_acme_corp"'))
print(db.execute(text('SELECT count(id) FROM employees')).fetchall())
