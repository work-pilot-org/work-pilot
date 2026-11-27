"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { Users, UserPlus } from "lucide-react";
import { InvitationsTab } from "@/components/hr/InvitationsTab";
import { EmployeesTab } from "@/components/hr/EmployeesTab";
import { Button } from "@/components/ui/Button";
import { RequireRole } from "@/components/RequireRole";

export default function EmployeesPage() {
  const [activeTab, setActiveTab] = useState<"EMPLOYEES" | "INVITATIONS">("EMPLOYEES");
  const router = useRouter();

  return (
    <div className="flex flex-col h-full space-y-8 max-w-7xl mx-auto pb-12">
      {/* Page Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-3xl font-bold tracking-tight text-foreground">Team</h1>
          <p className="text-muted-foreground mt-1 text-sm">Manage your organization, team members, and access roles.</p>
        </div>
        <RequireRole allowedRoles={["ORG_ADMIN", "HR_ADMIN"]}>
          <div className="flex items-center gap-3">
            <Button variant="outline" className="bg-surface shadow-sm hover:bg-surface-hover">
              Import
            </Button>
            <Button onClick={() => router.push("/dashboard/hr/create")} className="shadow-sm">
              <UserPlus className="mr-2 h-4 w-4" />
              Invite employee
            </Button>
          </div>
        </RequireRole>
      </div>

      {/* Tabs */}
      <div className="border-b border-border">
        <nav className="-mb-px flex space-x-8" aria-label="Tabs">
          <button
            onClick={() => setActiveTab("EMPLOYEES")}
            className={`${
              activeTab === "EMPLOYEES"
                ? "border-primary text-primary"
                : "border-transparent text-muted-foreground hover:border-border hover:text-foreground"
            } whitespace-nowrap border-b-2 py-4 px-1 text-sm font-medium transition-colors`}
          >
            Employees
          </button>
          <button
            onClick={() => setActiveTab("INVITATIONS")}
            className={`${
              activeTab === "INVITATIONS"
                ? "border-primary text-primary"
                : "border-transparent text-muted-foreground hover:border-border hover:text-foreground"
            } whitespace-nowrap border-b-2 py-4 px-1 text-sm font-medium transition-colors`}
          >
            Invitations
          </button>
        </nav>
      </div>

      {activeTab === "EMPLOYEES" ? (
        <EmployeesTab />
      ) : (
        <InvitationsTab />
      )}
    </div>
  );
}
