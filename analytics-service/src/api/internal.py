from fastapi import APIRouter, Depends, Header, HTTPException
from pydantic import BaseModel, field_validator
from sqlalchemy.orm import Session
from sqlalchemy import text
from alembic import command
from alembic.config import Config

from shared_infrastructure.core.config import settings
from shared_infrastructure.database.session import get_db

import os

internal_router = APIRouter(
    prefix="/internal/analytics",
    tags=["Internal Analytics"],
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
    Run alembic migrations to create analytics tables inside the given PostgreSQL schema.
    Called by auth-service after a new tenant schema has been created.
    """
    schema_name = req.schema_name

    # Set up Alembic config
    alembic_cfg = Config("alembic.ini")
    alembic_cfg.set_main_option("sqlalchemy.url", str(settings.DATABASE_URL))

    connection = db.connection()
    try:
        connection.execute(text(f'SET search_path TO "{schema_name}"'))
        # Important: pass connection to context so alembic uses the current search_path
        alembic_cfg.attributes['connection'] = connection
        
        command.upgrade(alembic_cfg, "head")
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    
    return {"status": "ok"}
