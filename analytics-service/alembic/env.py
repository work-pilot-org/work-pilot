from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool

from alembic import context
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'packages', 'shared-infrastructure', 'src')))

from shared_infrastructure.core.config import settings

# Import the Base classes
from src.models.base import TenantBase
# Import all models to ensure they are registered with the metadata
from src.models import *

config = context.config

config.set_main_option(
    "sqlalchemy.url",
    str(settings.DATABASE_URL),
)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Analytics has a single metadata for all tables now
target_metadata = TenantBase.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        compare_type=True,
        dialect_opts={"paramstyle": "named"},
        version_table="alembic_version_analytics",
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    # Check if a connection was passed in (e.g. from init_tenant_tables)
    connectable = config.attributes.get('connection', None)
    
    if connectable is None:
        connectable = engine_from_config(
            config.get_section(config.config_ini_section),
            prefix="sqlalchemy.",
            poolclass=pool.NullPool,
        )

        with connectable.connect() as connection:
            from sqlalchemy import text
            schemas_query = "SELECT schema_name FROM information_schema.schemata WHERE schema_name LIKE 'tenant_%'"
            schemas = [row[0] for row in connection.execute(text(schemas_query)).fetchall()]
            
            for schema_name in schemas:
                connection.execute(text(f'SET search_path TO "{schema_name}"'))
                context.configure(
                    connection=connection,
                    target_metadata=target_metadata,
                    compare_type=True,
                    version_table="alembic_version_analytics",
                    include_schemas=False,
                )

                with context.begin_transaction():
                    context.run_migrations()
    else:
        context.configure(
            connection=connectable,
            target_metadata=target_metadata,
            compare_type=True,
            version_table="alembic_version_analytics",
            include_schemas=False,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
