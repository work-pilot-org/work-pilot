import os
import sqlalchemy as sa
from alembic import command
from alembic.config import Config
from shared_infrastructure.core.config import settings

def main():
    print('Connecting to DB...')
    engine = sa.create_engine(str(settings.DATABASE_URL))
    with engine.connect() as conn:
        print('Fetching schemas...')
        res = conn.execute(sa.text("SELECT schema_name FROM information_schema.schemata WHERE schema_name LIKE 'tenant_%';"))
        schemas = [row[0] for row in res]
        
        for s in schemas:
            print(f'Migrating {s}...')
            try:
                conn.execute(sa.text(f'SET search_path TO "{s}"'))
                alembic_cfg = Config('alembic.ini')
                alembic_cfg.set_main_option('sqlalchemy.url', str(settings.DATABASE_URL))
                alembic_cfg.attributes['connection'] = conn
                command.upgrade(alembic_cfg, 'head')
                conn.commit()
                print(f'Success for {s}')
            except Exception as e:
                conn.rollback()
                print(f'Failed {s}: {e}')

if __name__ == '__main__':
    main()
