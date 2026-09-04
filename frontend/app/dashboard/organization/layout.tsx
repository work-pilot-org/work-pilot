"use client";

import { useAuthStore } from "@/store/authStore";
import { useRouter, usePathname } from "next/navigation";
import { useEffect } from "react";
import { canManageOrganization } from "@/lib/rbac";
import { LoadingState } from "@/components/common/LoadingState";
import Link from "next/link";
import { BarChart3, Users, Mail } from "lucide-react";

export default function OrganizationLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const { user, isInitialized } = useAuthStore();
  const router = useRouter();
  const pathname = usePathname();

  useEffect(() => {
    if (isInitialized && user) {
      if (!canManageOrganization(user.roles)) {
        router.replace("/dashboard");
      }
    }
  }, [isInitialized, user, router]);

  if (!isInitialized || !user) {
    return <LoadingState message="Verifying access..." />;
  }

  if (!canManageOrganization(user.roles)) {
    return null; // Will redirect
  }

  return (
    <div className="flex flex-col h-full space-y-8 max-w-7xl mx-auto pb-12">
      {/* Page Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-3xl font-bold tracking-tight text-foreground">Organization Administration</h1>
          <p className="text-muted-foreground mt-1 text-sm">Manage organization structure, employees, and view analytics.</p>
        </div>
      </div>
      
      {/* Tab Navigation via App Router */}
      <div className="flex border-b border-gray-200 overflow-x-auto">
        <Link
          href="/dashboard/organization"
          className={`flex items-center px-4 py-2 border-b-2 font-medium text-sm transition-colors whitespace-nowrap ${
            pathname === "/dashboard/organization" 
              ? "border-indigo-500 text-indigo-600" 
              : "border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300"
          }`}
        >
          <BarChart3 className="w-4 h-4 mr-2" />
          Overview & Analytics
        </Link>
        <Link
          href="/dashboard/organization/employees"
          className={`flex items-center px-4 py-2 border-b-2 font-medium text-sm transition-colors whitespace-nowrap ${
            pathname.startsWith("/dashboard/organization/employees") 
              ? "border-indigo-500 text-indigo-600" 
              : "border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300"
          }`}
        >
          <Users className="w-4 h-4 mr-2" />
          Employees
        </Link>
        <Link
          href="/dashboard/organization/invitations"
          className={`flex items-center px-4 py-2 border-b-2 font-medium text-sm transition-colors whitespace-nowrap ${
            pathname.startsWith("/dashboard/organization/invitations") 
              ? "border-indigo-500 text-indigo-600" 
              : "border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300"
          }`}
        >
          <Mail className="w-4 h-4 mr-2" />
          Pending Invitations
        </Link>
      </div>

      <div className="bg-surface rounded-xl border border-border-strong shadow-sm overflow-hidden min-h-[500px] p-6">
        {children}
      </div>
    </div>
  );
}
