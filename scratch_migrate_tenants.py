import sqlalchemy as sa
from sqlalchemy import text

# Update PostgreSQL connection string with psycopg (Supabase)
engine = sa.create_engine('postgresql+psycopg://postgres.bhllwlrdsbnynxhsgzio:szb2HURZUq5l5ybW@aws-1-ap-south-1.pooler.supabase.com:5432/postgres')

def fix_schema(schema_name: str, conn):
    print(f"Checking schema: {schema_name}")
    # Check if employee_code column exists in employees table
    res = conn.execute(text(f"SELECT column_name FROM information_schema.columns WHERE table_schema = '{schema_name}' AND table_name = 'employees' AND column_name = 'employee_code'")).fetchone()
    
    if res:
        print(f"  Schema {schema_name} already has employee_code.")
        return
        
    print(f"  Fixing schema {schema_name}...")
    try:
        # Alter table to match HR service Employee model
        # We need to add the missing columns and possibly drop old ones
        # But wait, what if we just add the missing ones?
        
        # Add employee_code, first_name, last_name, phone, gender, date_of_birth, joining_date, employment_type, department_id, designation_id, work_location, profile_photo
        # We can drop user_id, full_name, role, department, job_title, phone_number
        
        conn.execute(text(f"""
            ALTER TABLE {schema_name}.employees 
            ADD COLUMN IF NOT EXISTS employee_code VARCHAR(30),
            ADD COLUMN IF NOT EXISTS first_name VARCHAR(100),
            ADD COLUMN IF NOT EXISTS last_name VARCHAR(100),
            ADD COLUMN IF NOT EXISTS phone VARCHAR(20),
            ADD COLUMN IF NOT EXISTS gender VARCHAR(20),
            ADD COLUMN IF NOT EXISTS date_of_birth DATE,
            ADD COLUMN IF NOT EXISTS joining_date DATE,
            ADD COLUMN IF NOT EXISTS employment_type VARCHAR(50),
            ADD COLUMN IF NOT EXISTS department_id UUID,
            ADD COLUMN IF NOT EXISTS designation_id UUID,
            ADD COLUMN IF NOT EXISTS work_location VARCHAR(150),
            ADD COLUMN IF NOT EXISTS profile_photo TEXT
        """))
        
        # We must populate nullable=False columns with defaults for existing rows to avoid errors
        conn.execute(text(f"UPDATE {schema_name}.employees SET employee_code = 'EMP-' || SUBSTRING(id::text, 1, 6) WHERE employee_code IS NULL"))
        conn.execute(text(f"UPDATE {schema_name}.employees SET first_name = SPLIT_PART(full_name, ' ', 1) WHERE first_name IS NULL"))
        conn.execute(text(f"UPDATE {schema_name}.employees SET last_name = SUBSTRING(full_name FROM POSITION(' ' IN full_name) + 1) WHERE last_name IS NULL OR last_name = ''"))
        conn.execute(text(f"UPDATE {schema_name}.employees SET joining_date = created_at::DATE WHERE joining_date IS NULL"))
        conn.execute(text(f"UPDATE {schema_name}.employees SET employment_type = 'FULL_TIME' WHERE employment_type IS NULL"))
        
        # Alter columns to set NOT NULL constraints
        conn.execute(text(f"""
            ALTER TABLE {schema_name}.employees 
            ALTER COLUMN employee_code SET NOT NULL,
            ALTER COLUMN first_name SET NOT NULL,
            ALTER COLUMN last_name SET NOT NULL,
            ALTER COLUMN joining_date SET NOT NULL,
            ALTER COLUMN employment_type SET NOT NULL
        """))
        
        # Drop old columns (optional, but safe to drop since HR service doesn't use them)
        conn.execute(text(f"""
            ALTER TABLE {schema_name}.employees 
            DROP COLUMN IF EXISTS user_id CASCADE,
            DROP COLUMN IF EXISTS full_name CASCADE,
            DROP COLUMN IF EXISTS role CASCADE,
            DROP COLUMN IF EXISTS department CASCADE,
            DROP COLUMN IF EXISTS job_title CASCADE,
            DROP COLUMN IF EXISTS phone_number CASCADE
        """))
        
        # Unique constraints and indexes
        conn.execute(text(f"""
            DO $$
            BEGIN
                IF NOT EXISTS (SELECT 1 FROM pg_indexes WHERE indexname = 'uq_employees_employee_code_active_{schema_name}') THEN
                    CREATE UNIQUE INDEX uq_employees_employee_code_active_{schema_name} 
                    ON {schema_name}.employees (employee_code) WHERE is_active = true;
                END IF;
            END
            $$;
        """))
        
        conn.commit()
        print(f"  Successfully fixed schema {schema_name}")
    except Exception as e:
        print(f"  Error fixing schema {schema_name}: {e}")
        conn.rollback()

if __name__ == "__main__":
    with engine.connect() as conn:
        res = conn.execute(text("SELECT schema_name FROM tenants"))
        schemas = [row[0] for row in res]
        for schema in schemas:
            fix_schema(schema, conn)
