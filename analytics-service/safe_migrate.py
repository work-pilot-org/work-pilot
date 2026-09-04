import os
import time
import sqlalchemy as sa
from alembic import command
from alembic.config import Config
from shared_infrastructure.core.config import settings
from sqlalchemy.exc import OperationalError

def main():
    print('Connecting to DB...')
    engine = sa.create_engine(str(settings.DATABASE_URL), pool_size=1, max_overflow=0)
    with engine.connect() as conn:
        print('Fetching schemas...')
        res = conn.execute(sa.text("SELECT schema_name FROM information_schema.schemata WHERE schema_name LIKE 'tenant_%';"))
        schemas = [row[0] for row in res]
        
    engine.dispose()
    
    for s in schemas:
        success = False
        attempts = 0
        while not success and attempts < 5:
            attempts += 1
            print(f'Migrating {s}... (Attempt {attempts})')
            try:
                # Create a fresh engine for each schema to avoid holding connections
                schema_engine = sa.create_engine(str(settings.DATABASE_URL), pool_size=1, max_overflow=0)
                with schema_engine.connect() as conn:
                    conn.execute(sa.text(f'SET search_path TO "{s}"'))
                    alembic_cfg = Config('alembic.ini')
                    alembic_cfg.set_main_option('sqlalchemy.url', str(settings.DATABASE_URL))
                    alembic_cfg.attributes['connection'] = conn
                    command.upgrade(alembic_cfg, 'head')
                    conn.commit()
                print(f'Success for {s}')
                success = True
                schema_engine.dispose()
                time.sleep(1) # Give pooler time to release connection
            except OperationalError as e:
                print(f'Connection failed for {s}, retrying in 3 seconds...')
                time.sleep(3)
            except Exception as e:
                print(f'Failed {s}: {e}')
                break # Non-connection error, stop retrying

if __name__ == '__main__':
    main()
