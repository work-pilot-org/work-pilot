from logging.config import fileConfig

from alembic import context

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from src.core.config import settings
from src.infrastructure.database.base import TenantBase
from src.modules.workflow.models import *

config = context.config

config.set_main_option(
    "sqlalchemy.url",
    settings.DATABASE_URL,
)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = TenantBase.metadata

def include_object(object, name, type_, reflected, compare_to):
    if type_ == "table":
        # Only include tables defined in our target_metadata
        return name in target_metadata.tables
    return True


def run_migrations_offline():

    context.configure(
        url=settings.DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        version_table="alembic_version_workflow",
        include_object=include_object,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():

    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:

        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            version_table="alembic_version_workflow",
            include_object=include_object,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()

else:
    run_migrations_online()
