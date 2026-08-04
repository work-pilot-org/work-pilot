from sqlalchemy import create_engine, text
engine = create_engine('postgresql+psycopg://postgres.bhllwlrdsbnynxhsgzio:szb2HURZUq5l5ybW@aws-1-ap-south-1.pooler.supabase.com:5432/postgres')
with engine.connect() as conn:
    res = conn.execute(text("SELECT table_schema, table_name FROM information_schema.tables WHERE table_schema = 'public'"))
    for row in res:
        print(row)
