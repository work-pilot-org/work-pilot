import React, { ReactNode } from "react";
import { useAuthStore } from "@/store/authStore";

const ROLE_PERMISSIONS: Record<string, string[]> = {
  TENANT_ADMIN: [
    "admin:all",
    "hr:manage", "organization:manage", "departments:manage", 
    "branches:manage", "designations:manage", "shifts:manage", 
    "employee:manage", "attendance:manage", "attendance:read",
    "it:manage", "assets:manage", "devices:manage", "tickets:manage",
    "workflow:manage", "workflow:approve"
  ],
  HR_ADMIN: [
    "hr:manage", "organization:manage", "departments:manage", 
    "branches:manage", "designations:manage", "shifts:manage", 
    "employee:manage", "attendance:manage", "attendance:read",
    "workflow:approve"
  ],
  IT_ADMIN: [
    "it:manage", "assets:manage", "devices:manage", "tickets:manage",
    "workflow:approve"
  ],
  MANAGER: [
    "attendance:read",
    "workflow:approve"
  ],
  EMPLOYEE: []
};

interface RequirePermissionProps {
  requiredPermissions: string[];
  children: ReactNode;
  fallback?: ReactNode;
}

export function RequirePermission({ requiredPermissions, children, fallback = null }: RequirePermissionProps) {
  const { user } = useAuthStore();
  
  if (!user || !user.roles) {
    return <>{fallback}</>;
  }

  // Flatten permissions for user roles
  const userPermissions = new Set<string>();
  for (const role of user.roles) {
    const perms = ROLE_PERMISSIONS[role] || [];
    for (const p of perms) {
      userPermissions.add(p);
    }
  }

  // Admin bypass
  if (userPermissions.has("admin:all")) {
    return <>{children}</>;
  }

  // Check if user has ALL required permissions
  const hasAccess = requiredPermissions.every(p => userPermissions.has(p));
  
  if (hasAccess) {
    return <>{children}</>;
  }
  
  return <>{fallback}</>;
}
