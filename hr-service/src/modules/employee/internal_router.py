from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Header, Request
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr

from shared_infrastructure.database.session import get_db
from shared_infrastructure.database.tenant_session import set_tenant_schema, set_public_schema
from shared_infrastructure.core.config import settings
from src.modules.employee.models import Employee
from src.modules.employee.repository import EmployeeRepository
from shared_infrastructure.database.base import TenantBase

internal_router = APIRouter(
    prefix="/internal/employees",
    tags=["Internal Employees"],
)

def verify_internal_token(x_internal_token: str = Header(...)):
    if x_internal_token != settings.SECRET_KEY:
        raise HTTPException(status_code=403, detail="Invalid internal token")

class InitTenantRequest(BaseModel):
    schema_name: str

@internal_router.post("/tenants/init", dependencies=[Depends(verify_internal_token)])
def init_tenant_tables(
    req: InitTenantRequest,
    db: Session = Depends(get_db)
):
    from sqlalchemy import text
    # Import all models to ensure they are registered with TenantBase
    import src.modules.employee.models
    import src.modules.leave.models
    import src.modules.attendance.models
    import src.modules.policies.models
    import src.modules.organization.models
    
    connection = db.connection()
    connection.execute(text(f'SET search_path TO "{req.schema_name}"'))
    TenantBase.metadata.create_all(bind=connection)
    db.commit()
    db.execute(text(f'SET search_path TO "{req.schema_name}", public'))
    return {"status": "ok"}


class AdminCreateRequest(BaseModel):
    auth_user_id: UUID
    first_name: str
    last_name: str
    email: EmailStr
    role: str
    schema_name: str

class LinkUserRequest(BaseModel):
    auth_user_id: UUID
    schema_name: str

@internal_router.post("/admin", dependencies=[Depends(verify_internal_token)])
def create_org_admin(
    req: AdminCreateRequest,
    x_tenant_id: int = Header(...),
    db: Session = Depends(get_db)
):
    try:
        set_tenant_schema(db, req.schema_name)
        repo = EmployeeRepository(db)
        
        import random
        employee = Employee(
            auth_user_id=req.auth_user_id,
            employee_code=f"EMP-ADMIN-{random.randint(1000, 9999)}",
            first_name=req.first_name,
            last_name=req.last_name,
            joining_date="2026-08-01",
            employment_type="FULL_TIME",
            invitation_status="ACCEPTED"
        )
        repo.create_employee(employee)
        db.commit()
    finally:
        set_public_schema(db)
        
    return {"status": "ok"}

@internal_router.post("/{employee_id}/link-user", dependencies=[Depends(verify_internal_token)])
def link_user(
    employee_id: UUID,
    req: LinkUserRequest,
    x_tenant_id: int = Header(...),
    db: Session = Depends(get_db)
):
    try:
        set_tenant_schema(db, req.schema_name)
        repo = EmployeeRepository(db)
        employee = repo.get_employee_by_id(employee_id)
        if not employee:
            raise HTTPException(status_code=404, detail="Employee not found")
            
        employee.auth_user_id = req.auth_user_id
        employee.invitation_status = "ACCEPTED"
        repo.update_employee(employee)
        db.commit()
    finally:
        set_public_schema(db)
        
    return {"status": "ok"}
