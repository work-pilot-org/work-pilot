import os
import sys
from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool

# Add src/ to Python path
sys.path.insert(
    0,
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            "..",
            "src",
        )
    ),
)

from notification_service.modules.notifications.models import NotificationLog
from shared_infrastructure.core.config import settings
from shared_infrastructure.database.base import TenantBase


config = context.config

# Use the application's database configuration.
config.set_main_option(
    "sqlalchemy.url",
    settings.DATABASE_URL
    or "postgresql+psycopg://postgres:postgres@localhost:5432/workpilot",
)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)


# Importing NotificationLog registers it with TenantBase.metadata.
target_metadata = TenantBase.metadata


def include_object(
    object_,
    name,
    type_,
    reflected,
    compare_to,
):
    """
    Restrict this service's Alembic migrations to objects owned
    by Notification Service.

    The WorkPilot services share the same Supabase database, so
    Alembic must not generate DROP operations for tables owned by
    Auth, HR, IT, Workflow, Supabase, etc.
    """

    if type_ == "table":
        # Keep only Notification Service's table.
        return name == "notification_logs"

    if type_ == "index":
        # Keep indexes belonging to notification_logs.
        if object_.table.name == "notification_logs":
            return True
        return False

    if type_ == "column":
        # Keep columns belonging to notification_logs.
        if object_.table.name == "notification_logs":
            return True
        return False

    # Keep other objects associated with the target metadata.
    return True


def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")

    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        include_schemas=False,
        include_object=include_object,
        compare_type=True,
        version_table="alembic_version_notification",
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            include_schemas=False,
            include_object=include_object,
            compare_type=True,
            version_table="alembic_version_notification",
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()