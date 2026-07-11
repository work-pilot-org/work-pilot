import re

from sqlalchemy.orm import Session

from src.core.exceptions import (
    CompanyAlreadyExistsException,
    DomainAlreadyExistsException,
    EmailAlreadyExistsException,
    InvalidCredentialsException,
)

from src.modules.auth.schemas import (
    RegisterRequest,
    RegisterResponse,
    LoginRequest,
    LoginResponse,
    MFASetupResponse,
    MFAEnableRequest,
    MFADisableRequest,
    MFALoginRequest,
    PreAuthResponse,
)
from src.modules.employee.repository import EmployeeRepository
from src.modules.tenant.repository import TenantRepository
from src.modules.user.repository import UserRepository

from src.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    create_preauth_token,
    verify_preauth_token,
)

from src.modules.tenant.models import (
    Tenant,
    Domain,
)

from src.modules.user.models import (
    User,
    UserProfile,
)

from src.infrastructure.database.schema_manager import SchemaManager
from src.infrastructure.database.tenant_session import (
    set_tenant_schema,
    set_public_schema,
)

from src.modules.employee.models import (
    Employee,
    Role,
)

from src.modules.password_reset.service import PasswordResetService
from src.modules.password_reset.schemas import (
    ForgotPasswordRequest,
    ResetPasswordRequest,
)


class AuthService:

    def __init__(self):

        self.tenant_repository = TenantRepository()
        self.user_repository = UserRepository()
        self.employee_repository = EmployeeRepository()
        self.password_reset_service = PasswordResetService()
    # --------------------------------------------------
    # Validation Helpers
    # --------------------------------------------------

    def _validate_company(
        self,
        db: Session,
        company_name: str,
    ) -> None:

        tenant = self.tenant_repository.get_by_company_name(
            db,
            company_name,
        )

        if tenant:
            raise CompanyAlreadyExistsException(
                "Company already exists."
            )

    def _validate_email(
        self,
        db: Session,
        email: str,
    ) -> None:

        user = self.user_repository.get_user_by_email(
            db,
            email,
        )

        if user:
            raise EmailAlreadyExistsException(
                "Email already exists."
            )

    def _validate_domain(
        self,
        db: Session,
        domain: str,
    ) -> None:

        existing_domain = self.tenant_repository.get_domain(
            db,
            domain,
        )

        if existing_domain:
            raise DomainAlreadyExistsException(
                "Domain already exists."
            )

    # --------------------------------------------------
    # Helper Methods
    # --------------------------------------------------

    def _generate_schema_name(
        self,
        company_name: str,
    ) -> str:
        """
        Example:
        OpenAI India

        becomes

        tenant_openai_india
        """

        company = company_name.strip().lower()

        company = re.sub(
            r"[^a-z0-9]+",
            "_",
            company,
        )

        company = re.sub(
            r"_+",
            "_",
            company,
        ).strip("_")

        return f"tenant_{company}"

    def _generate_domain(
        self,
        company_name: str,
    ) -> str:
        """
        Example:

        OpenAI India

        becomes

        openai-india.workpilot.com
        """

        company = company_name.strip().lower()

        company = re.sub(
            r"[^a-z0-9]+",
            "-",
            company,
        )

        company = re.sub(
            r"-+",
            "-",
            company,
        ).strip("-")

        return company
    
    
    def register(
        self,
        db: Session,
        request: RegisterRequest,
    ) -> RegisterResponse:
        """
        Register a new company with its first organization admin.
        """

        try:

            # ------------------------------------------
            # Validate Company & Email
            # ------------------------------------------

            self._validate_company(
                db,
                request.company_name,
            )

            self._validate_email(
                db,
                request.email,
            )

            # ------------------------------------------
            # Generate Schema & Domain
            # ------------------------------------------

            schema_name = self._generate_schema_name(
                request.company_name,
            )

            domain = self._generate_domain(
                request.company_name,
            )

            self._validate_domain(
                db,
                domain,
            )

            # ------------------------------------------
            # Hash Password
            # ------------------------------------------

            hashed_password = hash_password(
                request.password,
            )

            # ------------------------------------------
            # Create Tenant
            # ------------------------------------------

            tenant = Tenant(
                company_name=request.company_name,
                schema_name=schema_name,
            )

            tenant = self.tenant_repository.create_tenant(
                db,
                tenant,
            )

            # ------------------------------------------
            # Create Domain
            # ------------------------------------------

            tenant_domain = Domain(
                tenant_id=tenant.id,
                domain=domain,
                is_primary=True,
            )

            self.tenant_repository.create_domain(
                db,
                tenant_domain,
            )

            # ------------------------------------------
            # Create User
            # ------------------------------------------

            user = User(
                email=request.email,
                password=hashed_password,
            )

            user = self.user_repository.create_user(
                db,
                user,
            )

            # ------------------------------------------
            # Create User Profile
            # ------------------------------------------

            profile = UserProfile(
                user_id=user.id,
                tenant_id=tenant.id,
                full_name=request.full_name,
            )

            self.user_repository.create_user_profile(
                db,
                profile,
            )

                        # ------------------------------------------
            # Create Tenant Schema
            # ------------------------------------------

            SchemaManager.create_schema(
                db,
                schema_name,
            )

            # ------------------------------------------
            # Switch to Tenant Schema
            # ------------------------------------------

            set_tenant_schema(
                db,
                schema_name,
            )

            # ------------------------------------------
            # Create Tenant Tables
            # ------------------------------------------

            SchemaManager.create_tenant_tables(
                db,
            )

            # ------------------------------------------
            # Create Organization Admin Employee
            # ------------------------------------------

            employee = Employee(
                user_id=user.id,
                full_name=request.full_name,
                email=request.email,
                role=Role.ORG_ADMIN,
            )

            self.employee_repository.create_employee(
                db,
                employee,
            )

            # ------------------------------------------
            # Switch Back to Public Schema
            # ------------------------------------------

            set_public_schema(
                db,
            )

            # ------------------------------------------
            # Commit Transaction
            # ------------------------------------------

            db.commit()

            # ------------------------------------------
            # Return Response
            # ------------------------------------------

            return RegisterResponse(
                message="Registration completed successfully.",
                tenant_id=tenant.id,
                company_name=tenant.company_name,
                domain=domain,
            )

        except Exception:

            db.rollback()

            set_public_schema(
                db,
            )

            raise

    def login(
        self,
        db: Session,
        request: LoginRequest,
    ) -> tuple[LoginResponse, str] | tuple[PreAuthResponse, None]:
        """
        Authenticate user. If MFA is enabled, return PreAuthResponse.
        Otherwise, return LoginResponse and refresh token.
        """
        
        # 1. Find user by email
        user = self.user_repository.get_user_by_email(db, request.email)
        if not user:
            raise InvalidCredentialsException("Invalid email or password.")
            
        # 2. Verify password
        if not verify_password(request.password, user.password):
            raise InvalidCredentialsException("Invalid email or password.")
            
        # 3. Get User Profile to find Tenant ID
        profile = self.user_repository.get_user_profile(db, user.id)
        if not profile:
            raise InvalidCredentialsException("User profile not found.")
            
        # 4. Get Tenant to find Schema Name
        tenant = self.tenant_repository.get_tenant_by_id(db, profile.tenant_id)
        if not tenant:
            raise InvalidCredentialsException("Tenant not found.")
            
        # 5. Extract Primary Domain
        primary_domain = next((d.domain for d in tenant.domains if d.is_primary), tenant.domains[0].domain if tenant.domains else "localhost")
        
        # 6. Create JWT payload
        token_data = {
            "sub": str(user.id),
            "email": user.email,
            "tenant_id": tenant.id,
            "schema_name": tenant.schema_name,
            "domain": primary_domain,
        }

        # 7. Check if MFA is enabled
        if user.is_mfa_enabled:
            preauth_token = create_preauth_token(token_data)
            return PreAuthResponse(preauth_token=preauth_token), None
        
        access_token = create_access_token(token_data)
        from src.core.security import create_refresh_token, create_sso_token
        refresh_token = create_refresh_token(token_data)
        sso_token = create_sso_token(token_data)
        
        return LoginResponse(
            access_token=access_token,
            user_id=str(user.id),
            email=user.email,
            tenant_id=tenant.id,
            schema_name=tenant.schema_name,
            company_name=tenant.company_name,
            domain=primary_domain,
            is_mfa_enabled=False,
            sso_token=sso_token,
        ), refresh_token

    def exchange_sso_token(
        self,
        db: Session,
        sso_token: str,
    ) -> str:
        from jose import jwt, JWTError
        from src.core.config import settings
        from src.core.security import create_refresh_token
        
        try:
            payload = jwt.decode(
                sso_token,
                settings.SECRET_KEY,
                algorithms=[settings.ALGORITHM]
            )
            if payload.get("type") != "sso":
                raise InvalidCredentialsException("Invalid token type.")
            
            user_id = payload.get("sub")
            if not user_id:
                raise InvalidCredentialsException("Invalid token payload.")
                
            user = self.user_repository.get_user_by_id(db, user_id)
            if not user:
                raise InvalidCredentialsException("User not found.")
                
            profile = self.user_repository.get_user_profile(db, user.id)
            tenant = self.tenant_repository.get_tenant_by_id(db, profile.tenant_id)
            primary_domain = next((d.domain for d in tenant.domains if d.is_primary), tenant.domains[0].domain if tenant.domains else "localhost")
            
            token_data = {
                "sub": str(user.id),
                "email": user.email,
                "tenant_id": tenant.id,
                "schema_name": tenant.schema_name,
                "domain": primary_domain,
            }
            
            return create_refresh_token(token_data)
            
        except JWTError:
            raise InvalidCredentialsException("Invalid or expired SSO token.")

    def refresh_access_token(
        self,
        db: Session,
        refresh_token: str,
    ) -> LoginResponse:
        from jose import jwt, JWTError
        from src.core.config import settings
        
        try:
            payload = jwt.decode(
                refresh_token,
                settings.SECRET_KEY,
                algorithms=[settings.ALGORITHM]
            )
            if payload.get("type") != "refresh":
                raise InvalidCredentialsException("Invalid token type.")
            
            user_id = payload.get("sub")
            if not user_id:
                raise InvalidCredentialsException("Invalid token payload.")
                
            user = self.user_repository.get_user_by_id(db, user_id)
            if not user:
                raise InvalidCredentialsException("User not found.")
                
            profile = self.user_repository.get_user_profile(db, user.id)
            tenant = self.tenant_repository.get_tenant_by_id(db, profile.tenant_id)
            
            primary_domain = next((d.domain for d in tenant.domains if d.is_primary), tenant.domains[0].domain if tenant.domains else "localhost")
            
            token_data = {
                "sub": str(user.id),
                "email": user.email,
                "tenant_id": tenant.id,
                "schema_name": tenant.schema_name,
                "domain": primary_domain,
            }
            
            new_access_token = create_access_token(token_data)
            from src.core.security import create_sso_token
            sso_token = create_sso_token(token_data)
            
            return LoginResponse(
                access_token=new_access_token,
                user_id=str(user.id),
                email=user.email,
                tenant_id=tenant.id,
                schema_name=tenant.schema_name,
                company_name=tenant.company_name,
                domain=primary_domain,
                is_mfa_enabled=user.is_mfa_enabled,
                sso_token=sso_token,
            )
            
        except JWTError:
            raise InvalidCredentialsException("Invalid or expired refresh token.")

    # --------------------------------------------------
    # MFA Methods
    # --------------------------------------------------

    def setup_mfa(self, db: Session, user_id: str) -> MFASetupResponse:
        import pyotp
        
        user = self.user_repository.get_user_by_id(db, user_id)
        if not user:
            raise Exception("User not found.")
            
        if user.is_mfa_enabled:
            raise Exception("MFA_ALREADY_ENABLED")
            
        secret = pyotp.random_base32()
        user.mfa_secret = secret
        
        db.add(user)
        db.commit()
        
        provisioning_uri = pyotp.totp.TOTP(secret).provisioning_uri(
            name=user.email,
            issuer_name="WorkPilot"
        )
        
        return MFASetupResponse(
            secret=secret,
            provisioning_uri=provisioning_uri
        )

    def enable_mfa(self, db: Session, user_id: str, request: MFAEnableRequest) -> dict:
        import pyotp
        from datetime import datetime, timezone
        
        user = self.user_repository.get_user_by_id(db, user_id)
        if not user or not user.mfa_secret:
            raise Exception("MFA_SETUP_REQUIRED")
            
        if user.is_mfa_enabled:
            raise Exception("MFA_ALREADY_ENABLED")
            
        totp = pyotp.TOTP(user.mfa_secret)
        if not totp.verify(request.code):
            raise Exception("INVALID_MFA_CODE")
            
        user.is_mfa_enabled = True
        user.mfa_enabled_at = datetime.now(timezone.utc)
        
        db.add(user)
        db.commit()
        
        return {"message": "MFA enabled successfully."}

    def disable_mfa(self, db: Session, user_id: str, request: MFADisableRequest) -> dict:
        import pyotp
        
        user = self.user_repository.get_user_by_id(db, user_id)
        if not user:
            raise Exception("User not found.")
            
        if not user.is_mfa_enabled:
            raise Exception("MFA_NOT_ENABLED")
            
        if not verify_password(request.password, user.password):
            raise InvalidCredentialsException("Invalid credentials.")
            
        totp = pyotp.TOTP(user.mfa_secret)
        if not totp.verify(request.code):
            raise Exception("INVALID_MFA_CODE")
            
        user.is_mfa_enabled = False
        user.mfa_secret = None
        user.mfa_enabled_at = None
        user.mfa_last_used_at = None
        
        db.add(user)
        db.commit()
        
        return {"message": "MFA disabled successfully."}

    def login_mfa(self, db: Session, request: MFALoginRequest) -> tuple[LoginResponse, str]:
        import pyotp
        from datetime import datetime, timezone
        from src.core.security import create_sso_token, create_refresh_token
        
        try:
            payload = verify_preauth_token(request.preauth_token)
        except ValueError as e:
            raise Exception("INVALID_PREAUTH_TOKEN")
            
        user_id = payload.get("sub")
        if not user_id:
            raise Exception("INVALID_PREAUTH_TOKEN")
            
        user = self.user_repository.get_user_by_id(db, user_id)
        if not user:
            raise Exception("User not found.")
            
        if not user.is_mfa_enabled or not user.mfa_secret:
            raise Exception("MFA_NOT_ENABLED")
            
        totp = pyotp.TOTP(user.mfa_secret)
        if not totp.verify(request.code):
            raise Exception("INVALID_MFA_CODE")
            
        user.mfa_last_used_at = datetime.now(timezone.utc)
        db.add(user)
        db.commit()
        
        token_data = {
            "sub": str(user.id),
            "email": user.email,
            "tenant_id": payload.get("tenant_id"),
            "schema_name": payload.get("schema_name"),
            "domain": payload.get("domain"),
        }
        
        access_token = create_access_token(token_data)
        refresh_token = create_refresh_token(token_data)
        sso_token = create_sso_token(token_data)
        
        tenant = self.tenant_repository.get_tenant_by_id(db, payload.get("tenant_id"))
        
        login_response = LoginResponse(
            access_token=access_token,
            user_id=str(user.id),
            email=user.email,
            tenant_id=tenant.id,
            schema_name=tenant.schema_name,
            company_name=tenant.company_name,
            domain=payload.get("domain"),
            is_mfa_enabled=True,
            sso_token=sso_token,
        )
        
        return login_response, refresh_token