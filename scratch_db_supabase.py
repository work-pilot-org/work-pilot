import sqlalchemy as sa
engine = sa.create_engine('postgresql+psycopg://postgres.bhllwlrdsbnynxhsgzio:szb2HURZUq5l5ybW@aws-1-ap-south-1.pooler.supabase.com:5432/postgres')
with engine.connect() as conn:
    try:
        res = conn.execute(sa.text("SELECT column_name FROM information_schema.columns WHERE table_name = 'employees'"))
        print("Columns in employees:", [r[0] for r in res])
    except Exception as e:
        print("Error reading employees:", e)
    
    try:
        res = conn.execute(sa.text("SELECT version_num FROM alembic_version_hr"))
        print("HR version:", [r[0] for r in res])
    except Exception as e:
        print("Error reading hr version:", e)
