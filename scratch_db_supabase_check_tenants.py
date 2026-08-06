import sqlalchemy as sa
engine = sa.create_engine('postgresql+psycopg://postgres.bhllwlrdsbnynxhsgzio:szb2HURZUq5l5ybW@aws-1-ap-south-1.pooler.supabase.com:5432/postgres')
with engine.connect() as conn:
    try:
        res = conn.execute(sa.text("SELECT schema_name FROM tenants"))
        print("Tenants schemas:", [r[0] for r in res])
    except Exception as e:
        print("Error reading tenants:", e)
