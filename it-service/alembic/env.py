import os
import sys
from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool
from it_service.modules.assets.models import Asset
from it_service.modules.devices.models import Device
# ---------------------------------------------------------------------
# Add src/ to Python path
# ---------------------------------------------------------------------
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

# ---------------------------------------------------------------------
# Project imports
# ---------------------------------------------------------------------
from it_service.core.config import settings
from it_service.infrastructure.database.base import TenantBase

# Import all models so Alembic can detect them
from it_service.modules.helpdesk.models import (
    Ticket,
    TicketComment,
    TicketAttachment,
    TicketActivity,
)
from it_service.modules.assets.models import Asset
from it_service.modules.devices.models import Device, DeviceMaintenanceHistory
from it_service.modules.software.models import Software, InstalledSoftware, InstallationRequest
from it_service.modules.licenses.models import License, LicenseAssignment
from it_service.modules.access.models import AccessRequest
from it_service.modules.maintenance.models import MaintenanceRecord

# ---------------------------------------------------------------------
# Alembic configuration
# ---------------------------------------------------------------------
config = context.config

config.set_main_option(
    "sqlalchemy.url",
    settings.database_url,
)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = TenantBase.metadata


# ---------------------------------------------------------------------
# Offline migrations
# ---------------------------------------------------------------------
def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")

    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        include_schemas=True,
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()


# ---------------------------------------------------------------------
# Online migrations
# ---------------------------------------------------------------------
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
            include_schemas=True,
            compare_type=True,
        )

        with context.begin_transaction():
            context.run_migrations()


# ---------------------------------------------------------------------
# Run migrations
# ---------------------------------------------------------------------
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()