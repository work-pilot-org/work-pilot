import sqlalchemy as sa

engine = sa.create_engine('postgresql+psycopg://postgres.bhllwlrdsbnynxhsgzio:szb2HURZUq5l5ybW@aws-1-ap-south-1.pooler.supabase.com:5432/postgres')

with engine.connect() as conn:
    res = conn.execute(sa.text("SELECT schema_name FROM tenants"))
    schemas = [r[0] for r in res]
    
    for schema in schemas:
        try:
            print(f"Fixing schema {schema}...")
            # Check if column exists
            check = conn.execute(sa.text(f"SELECT column_name FROM information_schema.columns WHERE table_schema = '{schema}' AND table_name = 'employees' AND column_name = 'auth_user_id'")).fetchone()
            if not check:
                conn.execute(sa.text(f"ALTER TABLE {schema}.employees ADD COLUMN auth_user_id UUID;"))
                conn.execute(sa.text(f"CREATE UNIQUE INDEX uq_employees_auth_user_id_active_{schema} ON {schema}.employees (auth_user_id) WHERE is_active = true AND auth_user_id IS NOT NULL;"))
                conn.commit()
                print(f"  Added auth_user_id to {schema}")
            else:
                print(f"  auth_user_id already exists in {schema}")
        except Exception as e:
            print(f"  Error on {schema}:", e)
            conn.rollback()

print("All schemas processed.")
