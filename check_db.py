import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), 'packages', 'shared-infrastructure', 'src'))
from shared_infrastructure.database.session import get_session
from sqlalchemy import text
from contextlib import contextmanager

def check_leave_balances():
    # Setup DB
    os.environ["DATABASE_URL"] = "postgresql+psycopg://postgres.bhllwlrdsbnynxhsgzio:szb2HURZUq5l5ybW@aws-1-ap-south-1.pooler.supabase.com:5432/postgres"
    
    with next(get_session()) as db:
        db.execute(text('SET search_path TO "tenant_1", public'))
        result = db.execute(text("SELECT employee_id, leave_type_id, total_days, year FROM leave_balances")).fetchall()
        for r in result:
            print(f"Employee: {r[0]}, Leave Type: {r[1]}, Total Days: {r[2]}, Year: {r[3]}")

if __name__ == '__main__':
    check_leave_balances()
