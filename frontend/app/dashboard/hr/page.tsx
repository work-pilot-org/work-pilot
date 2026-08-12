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
import { Users, Search, Plus, UserPlus, Filter, Building2, Briefcase, Calendar, Phone } from "lucide-react";
import { PendingInvitationsTab } from "@/components/hr/PendingInvitationsTab";
import { Button } from "@/components/ui/Button";
import { RequireRole } from "@/components/RequireRole";
import { DropdownMenu } from "@/components/ui/DropdownMenu";
import { Drawer } from "@/components/ui/Drawer";

export default function EmployeesPage() {
  const [employees, setEmployees] = useState<EmployeeResponse[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [activeTab, setActiveTab] = useState<"EMPLOYEES" | "INVITATIONS">("EMPLOYEES");
  const router = useRouter();

  const [searchKeyword, setSearchKeyword] = useState("");
  const [currentPage, setCurrentPage] = useState(1);
  const [isDeleting, setIsDeleting] = useState<string | null>(null);
  
  // Detail Drawer State
  const [selectedEmployee, setSelectedEmployee] = useState<EmployeeResponse | null>(null);

  const fetchEmployees = async () => {
    try {
      setIsLoading(true);
      setError(null);
      if (searchKeyword) {
        const data = await hrRepository.searchEmployees(searchKeyword, currentPage, 10);
        setEmployees(data);
      } else {
        const data = await hrRepository.getEmployees(); 
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
      if (selectedEmployee?.id === id) setSelectedEmployee(null);
      await fetchEmployees();
    } catch (err: unknown) {
      alert(err instanceof Error ? err.message : "Failed to delete employee");
    } finally {
      setIsDeleting(null);
    }
  };

  return (
    <div className="flex flex-col h-full space-y-8 max-w-7xl mx-auto pb-12">
      {/* Page Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-3xl font-bold tracking-tight text-foreground">Team</h1>
          <p className="text-muted-foreground mt-1 text-sm">Manage your organization, team members, and access roles.</p>
        </div>
        <RequireRole allowedRoles={["TENANT_ADMIN", "HR_ADMIN"]}>
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
          <div className="flex flex-col space-y-6">
            
            {/* Contextual Toolbar */}
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 bg-surface p-4 rounded-xl border border-border-strong shadow-sm">
              <div className="relative max-w-md w-full">
                <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
                <input 
                  type="text" 
                  placeholder="Search by name, role, or code..." 
                  className="flex h-10 w-full rounded-md border border-border bg-transparent px-9 py-2 text-sm transition-colors placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-primary"
                  value={searchKeyword}
                  onChange={(e) => setSearchKeyword(e.target.value)}
                />
              </div>
              <div className="flex items-center gap-2">
                <Button variant="outline" size="sm" className="h-10 border-border text-muted-foreground bg-transparent">
                  <Filter className="mr-2 h-4 w-4" />
                  Filters
                </Button>
                <div className="text-sm text-muted-foreground border-l border-border pl-4 ml-2">
                  {employees.length} members
                </div>
              </div>
            </div>
            
            {/* Data Table Area */}
            {employees.length === 0 ? (
              <div className="bg-surface rounded-xl border border-border-strong shadow-sm p-12">
                <EmptyState 
                  title="No employees found"
                  description={searchKeyword ? "No employees match your search criteria." : "There are currently no employees in your organization."}
                  icon={<Users className="w-8 h-8 text-muted-foreground" />}
                />
              </div>
            ) : (
              <div className="flex flex-col space-y-4">
                <Table>
                  <TableHeader>
                    <TableRow>
                      <TableHead>Employee</TableHead>
                      <TableHead>Role</TableHead>
                      <TableHead>Status</TableHead>
                      <TableHead>Joined</TableHead>
                      <TableHead className="text-right">Actions</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {employees.map((emp) => (
                      <TableRow 
                        key={emp.id} 
                        className="cursor-pointer group"
                        onClick={() => setSelectedEmployee(emp)}
                      >
                        <TableCell>
                          <div className="flex items-center gap-3">
                            <div className="h-10 w-10 rounded-full bg-primary/10 text-primary flex items-center justify-center font-semibold text-sm">
                              {emp.first_name[0]}{emp.last_name[0]}
                            </div>
                            <div className="flex flex-col">
                              <span className="font-medium text-foreground group-hover:text-primary transition-colors">
                                {emp.first_name} {emp.last_name}
                              </span>
                              <span className="text-xs text-muted-foreground">{emp.employee_code}</span>
                            </div>
                          </div>
                        </TableCell>
                        <TableCell>
                          <div className="flex flex-col">
                            <span className="text-sm font-medium text-foreground">
                              {emp.employment_type.replace('_', ' ')}
                            </span>
                          </div>
                        </TableCell>
                        <TableCell>
                          <Badge 
                            variant={emp.employment_status === "ACTIVE" ? "success" : "secondary" as any}
                            className="font-medium"
                          >
                            {emp.employment_status}
                          </Badge>
                        </TableCell>
                        <TableCell className="text-sm text-muted-foreground">
                          {new Date(emp.joining_date).toLocaleDateString()}
                        </TableCell>
                        <TableCell className="text-right">
                          <RequireRole allowedRoles={["TENANT_ADMIN", "HR_ADMIN"]}>
                            <DropdownMenu 
                              items={[
                                { label: "View Profile", onClick: (e) => { e.stopPropagation(); setSelectedEmployee(emp); } },
                                { label: "Edit Details", onClick: (e) => { e.stopPropagation(); router.push(`/dashboard/hr/${emp.id}`); } },
                                { label: "Delete Employee", variant: "danger", onClick: (e) => handleDelete(e, emp.id) }
                              ]}
                            />
                          </RequireRole>
                        </TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
                
                {/* Pagination Controls */}
                <div className="flex justify-between items-center py-2 px-1">
                  <span className="text-sm text-muted-foreground">
                    Showing <span className="font-medium text-foreground">{employees.length}</span> results
                  </span>
                  <div className="flex gap-2">
                    <Button 
                      variant="outline" 
                      size="sm"
                      disabled={currentPage === 1}
                      onClick={() => setCurrentPage(p => p - 1)}
                    >
                      Previous
                    </Button>
                    <Button 
                      variant="outline" 
                      size="sm"
                      disabled={employees.length < 10}
                      onClick={() => setCurrentPage(p => p + 1)}
                    >
                      Next
                    </Button>
                  </div>
                </div>
              </div>
            )}
          </div>
        )
      ) : (
        <PendingInvitationsTab />
      )}

      {/* Employee Detail Drawer */}
      <Drawer
        isOpen={!!selectedEmployee}
        onClose={() => setSelectedEmployee(null)}
        title="Employee Profile"
        description="Detailed view of employee information and access roles."
      >
        {selectedEmployee && (
          <div className="space-y-8 py-2">
            
            {/* Avatar & Name Header */}
            <div className="flex flex-col items-center justify-center text-center space-y-4 py-4">
               <div className="h-24 w-24 rounded-full bg-primary/10 text-primary flex items-center justify-center font-bold text-3xl shadow-sm border border-primary/20">
                  {selectedEmployee.first_name[0]}{selectedEmployee.last_name[0]}
               </div>
               <div>
                 <h3 className="text-xl font-bold text-foreground">{selectedEmployee.first_name} {selectedEmployee.last_name}</h3>
                 <p className="text-sm text-muted-foreground mt-1">{selectedEmployee.employee_code}</p>
                 <div className="mt-3">
                   <Badge variant={selectedEmployee.employment_status === "ACTIVE" ? "success" : "secondary" as any}>
                     {selectedEmployee.employment_status}
                   </Badge>
                 </div>
               </div>
            </div>

            <div className="h-px bg-border w-full" />

            {/* Details Section */}
            <div className="space-y-6">
              
              <div>
                <h4 className="text-sm font-semibold text-foreground flex items-center gap-2 mb-4">
                  <Briefcase className="w-4 h-4 text-muted-foreground" />
                  Employment Details
                </h4>
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <span className="text-xs text-muted-foreground block mb-1">Type</span>
                    <span className="text-sm font-medium text-foreground">{selectedEmployee.employment_type.replace('_', ' ')}</span>
                  </div>
                  <div>
                    <span className="text-xs text-muted-foreground block mb-1">Joined Date</span>
                    <span className="text-sm font-medium text-foreground">{new Date(selectedEmployee.joining_date).toLocaleDateString()}</span>
                  </div>
                </div>
              </div>

              <div>
                <h4 className="text-sm font-semibold text-foreground flex items-center gap-2 mb-4">
                  <Building2 className="w-4 h-4 text-muted-foreground" />
                  Organization
                </h4>
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <span className="text-xs text-muted-foreground block mb-1">Department</span>
                    <span className="text-sm font-medium text-foreground">{selectedEmployee.department_id || "Unassigned"}</span>
                  </div>
                  <div>
                    <span className="text-xs text-muted-foreground block mb-1">Manager</span>
                    <span className="text-sm font-medium text-foreground">{selectedEmployee.manager_id || "Unassigned"}</span>
                  </div>
                </div>
              </div>
              
              <div>
                <h4 className="text-sm font-semibold text-foreground flex items-center gap-2 mb-4">
                  <Phone className="w-4 h-4 text-muted-foreground" />
                  Contact
                </h4>
                <div className="grid grid-cols-1 gap-4">
                  <div>
                    <span className="text-xs text-muted-foreground block mb-1">Phone Number</span>
                    <span className="text-sm font-medium text-foreground">{selectedEmployee.phone || "Not provided"}</span>
                  </div>
                </div>
              </div>

            </div>

            {/* Actions */}
            <div className="pt-6 mt-8 border-t border-border flex justify-end gap-3">
              <Button variant="outline" onClick={() => setSelectedEmployee(null)}>
                Close
              </Button>
              <Button onClick={() => router.push(`/dashboard/hr/${selectedEmployee.id}`)}>
                Edit Employee
              </Button>
            </div>
          </div>
        )}
      </Drawer>
    </div>
  );
}
