from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from it_service.core.config import settings
from it_service.core.rbac import Permission, get_permissions_for_roles
from it_service.infrastructure.database.session import get_db
from it_service.infrastructure.database.tenant_session import set_tenant_schema

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/swagger-login")

def get_current_user_and_set_schema(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> dict:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(
            token, 
            settings.SECRET_KEY, 
            algorithms=[settings.ALGORITHM]
        )
        schema_name: str = payload.get("schema_name")
        if schema_name is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    set_tenant_schema(db, schema_name)
    return payload

def require_permissions(required_permissions: list[Permission]):
    def permission_dependency(
        current_user: dict = Depends(get_current_user_and_set_schema)
    ):
        roles = current_user.get("roles", [])
        user_perms = get_permissions_for_roles(roles)
        
        if Permission.ADMIN_ALL in user_perms:
            return current_user
            
        if not all(p in user_perms for p in required_permissions):
            raise HTTPException(status_code=403, detail="Forbidden: Insufficient permissions")
        return current_user
    return permission_dependency

from uuid import UUID


def verify_ticket_ownership(
    ticket_id: UUID,
    current_user: dict,
    db: Session,
    bypass_permissions: list[Permission] = None,
):
    roles = current_user.get("roles", [])
    user_perms = get_permissions_for_roles(roles)
    
    if Permission.ADMIN_ALL in user_perms:
        return
        
    if bypass_permissions and any(p in user_perms for p in bypass_permissions):
        return
        
    auth_user_id = current_user.get("sub")
    if not auth_user_id:
        raise HTTPException(status_code=401, detail="Unauthorized: Invalid token payload")
        
    from it_service.modules.helpdesk.models.ticket import Ticket
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    
    if not ticket or str(ticket.requester_id) != str(auth_user_id):
        raise HTTPException(status_code=403, detail="Forbidden: You do not own this ticket")

# Access
from it_service.modules.access.repository import AccessRequestRepository
from it_service.modules.access.service import AccessService

# Assets
from it_service.modules.assets.repository import AssetRepository
from it_service.modules.assets.service import AssetService

# Devices
from it_service.modules.devices.repository import (
    DeviceMaintenanceHistoryRepository,
    DeviceRepository,
)
from it_service.modules.devices.service import DeviceService
from it_service.modules.helpdesk.activity_repository import TicketActivityRepository
from it_service.modules.helpdesk.activity_service import ActivityService

# Help Desk
from it_service.modules.helpdesk.repository import TicketRepository
from it_service.modules.helpdesk.service import TicketService

# Licenses
from it_service.modules.licenses.repository import LicenseAssignmentRepository, LicenseRepository
from it_service.modules.licenses.service import LicenseService

# Maintenance
from it_service.modules.maintenance.repository import MaintenanceRepository
from it_service.modules.maintenance.service import MaintenanceService

# Software
from it_service.modules.software.repository import (
    InstallationRequestRepository,
    InstalledSoftwareRepository,
    SoftwareRepository,
)
from it_service.modules.software.service import SoftwareService

# ==========================================================
# Database
# ==========================================================

def get_database() -> Session:
    """
    Returns the current database session.
    """
    return Depends(get_db)


# ==========================================================
# Repositories
# ==========================================================

def get_ticket_repository() -> TicketRepository:
    return TicketRepository()


def get_activity_repository() -> TicketActivityRepository:
    return TicketActivityRepository()


def get_asset_repository() -> AssetRepository:
    return AssetRepository()


def get_device_repository() -> DeviceRepository:
    return DeviceRepository()


def get_device_maintenance_repository() -> DeviceMaintenanceHistoryRepository:
    return DeviceMaintenanceHistoryRepository()


def get_software_repository() -> SoftwareRepository:
    return SoftwareRepository()


def get_installed_software_repository() -> InstalledSoftwareRepository:
    return InstalledSoftwareRepository()


def get_installation_request_repository() -> InstallationRequestRepository:
    return InstallationRequestRepository()


def get_license_repository() -> LicenseRepository:
    return LicenseRepository()


def get_license_assignment_repository() -> LicenseAssignmentRepository:
    return LicenseAssignmentRepository()


def get_access_repository() -> AccessRequestRepository:
    return AccessRequestRepository()


def get_maintenance_repository() -> MaintenanceRepository:
    return MaintenanceRepository()


# ==========================================================
# Services
# ==========================================================

def get_activity_service(
    repository: TicketActivityRepository = Depends(get_activity_repository),
) -> ActivityService:
    return ActivityService(repository)


def get_ticket_service(
    repository: TicketRepository = Depends(get_ticket_repository),
    activity_service: ActivityService = Depends(get_activity_service),
) -> TicketService:
    return TicketService(
        repository=repository,
        activity_service=activity_service,
    )


def get_asset_service(
    repository: AssetRepository = Depends(get_asset_repository),
) -> AssetService:
    return AssetService(repository=repository)


def get_device_service(
    repository: DeviceRepository = Depends(get_device_repository),
    maintenance_repository: DeviceMaintenanceHistoryRepository = Depends(get_device_maintenance_repository),
) -> DeviceService:
    return DeviceService(
        repository=repository,
        maintenance_repository=maintenance_repository,
    )


def get_software_service(
    repository: SoftwareRepository = Depends(get_software_repository),
    installed_repository: InstalledSoftwareRepository = Depends(get_installed_software_repository),
    request_repository: InstallationRequestRepository = Depends(get_installation_request_repository),
) -> SoftwareService:
    return SoftwareService(
        repository=repository,
        installed_repository=installed_repository,
        request_repository=request_repository,
    )


def get_license_service(
    repository: LicenseRepository = Depends(get_license_repository),
    assignment_repository: LicenseAssignmentRepository = Depends(get_license_assignment_repository),
) -> LicenseService:
    return LicenseService(
        repository=repository,
        assignment_repository=assignment_repository,
    )


def get_access_service(
    repository: AccessRequestRepository = Depends(get_access_repository),
) -> AccessService:
    return AccessService(repository=repository)


def get_maintenance_service(
    repository: MaintenanceRepository = Depends(get_maintenance_repository),
) -> MaintenanceService:
    return MaintenanceService(repository=repository)