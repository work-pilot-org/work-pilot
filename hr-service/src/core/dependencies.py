from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from src.core.config import settings
from src.core.rbac import Permission, get_permissions_for_roles
from src.infrastructure.database.session import get_db
from src.infrastructure.database.tenant_session import set_tenant_schema

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

from src.modules.employee.models import Employee


def verify_employee_ownership(
    target_employee_id: UUID,
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
        
    employee = db.query(Employee).filter(Employee.id == target_employee_id).first()
    
    if not employee or str(employee.auth_user_id) != str(auth_user_id):
        raise HTTPException(status_code=403, detail="Forbidden: You do not own this resource")

