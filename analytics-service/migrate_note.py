import os
import sqlalchemy as sa
from alembic import command
from alembic.config import Config
from shared_infrastructure.core.config import settings

def main():
    s = "tenant_note"
    print(f'Migrating {s}...')
    engine = sa.create_engine(str(settings.DATABASE_URL), pool_size=1, max_overflow=0)
    with engine.connect() as conn:
        conn.execute(sa.text(f'SET search_path TO "{s}"'))
        alembic_cfg = Config('alembic.ini')
        alembic_cfg.set_main_option('sqlalchemy.url', str(settings.DATABASE_URL))
        alembic_cfg.attributes['connection'] = conn
        command.upgrade(alembic_cfg, 'head')
        conn.commit()
    print(f'Success for {s}')

if __name__ == '__main__':
    main()
