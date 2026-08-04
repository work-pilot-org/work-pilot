
"use client";
import { useState } from "react";
import { RequireRole } from "@/components/RequireRole";
import { Users } from "lucide-react";
import { EmptyState } from "@/components/common/EmptyState";
export default function OrganizationPage() {
  const [activeTab, setActiveTab] = useState("DEPARTMENTS");
  return (
    <RequireRole allowedRoles={["TENANT_ADMIN", "HR_ADMIN"]}>
      <div className="space-y-6">
        <h1 className="text-2xl font-bold tracking-tight text-foreground">Organization Management</h1>
        <div className="border-b border-gray-200">
          <nav className="-mb-px flex space-x-8">
            <button onClick={() => setActiveTab("DEPARTMENTS")} className={`${activeTab === "DEPARTMENTS" ? "border-indigo-500 text-indigo-600" : "border-transparent text-gray-500"} whitespace-nowrap border-b-2 py-4 px-1 text-sm font-medium`}>Departments</button>
            <button onClick={() => setActiveTab("DESIGNATIONS")} className={`${activeTab === "DESIGNATIONS" ? "border-indigo-500 text-indigo-600" : "border-transparent text-gray-500"} whitespace-nowrap border-b-2 py-4 px-1 text-sm font-medium`}>Designations</button>
          </nav>
        </div>
        <EmptyState title={`No ${activeTab.toLowerCase()} found`} description="Please create one to get started." icon={<Users className="w-6 h-6" />} />
      </div>
    </RequireRole>
  );
}
