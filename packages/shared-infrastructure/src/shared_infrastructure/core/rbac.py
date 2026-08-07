from enum import Enum


class Role(str, Enum):
    TENANT_ADMIN = "TENANT_ADMIN"
    HR_ADMIN = "HR_ADMIN"
    IT_ADMIN = "IT_ADMIN"
    MANAGER = "MANAGER"
    EMPLOYEE = "EMPLOYEE"

class Permission(str, Enum):
    # Admin
    ADMIN_ALL = "admin:all"
    
    # HR & Organization
    HR_MANAGE = "hr:manage"
    ORGANIZATION_MANAGE = "organization:manage"
    DEPARTMENTS_MANAGE = "departments:manage"
    BRANCHES_MANAGE = "branches:manage"
    DESIGNATIONS_MANAGE = "designations:manage"
    SHIFTS_MANAGE = "shifts:manage"
    EMPLOYEE_MANAGE = "employee:manage"
    ATTENDANCE_MANAGE = "attendance:manage"
    ATTENDANCE_READ = "attendance:read"
    
    # IT
    IT_MANAGE = "it:manage"
    ASSETS_MANAGE = "assets:manage"
    DEVICES_MANAGE = "devices:manage"
    TICKETS_MANAGE = "tickets:manage"
    
    # Workflow
    WORKFLOW_MANAGE = "workflow:manage"
    WORKFLOW_APPROVE = "workflow:approve"

# Mapping of roles to their default permissions
ROLE_PERMISSIONS: dict[Role, list[Permission]] = {
    Role.TENANT_ADMIN: [
        Permission.ADMIN_ALL,
        Permission.HR_MANAGE, Permission.ORGANIZATION_MANAGE, Permission.DEPARTMENTS_MANAGE, 
        Permission.BRANCHES_MANAGE, Permission.DESIGNATIONS_MANAGE, Permission.SHIFTS_MANAGE, 
        Permission.EMPLOYEE_MANAGE, Permission.ATTENDANCE_MANAGE, Permission.ATTENDANCE_READ,
        Permission.IT_MANAGE, Permission.ASSETS_MANAGE, Permission.DEVICES_MANAGE, Permission.TICKETS_MANAGE,
        Permission.WORKFLOW_MANAGE, Permission.WORKFLOW_APPROVE
    ],
    Role.HR_ADMIN: [
        Permission.HR_MANAGE, Permission.ORGANIZATION_MANAGE, Permission.DEPARTMENTS_MANAGE, 
        Permission.BRANCHES_MANAGE, Permission.DESIGNATIONS_MANAGE, Permission.SHIFTS_MANAGE, 
        Permission.EMPLOYEE_MANAGE, Permission.ATTENDANCE_MANAGE, Permission.ATTENDANCE_READ,
        Permission.WORKFLOW_APPROVE
    ],
    Role.IT_ADMIN: [
        Permission.IT_MANAGE, Permission.ASSETS_MANAGE, Permission.DEVICES_MANAGE, Permission.TICKETS_MANAGE,
        Permission.WORKFLOW_APPROVE
    ],
    Role.MANAGER: [
        Permission.ATTENDANCE_READ,
        Permission.WORKFLOW_APPROVE
    ],
    Role.EMPLOYEE: [
        # Employees can read their own attendance and leave data via ownership-scoped endpoints.
        Permission.ATTENDANCE_READ,
    ]
}

def get_permissions_for_role(role_name: str) -> list[str]:
    try:
        role = Role(role_name)
        return [p.value for p in ROLE_PERMISSIONS.get(role, [])]
    except ValueError:
        return []

def get_permissions_for_roles(role_names: list[str]) -> list[str]:
    perms = set()
    for role_name in role_names:
        perms.update(get_permissions_for_role(role_name))
    return list(perms)
