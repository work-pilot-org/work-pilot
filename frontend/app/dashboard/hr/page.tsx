"use client";

import { useEffect, useState } from "react";
import { hrRepository } from "@/repositories/hrRepository";
import { EmployeeResponse } from "@/types/hr";
import { useRouter } from "next/navigation";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/Table";
import { Badge } from "@/components/ui/Badge";
import { LoadingState } from "@/components/common/LoadingState";
import { ErrorState } from "@/components/common/ErrorState";
import { EmptyState } from "@/components/common/EmptyState";
import { Users } from "lucide-react";
import { PendingInvitationsTab } from "@/components/hr/PendingInvitationsTab";

export default function EmployeesPage() {
  const [employees, setEmployees] = useState<EmployeeResponse[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [activeTab, setActiveTab] = useState<"EMPLOYEES" | "INVITATIONS">("EMPLOYEES");
  const router = useRouter();

  const fetchEmployees = async () => {
    try {
      setIsLoading(true);
      setError(null);
      const data = await hrRepository.getEmployees();
      setEmployees(data);
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : "Failed to load employees.");
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchEmployees();
  }, []);

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-semibold tracking-tight text-gray-900">Team Management</h1>
      </div>

      <div className="border-b border-gray-200">
        <nav className="-mb-px flex space-x-8" aria-label="Tabs">
          <button
            onClick={() => setActiveTab("EMPLOYEES")}
            className={`${
              activeTab === "EMPLOYEES"
                ? "border-indigo-500 text-indigo-600"
                : "border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700"
            } whitespace-nowrap border-b-2 py-4 px-1 text-sm font-medium`}
          >
            Employees
          </button>
          <button
            onClick={() => setActiveTab("INVITATIONS")}
            className={`${
              activeTab === "INVITATIONS"
                ? "border-indigo-500 text-indigo-600"
                : "border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700"
            } whitespace-nowrap border-b-2 py-4 px-1 text-sm font-medium`}
          >
            Pending Invitations
          </button>
        </nav>
      </div>

      {activeTab === "EMPLOYEES" ? (
        isLoading ? (
          <LoadingState message="Loading employees..." className="py-12" />
        ) : error ? (
          <ErrorState message={error} onRetry={fetchEmployees} />
        ) : employees.length === 0 ? (
          <EmptyState 
            title="No employees found"
            description="There are currently no employees in your organization."
            icon={<Users className="w-6 h-6" />}
          />
        ) : (
          <div className="border rounded-lg overflow-hidden mt-6">
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Employee Code</TableHead>
                  <TableHead>Name</TableHead>
                  <TableHead>Role Type</TableHead>
                  <TableHead>Status</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {employees.map((emp) => (
                  <TableRow 
                    key={emp.id} 
                    className="cursor-pointer"
                    onClick={() => router.push(`/dashboard/hr/${emp.id}`)}
                  >
                    <TableCell className="font-medium">
                      {emp.employee_code}
                    </TableCell>
                    <TableCell>
                      {emp.first_name} {emp.last_name}
                    </TableCell>
                    <TableCell>
                      {emp.employment_type}
                    </TableCell>
                    <TableCell>
                      <Badge variant={emp.employment_status === "ACTIVE" ? "success" : "secondary" as any}>
                        {emp.employment_status}
                      </Badge>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </div>
        )
      ) : (
        <PendingInvitationsTab />
      )}
    </div>
  );
}
