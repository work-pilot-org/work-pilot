import sqlalchemy as sa
from sqlalchemy import text

engine = sa.create_engine('postgresql+psycopg://postgres.bhllwlrdsbnynxhsgzio:szb2HURZUq5l5ybW@aws-1-ap-south-1.pooler.supabase.com:5432/postgres')

def silent_delete(conn, query, params):
    try:
        conn.execute(text(query), params)
    except Exception as e:
        print(f"Skipped error: {e}")

def cleanup():
    # Use autocommit so a single failure doesn't abort the whole transaction
    with engine.connect().execution_options(isolation_level="AUTOCOMMIT") as conn:
        print("Cleaning up database...")
        
        # 1. Delete specific users
        emails_to_delete = ['ashifek11@gmail.com', 'projectworkpilot@gmail.com']
        for email in emails_to_delete:
            res = conn.execute(text("SELECT id FROM users WHERE email = :email"), {"email": email}).fetchone()
            if res:
                user_id = res[0]
                print(f"Deleting user {email} ({user_id})")
                silent_delete(conn, "DELETE FROM user_roles WHERE user_id = :uid", {"uid": user_id})
                silent_delete(conn, "DELETE FROM user_profiles WHERE user_id = :uid", {"uid": user_id})
                
                # Try deleting them from all tenant schemas
                res_tenants = conn.execute(text("SELECT schema_name FROM tenants"))
                for row in res_tenants:
                    silent_delete(conn, f"DELETE FROM {row[0]}.employees WHERE auth_user_id = :uid", {"uid": user_id})
                
                silent_delete(conn, "DELETE FROM users WHERE id = :uid", {"uid": user_id})
        
        # 2. Identify test tenants
        res = conn.execute(text("SELECT id, schema_name FROM tenants WHERE schema_name LIKE 'tenant_test%' OR company_name ILIKE '%test%' OR schema_name = 'tenant_gmail'"))
        test_tenants = res.fetchall()
        
        for tenant_id, schema_name in test_tenants:
            print(f"Deleting test tenant {schema_name} (ID: {tenant_id})")
            
            silent_delete(conn, "DELETE FROM domains WHERE tenant_id = :tid", {"tid": tenant_id})
            silent_delete(conn, "DELETE FROM user_profiles WHERE tenant_id = :tid", {"tid": tenant_id})
            
            # Find users referencing this tenant
            res_users = conn.execute(text("SELECT id FROM users WHERE id IN (SELECT user_id FROM user_profiles WHERE tenant_id = :tid)"), {"tid": tenant_id})
            for row in res_users:
                silent_delete(conn, "DELETE FROM user_roles WHERE user_id = :uid", {"uid": row[0]})
                silent_delete(conn, "DELETE FROM users WHERE id = :uid", {"uid": row[0]})
                
            silent_delete(conn, f"DROP SCHEMA IF EXISTS {schema_name} CASCADE", {})
            silent_delete(conn, "DELETE FROM tenants WHERE id = :tid", {"tid": tenant_id})
            
        print("Cleanup complete.")

if __name__ == "__main__":
    cleanup()
