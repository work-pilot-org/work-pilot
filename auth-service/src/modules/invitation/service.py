import secrets
import hashlib
from datetime import datetime
from uuid import UUID
from fastapi import HTTPException
from sqlalchemy.orm import Session
from src.core.email.email_service import EmailService
from shared_infrastructure.core.security import hash_password
from shared_infrastructure.database.tenant_session import set_tenant_schema, set_public_schema

from src.modules.invitation.models import Invitation, InvitationStatus, default_expiry
from src.modules.invitation.repository import InvitationRepository
from src.modules.invitation.schemas import (
    InvitationCreateRequest, 
    AcceptInvitationRequest,
    InvitationValidateResponse
)
from src.modules.tenant.repository import TenantRepository
from src.modules.user.repository import UserRepository
from src.modules.user.models import User
from src.modules.employee.repository import EmployeeRepository
from src.modules.employee.models import Employee

class InvitationService:
    def __init__(self):
        self.repository = InvitationRepository()
        self.tenant_repo = TenantRepository()
        self.user_repo = UserRepository()
        self.employee_repo = EmployeeRepository()
        self.email_service = EmailService()

    def generate_token(self) -> str:
        return secrets.token_urlsafe(48)

    def hash_token(self, token: str) -> str:
        return hashlib.sha256(token.encode()).hexdigest()

    def create_invitation(
        self, 
        db: Session, 
        req: InvitationCreateRequest, 
        tenant_id: int, 
        actor_id: UUID,
        frontend_url: str
    ) -> Invitation:
        # Check if tenant exists
        tenant = self.tenant_repo.get_tenant_by_id(db, tenant_id)
        if not tenant:
            raise HTTPException(status_code=404, detail="Tenant not found")
            
        email = req.email.strip().lower()

        # Prevent duplicate pending invitations
        existing = self.repository.get_by_tenant_and_email(db, tenant_id, email)
        if existing:
            raise HTTPException(status_code=409, detail="A pending invitation already exists for this email.")

        # Check if user is already an employee
        user = self.user_repo.get_user_by_email(db, email)
        if user:
            # We must switch to the tenant schema to check employee
            try:
                set_tenant_schema(db, tenant.schema_name)
                emp = self.employee_repo.get_employee_by_user_id(db, user.id)
            finally:
                set_public_schema(db)
            if emp:
                raise HTTPException(status_code=409, detail="User is already an employee of this company.")

        raw_token = self.generate_token()
        token_hash = self.hash_token(raw_token)

        invitation = Invitation(
            tenant_id=tenant_id,
            email=email,
            role=req.role,
            token_hash=token_hash,
            status=InvitationStatus.PENDING,
            created_by=actor_id,
            expires_at=default_expiry()
        )

        self.repository.create_invitation(db, invitation)
        db.commit()

        # Send email (after commit to avoid inconsistent state if email fails)
        invite_link = f"{frontend_url}/accept-invitation/{raw_token}"
        try:
            self.email_service.send_invitation_email(
                email=email,
                invite_link=invite_link,
                company_name=tenant.company_name,
                role=req.role.value,
                expiry_date=invitation.expires_at.strftime("%Y-%m-%d %H:%M:%S UTC")
            )
            invitation.last_sent_at = datetime.utcnow()
            self.repository.update_invitation(db, invitation)
            db.commit()
        except Exception as e:
            # We don't rollback the DB because the invite is valid, just log it.
            print(f"Failed to send invitation email to {email}: {str(e)}")

        return invitation

    def validate_invitation(self, db: Session, token: str) -> InvitationValidateResponse:
        token_hash = self.hash_token(token)
        inv = self.repository.get_by_token_hash(db, token_hash)
        
        if not inv:
            return InvitationValidateResponse(
                valid=False, expired=False, revoked=False, user_exists=False
            )

        expired = inv.expires_at < datetime.utcnow()
        revoked = inv.status == InvitationStatus.REVOKED
        valid = inv.status == InvitationStatus.PENDING and not expired

        tenant = self.tenant_repo.get_tenant_by_id(db, inv.tenant_id)
        user = self.user_repo.get_user_by_email(db, inv.email)

        return InvitationValidateResponse(
            valid=valid,
            expired=expired,
            revoked=revoked,
            company_name=tenant.company_name if tenant else None,
            role=inv.role,
            user_exists=user is not None,
            email=inv.email
        )

    def accept_invitation(
        self, 
        db: Session, 
        req: AcceptInvitationRequest, 
        authenticated_user: User | None = None
    ):
        token_hash = self.hash_token(req.token)

        # 1. Begin transaction and lock row
        invitation = self.repository.get_by_token_hash_for_update(db, token_hash)
        if not invitation:
            raise HTTPException(status_code=404, detail="Invitation not found.")

        # 2. Validation
        if invitation.status != InvitationStatus.PENDING:
            db.rollback()
            raise HTTPException(status_code=400, detail="Invitation is no longer valid.")

        if invitation.expires_at < datetime.utcnow():
            invitation.status = InvitationStatus.EXPIRED
            db.commit()
            raise HTTPException(status_code=400, detail="Invitation has expired.")

        tenant = self.tenant_repo.get_tenant_by_id(db, invitation.tenant_id)
        if not tenant:
            db.rollback()
            raise HTTPException(status_code=404, detail="Tenant not found.")

        # 3. User check and creation
        existing_user = self.user_repo.get_user_by_email(db, invitation.email)
        
        if existing_user:
            if not authenticated_user or authenticated_user.id != existing_user.id:
                db.rollback()
                raise HTTPException(
                    status_code=401, 
                    detail="This email belongs to an existing user. Please log in to accept the invitation."
                )
            target_user = existing_user
        else:
            if authenticated_user and authenticated_user.email != invitation.email:
                db.rollback()
                raise HTTPException(
                    status_code=401,
                    detail="You are authenticated with a different email. Please log out to accept this invitation."
                )
            # Create user
            hashed_pwd = hash_password(req.password)
            target_user = User(
                email=invitation.email,
                hashed_password=hashed_pwd,
                full_name=req.full_name,
                is_active=True
            )
            self.user_repo.create_user(db, target_user)
            db.flush()

        # 4. Employee creation in tenant schema
        try:
            set_tenant_schema(db, tenant.schema_name)
            
            # Check if already employee
            if self.employee_repo.get_employee_by_user_id(db, target_user.id):
                db.rollback()
                raise HTTPException(status_code=409, detail="User is already an employee of this company.")

            emp = Employee(
                user_id=target_user.id,
                full_name=target_user.full_name,
                email=target_user.email,
                role=invitation.role
            )
            self.employee_repo.create_employee(db, emp)
            db.flush()

        finally:
            # 5. Invitation status update
            set_public_schema(db)
            
        invitation.status = InvitationStatus.ACCEPTED
        invitation.accepted_by_user_id = target_user.id
        self.repository.update_invitation(db, invitation)

        # 6. Commit
        try:
            db.commit()
        except Exception:
            db.rollback()
            raise HTTPException(status_code=500, detail="Failed to accept invitation due to a server error.")

        return {"message": "Invitation accepted successfully."}
