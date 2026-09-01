"use client";
import { useState } from "react";
import { PendingInvitationsTab } from "@/components/hr/PendingInvitationsTab";
import { EmployeesTab } from "@/components/hr/EmployeesTab";
import { Button } from "@/components/ui/Button";
import { UserPlus, Users, Mail } from "lucide-react";
import { InviteEmployeeModal } from "@/components/hr/InviteEmployeeModal";

export default function OrganizationPage() {
  const [isInviteModalOpen, setIsInviteModalOpen] = useState(false);
  const [activeTab, setActiveTab] = useState<"EMPLOYEES" | "INVITATIONS">("EMPLOYEES");
  const [refreshTrigger, setRefreshTrigger] = useState(0);

  return (
    <div className="flex flex-col h-full space-y-8 max-w-7xl mx-auto pb-12">
      {/* Page Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-3xl font-bold tracking-tight text-foreground">Organization Administration</h1>
          <p className="text-muted-foreground mt-1 text-sm">Manage employees, access roles, and pending invitations.</p>
        </div>
        <div className="flex items-center gap-3">
          <Button onClick={() => setIsInviteModalOpen(true)} className="shadow-sm">
            <UserPlus className="mr-2 h-4 w-4" />
            Invite User
          </Button>
        </div>
      </div>
      
      {/* Tab Navigation */}
      <div className="flex border-b border-gray-200">
        <button
          onClick={() => setActiveTab("EMPLOYEES")}
          className={`flex items-center px-4 py-2 border-b-2 font-medium text-sm transition-colors ${
            activeTab === "EMPLOYEES" 
              ? "border-indigo-500 text-indigo-600" 
              : "border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300"
          }`}
        >
          <Users className="w-4 h-4 mr-2" />
          Employees
        </button>
        <button
          onClick={() => setActiveTab("INVITATIONS")}
          className={`flex items-center px-4 py-2 border-b-2 font-medium text-sm transition-colors ${
            activeTab === "INVITATIONS" 
              ? "border-indigo-500 text-indigo-600" 
              : "border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300"
          }`}
        >
          <Mail className="w-4 h-4 mr-2" />
          Pending Invitations
        </button>
      </div>

      <div className="bg-surface rounded-xl border border-border-strong shadow-sm overflow-hidden min-h-[500px] p-6">
        {activeTab === "EMPLOYEES" ? <EmployeesTab refreshTrigger={refreshTrigger} /> : <PendingInvitationsTab refreshTrigger={refreshTrigger} />}
      </div>

      <InviteEmployeeModal 
        isOpen={isInviteModalOpen} 
        onClose={() => setIsInviteModalOpen(false)}
        onSuccess={() => {
          setIsInviteModalOpen(false);
          setRefreshTrigger(prev => prev + 1);
        }}
      />
    </div>
  );
}
