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
import { Button } from "@/components/ui/Button";
import { RequireRole } from "@/components/RequireRole";

export default function EmployeesPage() {
  const [employees, setEmployees] = useState<EmployeeResponse[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [activeTab, setActiveTab] = useState<"EMPLOYEES" | "INVITATIONS">("EMPLOYEES");
  const router = useRouter();

  const [searchKeyword, setSearchKeyword] = useState("");
  const [currentPage, setCurrentPage] = useState(1);
  const [isDeleting, setIsDeleting] = useState<string | null>(null);

  const fetchEmployees = async () => {
    try {
      setIsLoading(true);
      setError(null);
      if (searchKeyword) {
        const data = await hrRepository.searchEmployees(searchKeyword, currentPage, 10);
        setEmployees(data);
      } else {
        const data = await hrRepository.getEmployees(); // We can also use searchEmployees("", currentPage) if the backend supports empty keyword. But backend requires min_length=1.
        setEmployees(data);
      }
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : "Failed to load employees.");
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchEmployees();
  }, [searchKeyword, currentPage]);

  const handleDelete = async (e: React.MouseEvent, id: string) => {
    e.stopPropagation();
    if (!confirm("Are you sure you want to delete this employee?")) return;
    
    try {
      setIsDeleting(id);
      await hrRepository.deleteEmployee(id);
      await fetchEmployees();
    } catch (err: unknown) {
      alert(err instanceof Error ? err.message : "Failed to delete employee");
    } finally {
      setIsDeleting(null);
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-semibold tracking-tight text-gray-900">Team Management</h1>
        <RequireRole allowedRoles={["TENANT_ADMIN", "HR_ADMIN"]}>
          <Button onClick={() => router.push("/dashboard/hr/create")}>
            Create Employee
          </Button>
        </RequireRole>
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
        ) : (
          <div className="space-y-4">
            <div className="flex gap-4 items-center">
              <input 
                type="text" 
                placeholder="Search employees..." 
                className="flex h-10 w-full max-w-sm rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2"
                value={searchKeyword}
                onChange={(e) => setSearchKeyword(e.target.value)}
              />
            </div>
            
            {employees.length === 0 ? (
              <EmptyState 
                title="No employees found"
                description={searchKeyword ? "No employees match your search criteria." : "There are currently no employees in your organization."}
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
                      <TableHead className="text-right">Actions</TableHead>
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
                        <TableCell className="text-right">
                          <RequireRole allowedRoles={["TENANT_ADMIN", "HR_ADMIN"]}>
                            <Button 
                              variant="outline" 
                              size="sm"
                              className="text-red-600 hover:text-red-700 hover:bg-red-50 border-red-200"
                              onClick={(e) => handleDelete(e, emp.id)}
                              disabled={isDeleting === emp.id}
                            >
                              {isDeleting === emp.id ? "Deleting..." : "Delete"}
                            </Button>
                          </RequireRole>
                        </TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </div>
            )}
            
            {/* Pagination Controls */}
            <div className="flex justify-between items-center py-4 border-t border-gray-200">
              <Button 
                variant="outline" 
                disabled={currentPage === 1}
                onClick={() => setCurrentPage(p => p - 1)}
              >
                Previous
              </Button>
              <span className="text-sm text-gray-500">Page {currentPage}</span>
              <Button 
                variant="outline" 
                disabled={employees.length < 10} // Assuming page size is 10
                onClick={() => setCurrentPage(p => p + 1)}
              >
                Next
              </Button>
            </div>
          </div>
        )
      ) : (
        <PendingInvitationsTab />
      )}
    </div>
  );
}
