import sqlalchemy as sa
engine = sa.create_engine('postgresql+psycopg://postgres:postgres@db:5432/workpilot')
with engine.connect() as conn:
    conn.execute(sa.text("DROP SCHEMA public CASCADE;"))
    conn.execute(sa.text("CREATE SCHEMA public;"))
    conn.execute(sa.text("GRANT ALL ON SCHEMA public TO postgres;"))
    conn.execute(sa.text("GRANT ALL ON SCHEMA public TO public;"))
    conn.commit()
print("Schema dropped and recreated")
