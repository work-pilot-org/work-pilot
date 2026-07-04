import re

from sqlalchemy.orm import Session

from src.core.exceptions import (
    CompanyAlreadyExistsException,
    DomainAlreadyExistsException,
    EmailAlreadyExistsException,
)

from src.modules.auth.schemas import (
    RegisterRequest,
    RegisterResponse,
)
from src.modules.employee.repository import EmployeeRepository
from src.modules.tenant.repository import TenantRepository
from src.modules.user.repository import UserRepository

from src.core.security import hash_password

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



class AuthService:

    def __init__(self):

        self.tenant_repository = TenantRepository()
        self.user_repository = UserRepository()
        self.employee_repository = EmployeeRepository()

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

        return f"{company}.workpilot.com"
    
    
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

        