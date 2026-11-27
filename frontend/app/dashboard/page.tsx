"use client";

import { useAuthStore } from "@/store/authStore";
import { AdminDashboard } from "@/components/dashboard/AdminDashboard";
import { HRDashboard } from "@/components/dashboard/HRDashboard";
import { ManagerDashboard } from "@/components/dashboard/ManagerDashboard";
import { EmployeeDashboard } from "@/components/dashboard/EmployeeDashboard";
import { ITDashboard } from "@/components/dashboard/ITDashboard";
import { LoadingState } from "@/components/common/LoadingState";
import { useEffect, useState } from "react";

export default function DashboardPage() {
  const { user, isInitialized } = useAuthStore();
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  if (!isInitialized || !mounted) {
    return <LoadingState message="Loading workspace..." className="py-20" />;
  }

  const primaryRole = user?.roles?.[0] || "EMPLOYEE";

  switch (primaryRole) {
    case "ORG_ADMIN":
      return <AdminDashboard />;
    case "HR_ADMIN":
      return <HRDashboard />;
    case "IT_ADMIN":
      return <ITDashboard />;
    case "MANAGER":
      return <ManagerDashboard />;
    case "EMPLOYEE":
    default:
      return <EmployeeDashboard />;
  }
}

