import React, { ReactNode } from "react";
import { useAuthStore } from "@/store/authStore";

interface RequireRoleProps {
  allowedRoles: string[];
  children: ReactNode;
  fallback?: ReactNode;
}

export function RequireRole({ allowedRoles, children, fallback = null }: RequireRoleProps) {
  const { user } = useAuthStore();
  
  if (!user || !user.roles) {
    return <>{fallback}</>;
  }

  // Check if user has ANY allowed role
  const hasAccess = user.roles.some(role => allowedRoles.includes(role));
  
  if (hasAccess) {
    return <>{children}</>;
  }
  
  return <>{fallback}</>;
}
