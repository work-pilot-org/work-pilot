import sqlalchemy as sa
engine = sa.create_engine('postgresql+psycopg://postgres:postgres@localhost:5432/workpilot')
with engine.connect() as conn:
    res = conn.execute(sa.text("SELECT column_name FROM information_schema.columns WHERE table_name = 'employees'"))
    print([r[0] for r in res])
