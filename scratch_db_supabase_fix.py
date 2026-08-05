import sqlalchemy as sa
engine = sa.create_engine('postgresql+psycopg://postgres.bhllwlrdsbnynxhsgzio:szb2HURZUq5l5ybW@aws-1-ap-south-1.pooler.supabase.com:5432/postgres')
with engine.connect() as conn:
    try:
        conn.execute(sa.text("ALTER TABLE employees ADD COLUMN auth_user_id UUID;"))
        conn.execute(sa.text("CREATE UNIQUE INDEX uq_employees_auth_user_id_active ON employees (auth_user_id) WHERE is_active = true AND auth_user_id IS NOT NULL;"))
        conn.commit()
        print("Successfully added auth_user_id and index.")
    except Exception as e:
        print("Error:", e)
        conn.rollback()
