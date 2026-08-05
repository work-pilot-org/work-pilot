import sqlalchemy as sa
from sqlalchemy import text

engine = sa.create_engine('postgresql+psycopg://postgres.bhllwlrdsbnynxhsgzio:szb2HURZUq5l5ybW@aws-1-ap-south-1.pooler.supabase.com:5432/postgres')

def fix_enum(schema_name: str, conn):
    print(f"Fixing schema: {schema_name}")
    try:
        conn.execute(text(f"ALTER TABLE {schema_name}.employees ALTER COLUMN employment_status TYPE VARCHAR(50) USING employment_status::text;"))
        conn.commit()
        print(f"  Fixed employment_status in {schema_name}")
    except Exception as e:
        print(f"  Error fixing schema {schema_name}: {e}")
        conn.rollback()

if __name__ == "__main__":
    with engine.connect() as conn:
        res = conn.execute(text("SELECT schema_name FROM tenants"))
        schemas = [row[0] for row in res]
        for schema in schemas:
            fix_enum(schema, conn)
