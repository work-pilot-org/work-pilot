import io
import base64
import pyotp
import qrcode
from uuid import UUID
from jose import jwt, JWTError
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from src.core.config import settings
from src.core.email.email_service import EmailService
from src.modules.mfa.repository import MFARepository
from src.modules.user.repository import UserRepository
from src.modules.tenant.repository import TenantRepository
from src.modules.auth.schemas import LoginResponse
from src.core.security import create_access_token, create_refresh_token, create_sso_token

class MFAService:
    def __init__(self):
        self.mfa_repository = MFARepository()
        self.user_repository = UserRepository()
        self.tenant_repository = TenantRepository()
        self.email_service = EmailService()

    def setup_mfa(self, db: Session, user_id: UUID) -> dict:
        user = self.mfa_repository.get_user_by_id(db, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found.")

        # Generate secret
        secret = pyotp.random_base32()
        self.mfa_repository.update_mfa_secret(db, user_id, secret)
        db.commit()

        # Generate URI
        otpauth_url = pyotp.totp.TOTP(secret).provisioning_uri(
            name=user.email,
            issuer_name="WorkPilot"
        )

        # Generate base64 QR code image
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(otpauth_url)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        buffered = io.BytesIO()
        img.save(buffered, format="PNG")
        qr_code_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")

        return {
            "otpauth_url": otpauth_url,
            "qr_code": qr_code_base64
        }

    def verify_mfa(self, db: Session, code: str, mfa_token: str | None, current_user_id: UUID | None) -> tuple | None:
        user_id = current_user_id

        # Case 1: Verification during login (unauthenticated)
        if mfa_token:
            try:
                payload = jwt.decode(
                    mfa_token,
                    settings.SECRET_KEY,
                    algorithms=[settings.ALGORITHM]
                )
                if payload.get("type") != "mfa_pending":
                    raise HTTPException(status_code=401, detail="Invalid token type.")
                
                sub_val = payload.get("sub")
                if not sub_val:
                    raise HTTPException(status_code=401, detail="Invalid token payload.")
                
                user_id = UUID(sub_val)
            except JWTError:
                raise HTTPException(status_code=401, detail="Invalid or expired MFA token.")

        if not user_id:
            raise HTTPException(status_code=400, detail="User context missing.")

        user = self.mfa_repository.get_user_by_id(db, user_id)
        if not user or not user.mfa_secret:
            raise HTTPException(status_code=400, detail="MFA setup has not been initiated.")

        # Verify code
        totp = pyotp.TOTP(user.mfa_secret)
        if not totp.verify(code):
            raise HTTPException(status_code=400, detail="Invalid verification code.")

        # If it was a setup phase, enable MFA
        if not user.is_mfa_enabled:
            self.mfa_repository.enable_mfa(db, user_id)
            db.commit()
            self.email_service.send_mfa_enabled_email(user.email)
            return None

        # If verification is during login, generate and return final tokens
        profile = self.user_repository.get_user_profile(db, user.id)
        if not profile:
            raise HTTPException(status_code=400, detail="User profile not found.")

        tenant = self.tenant_repository.get_tenant_by_id(db, profile.tenant_id)
        if not tenant:
            raise HTTPException(status_code=400, detail="Tenant not found.")

        primary_domain = next((d.domain for d in tenant.domains if d.is_primary), tenant.domains[0].domain if tenant.domains else "localhost")

        token_data = {
            "sub": str(user.id),
            "email": user.email,
            "tenant_id": tenant.id,
            "schema_name": tenant.schema_name,
            "domain": primary_domain,
        }

        access_token = create_access_token(token_data)
        refresh_token = create_refresh_token(token_data)
        sso_token = create_sso_token(token_data)

        login_response = LoginResponse(
            access_token=access_token,
            user_id=str(user.id),
            email=user.email,
            tenant_id=tenant.id,
            schema_name=tenant.schema_name,
            company_name=tenant.company_name,
            domain=primary_domain,
            sso_token=sso_token,
        )

        return login_response, refresh_token

    def disable_mfa(self, db: Session, user_id: UUID, code: str) -> None:
        user = self.mfa_repository.get_user_by_id(db, user_id)
        if not user or not user.is_mfa_enabled or not user.mfa_secret:
            raise HTTPException(status_code=400, detail="MFA is not enabled.")

        totp = pyotp.TOTP(user.mfa_secret)
        if not totp.verify(code):
            raise HTTPException(status_code=400, detail="Invalid verification code.")

        self.mfa_repository.disable_mfa(db, user_id)
        db.commit()
        self.email_service.send_mfa_disabled_email(user.email)

    def get_mfa_status(self, db: Session, user_id: UUID) -> bool:
        user = self.mfa_repository.get_user_by_id(db, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found.")
        return user.is_mfa_enabled
