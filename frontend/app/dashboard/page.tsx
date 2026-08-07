"use client";

import { useAuthStore } from "@/store/authStore";
import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";

export default function DashboardPage() {
  const { user, isInitialized } = useAuthStore();
  const router = useRouter();
  const [redirected, setRedirected] = useState(false);

  useEffect(() => {
    if (!isInitialized || !user || redirected) return;

    const primaryRole = user.roles?.[0];

    if (primaryRole === "EMPLOYEE") {
      setRedirected(true);
      router.replace("/dashboard/employee");
    } else if (primaryRole === "HR_ADMIN") {
      setRedirected(true);
      router.replace("/dashboard/hr");
    } else if (primaryRole === "IT_ADMIN") {
      setRedirected(true);
      router.replace("/dashboard/it/tickets");
    }
    // TENANT_ADMIN and MANAGER stay on /dashboard (overview stats)
  }, [isInitialized, user, router, redirected]);

  if (!isInitialized) {
    return <div className="p-12 text-center text-gray-500 animate-pulse">Loading workspace...</div>;
  }

  // While redirecting for role-specific users show a brief spinner
  const primaryRole = user?.roles?.[0];
  if (primaryRole === "EMPLOYEE" || primaryRole === "HR_ADMIN" || primaryRole === "IT_ADMIN") {
    return <div className="p-12 text-center text-gray-500 animate-pulse">Redirecting...</div>;
  }

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold tracking-tight text-foreground">
        Welcome back, {user?.name || "User"}!
      </h1>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-100">
          <h3 className="text-sm font-medium text-gray-500">Pending Approvals</h3>
          <p className="text-3xl font-semibold mt-2">0</p>
        </div>
        <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-100">
          <h3 className="text-sm font-medium text-gray-500">Active Tickets</h3>
          <p className="text-3xl font-semibold mt-2">0</p>
        </div>
        <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-100">
          <h3 className="text-sm font-medium text-gray-500">Upcoming Leave</h3>
          <p className="text-3xl font-semibold mt-2">None</p>
        </div>
      </div>
      <div className="mt-8 bg-white p-6 rounded-lg shadow-sm border border-gray-100 min-h-[300px]">
        <h3 className="text-lg font-medium mb-4">Recent Activity Feed</h3>
        <p className="text-gray-500 text-sm italic">No recent activity to display.</p>
      </div>
    </div>
  );
}
