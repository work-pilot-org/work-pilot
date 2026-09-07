from sqlalchemy import text
from shared_infrastructure.database.session import engine
from shared_infrastructure.database.base import TenantBase
from src.modules.onboarding.models import OnboardingTask
from src.modules.offboarding.models import OffboardingTask

def create_tables():
    with engine.begin() as conn:
        schemas_query = "SELECT schema_name FROM information_schema.schemata WHERE schema_name LIKE 'tenant_%'"
        result = conn.execute(text(schemas_query))
        schemas = [row[0] for row in result.fetchall()]

        for schema_name in schemas:
            print(f"Creating tables for {schema_name}")
            conn.execute(text(f'SET search_path TO "{schema_name}"'))
            TenantBase.metadata.create_all(conn)

if __name__ == "__main__":
    create_tables()
