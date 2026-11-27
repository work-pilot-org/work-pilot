from fastapi import APIRouter, Depends, Header, HTTPException
from pydantic import BaseModel, field_validator
from sqlalchemy.orm import Session

from shared_infrastructure.core.config import settings
from shared_infrastructure.database.base import TenantBase
from shared_infrastructure.database.schema_utils import validate_schema_name
from shared_infrastructure.database.session import get_db
from shared_infrastructure.database.tenant_session import set_public_schema

# Import ALL IT-service tenant models so TenantBase.metadata is complete
from it_service.modules.assets.models import Asset  # noqa: F401
from it_service.modules.helpdesk.models import (  # noqa: F401
    Ticket,
    TicketComment,
    TicketAttachment,
    TicketActivity,
)
from it_service.modules.devices.models import Device, DeviceMaintenanceHistory  # noqa: F401
from it_service.modules.access.models import AccessRequest  # noqa: F401
from it_service.modules.software.models import Software, InstalledSoftware, InstallationRequest  # noqa: F401
from it_service.modules.licenses.models import License, LicenseAssignment  # noqa: F401
from it_service.modules.maintenance.models import MaintenanceRecord  # noqa: F401

internal_router = APIRouter(
    prefix="/internal/tickets",
    tags=["Internal IT"],
)


def verify_internal_token(x_internal_token: str = Header(...)) -> None:
    if x_internal_token != settings.SECRET_KEY:
        raise HTTPException(status_code=403, detail="Invalid internal token")


class InitTenantRequest(BaseModel):
    schema_name: str

    @field_validator("schema_name")
    @classmethod
    def validate_schema_name_field(cls, value: str) -> str:
        if not value:
            raise ValueError("schema_name cannot be empty")
        if not (value[0].isalpha() or value[0] == "_"):
            raise ValueError("schema_name must start with a letter or underscore")
        if not all(ch.isalnum() or ch == "_" for ch in value):
            raise ValueError("schema_name must contain only letters, numbers, and underscores")
        return value


@internal_router.post(
    "/tenants/init",
    dependencies=[Depends(verify_internal_token)],
)
def init_tenant_tables(
    req: InitTenantRequest,
    db: Session = Depends(get_db),
) -> dict:
    """
    Create all IT-service tenant tables inside the given PostgreSQL schema.
    Called by auth-service after a new tenant schema has been created.
    """
    schema_name = validate_schema_name(req.schema_name)

    try:
        connection = db.connection()

        # Isolate to the tenant schema so create_all targets only it
        connection.exec_driver_sql(f'SET search_path TO "{schema_name}"')

        TenantBase.metadata.create_all(bind=connection)

        db.commit()

    finally:
        set_public_schema(db)

    return {"status": "ok"}
