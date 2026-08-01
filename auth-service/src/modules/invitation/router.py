from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from typing import List

from src.infrastructure.database.session import get_db
from src.core.dependencies import require_permissions
from src.core.rbac import Permission
from src.modules.invitation.schemas import (
    InvitationCreateRequest,
    InvitationResponse,
    InvitationValidateResponse,
    AcceptInvitationRequest
)
from src.modules.invitation.service import InvitationService
from src.modules.user.repository import UserRepository
from src.modules.invitation.repository import InvitationRepository
from src.modules.invitation.models import InvitationStatus

from jose import jwt, JWTError
from src.core.config import settings

router = APIRouter(
    prefix="/invitations",
    tags=["Invitations"],
)

invitation_service = InvitationService()
invitation_repo = InvitationRepository()
user_repo = UserRepository()


@router.post(
    "",
    response_model=InvitationResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_invitation(
    req: InvitationCreateRequest,
    request: Request,
    current_user_payload: dict = Depends(require_permissions([Permission.EMPLOYEE_MANAGE])),
    db: Session = Depends(get_db),
):
    """
    Create a new employee invitation (Admin only).
    """
    tenant_id = current_user_payload.get("tenant_id")
    actor_id = UUID(current_user_payload.get("sub"))
    
    # We need the frontend URL to construct the invite link. For now, assume it's passed or env var.
    frontend_url = getattr(settings, "FRONTEND_URL", "http://localhost:3000")

    return invitation_service.create_invitation(
        db=db,
        req=req,
        tenant_id=tenant_id,
        actor_id=actor_id,
        frontend_url=frontend_url
    )


@router.get(
    "",
    response_model=List[InvitationResponse],
    status_code=status.HTTP_200_OK,
)
def list_pending_invitations(
    current_user_payload: dict = Depends(require_permissions([Permission.EMPLOYEE_MANAGE])),
    db: Session = Depends(get_db),
):
    """
    List pending invitations for the current tenant (Admin only).
    """
    tenant_id = current_user_payload.get("tenant_id")
    return invitation_repo.get_pending_by_tenant(db, tenant_id)


@router.post(
    "/{invitation_id}/resend",
    response_model=InvitationResponse,
    status_code=status.HTTP_200_OK,
)
def resend_invitation(
    invitation_id: UUID,
    request: Request,
    current_user_payload: dict = Depends(require_permissions([Permission.EMPLOYEE_MANAGE])),
    db: Session = Depends(get_db),
):
    """
    Resend an invitation email with a fresh token.
    """
    tenant_id = current_user_payload.get("tenant_id")
    
    inv = invitation_repo.get_by_id(db, invitation_id)
    if not inv or inv.tenant_id != tenant_id:
        raise HTTPException(status_code=404, detail="Invitation not found.")
        
    if inv.status != InvitationStatus.PENDING:
        raise HTTPException(status_code=400, detail="Only pending invitations can be resent.")
        
    # Generate new token
    raw_token = invitation_service.generate_token()
    token_hash = invitation_service.hash_token(raw_token)
    
    inv.token_hash = token_hash
    # You could optionally extend the expiry date here
    
    frontend_url = getattr(settings, "FRONTEND_URL", "http://localhost:3000")
    invite_link = f"{frontend_url}/accept-invitation/{raw_token}"
    
    # Send email
    try:
        invitation_service.email_service.send_invitation_email(
            email=inv.email,
            invite_link=invite_link,
            company_name="WorkPilot", # Should ideally fetch Tenant name
            role=inv.role.value,
            expiry_date=inv.expires_at.strftime("%Y-%m-%d %H:%M:%S UTC")
        )
        import datetime
        inv.last_sent_at = datetime.datetime.utcnow()
        invitation_repo.update_invitation(db, inv)
        db.commit()
    except Exception as e:
        print(f"Failed to resend invitation email to {inv.email}: {str(e)}")
        
    return inv


@router.post(
    "/{invitation_id}/revoke",
    response_model=InvitationResponse,
    status_code=status.HTTP_200_OK,
)
def revoke_invitation(
    invitation_id: UUID,
    current_user_payload: dict = Depends(require_permissions([Permission.EMPLOYEE_MANAGE])),
    db: Session = Depends(get_db),
):
    """
    Revoke a pending invitation.
    """
    tenant_id = current_user_payload.get("tenant_id")
    
    inv = invitation_repo.get_by_id(db, invitation_id)
    if not inv or inv.tenant_id != tenant_id:
        raise HTTPException(status_code=404, detail="Invitation not found.")
        
    if inv.status != InvitationStatus.PENDING:
        raise HTTPException(status_code=400, detail="Only pending invitations can be revoked.")
        
    import datetime
    inv.status = InvitationStatus.REVOKED
    inv.revoked_at = datetime.datetime.utcnow()
    
    invitation_repo.update_invitation(db, inv)
    db.commit()
    
    return inv


# --- Public / Hybrid Endpoints ---

@router.get(
    "/validate/{token}",
    response_model=InvitationValidateResponse,
    status_code=status.HTTP_200_OK,
)
def validate_invitation(
    token: str,
    db: Session = Depends(get_db),
):
    """
    Validate an invitation token and return details to populate the frontend.
    """
    return invitation_service.validate_invitation(db, token)


def get_optional_current_user(
    request: Request,
    db: Session
):
    """
    Helper to extract user from Authorization header if present.
    """
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return None
        
    token = auth_header.split(" ")[1]
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id = payload.get("sub")
        if user_id:
            return user_repo.get_user_by_id(db, UUID(user_id))
    except JWTError:
        pass
    return None


@router.post(
    "/accept",
    status_code=status.HTTP_200_OK,
)
def accept_invitation(
    req: AcceptInvitationRequest,
    request: Request,
    db: Session = Depends(get_db),
):
    """
    Accept an invitation. 
    If the email already belongs to a user, they must be authenticated (JWT passed in Authorization header).
    """
    authenticated_user = get_optional_current_user(request, db)
    return invitation_service.accept_invitation(db, req, authenticated_user)
