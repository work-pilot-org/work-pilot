from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr

from shared_infrastructure.database.session import get_db
from shared_infrastructure.core.config import settings
from src.modules.invitation.schemas import InvitationCreateRequest
from src.modules.invitation.service import InvitationService

internal_router = APIRouter(
    prefix="/internal/invitations",
    tags=["Internal Invitations"],
)

def verify_internal_token(x_internal_token: str = Header(...)):
    if x_internal_token != settings.SECRET_KEY:
        raise HTTPException(status_code=403, detail="Invalid internal token")

class InternalInvitationCreate(BaseModel):
    email: EmailStr
    role: str
    employee_id: UUID

@internal_router.post("", dependencies=[Depends(verify_internal_token)])
def create_invitation_internally(
    req: InternalInvitationCreate,
    x_tenant_id: int = Header(...),
    x_actor_id: str = Header(...),
    db: Session = Depends(get_db)
):
    service = InvitationService()
    
    frontend_url = settings.FRONTEND_URL
    
    # We map InternalInvitationCreate to InvitationCreateRequest
    from src.modules.invitation.schemas import InvitationCreateRequest
    from src.modules.employee.models import Role
    
    mapped_req = InvitationCreateRequest(
        email=req.email,
        role=Role(req.role),
        employee_id=req.employee_id
    )
    
    try:
        invitation = service.create_invitation(
            db=db,
            req=mapped_req,
            tenant_id=x_tenant_id,
            actor_id=UUID(x_actor_id),
            frontend_url=frontend_url
        )
        return {"status": "ok", "invitation_id": str(invitation.id)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
