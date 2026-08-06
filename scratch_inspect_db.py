import sqlalchemy as sa
from sqlalchemy import text
import pprint

engine = sa.create_engine('postgresql+psycopg://postgres.bhllwlrdsbnynxhsgzio:szb2HURZUq5l5ybW@aws-1-ap-south-1.pooler.supabase.com:5432/postgres')

with engine.connect() as conn:
    print("=== USERS ===")
    res = conn.execute(text("SELECT id, email FROM users"))
    users = res.fetchall()
    for row in users:
        print(f"{row[0]} | {row[1]}")
        
    print("\n=== TENANTS ===")
    res = conn.execute(text("SELECT id, company_name, schema_name FROM tenants"))
    tenants = res.fetchall()
    for row in tenants:
        print(f"{row[0]} | {row[1]} | {row[2]}")
