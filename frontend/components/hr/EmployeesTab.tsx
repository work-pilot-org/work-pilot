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
import { Button } from "@/components/ui/Button";
import { LoadingState } from "@/components/common/LoadingState";
import { ErrorState } from "@/components/common/ErrorState";
import { EmptyState } from "@/components/common/EmptyState";
import { Users, Search, Filter, Briefcase, Building2, Phone } from "lucide-react";
import { RequireRole } from "@/components/RequireRole";
import { DropdownMenu } from "@/components/ui/DropdownMenu";
import { Drawer } from "@/components/ui/Drawer";
import toast from "react-hot-toast";

export function EmployeesTab({ refreshTrigger = 0 }: { refreshTrigger?: number }) {
  const [employees, setEmployees] = useState<EmployeeResponse[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const router = useRouter();

  const [searchKeyword, setSearchKeyword] = useState("");
  const [currentPage, setCurrentPage] = useState(1);
  const [isUpdating, setIsUpdating] = useState<string | null>(null);
  
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
  }, [searchKeyword, currentPage, refreshTrigger]);

  const handleDeactivate = async (e: React.MouseEvent, id: string) => {
    e.stopPropagation();
    if (!window.confirm("Are you sure you want to deactivate this employee?")) return;
    
    try {
      setIsUpdating(id);
      await hrRepository.updateEmployee(id, { employment_status: 'INACTIVE' } as any);
      toast.success("Employee deactivated successfully");
      if (selectedEmployee?.id === id) {
        setSelectedEmployee(prev => prev ? { ...prev, employment_status: 'INACTIVE' } as any : null);
      }
      await fetchEmployees();
    } catch (err: unknown) {
      toast.error(err instanceof Error ? err.message : "Failed to deactivate employee");
    } finally {
      setIsUpdating(null);
    }
  };

  const handleReactivate = async (e: React.MouseEvent, id: string) => {
    e.stopPropagation();
    if (!window.confirm("Are you sure you want to reactivate this employee?")) return;
    
    try {
      setIsUpdating(id);
      await hrRepository.updateEmployee(id, { employment_status: 'ACTIVE' } as any);
      toast.success("Employee reactivated successfully");
      if (selectedEmployee?.id === id) {
        setSelectedEmployee(prev => prev ? { ...prev, employment_status: 'ACTIVE' } as any : null);
      }
      await fetchEmployees();
    } catch (err: unknown) {
      toast.error(err instanceof Error ? err.message : "Failed to reactivate employee");
    } finally {
      setIsUpdating(null);
    }
  };

  if (isLoading && employees.length === 0) {
    return <LoadingState message="Loading employees..." className="py-12" />;
  }

  if (error && employees.length === 0) {
    return <ErrorState message={error} onRetry={fetchEmployees} />;
  }

  return (
    <div className="space-y-8 mt-2">
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h2 className="text-2xl font-bold tracking-tight text-gray-900">Employees</h2>
          <p className="text-sm text-gray-500 mt-1">Manage organization employees and access roles.</p>
        </div>
      </div>
      
      {/* Contextual Toolbar */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 bg-white p-4 rounded-xl border border-gray-200 shadow-sm">
        <div className="relative max-w-md w-full">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-gray-400" />
          <input 
            type="text" 
            placeholder="Search by name, role, or code..." 
            className="flex h-10 w-full rounded-md border border-gray-200 bg-transparent px-9 py-2 text-sm transition-colors placeholder:text-gray-400 focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-indigo-500"
            value={searchKeyword}
            onChange={(e) => setSearchKeyword(e.target.value)}
          />
        </div>
        <div className="flex items-center gap-3">
          <Button variant="outline" size="sm" className="h-10 border-gray-200 text-gray-600 bg-white hover:bg-gray-50">
            <Filter className="mr-2 h-4 w-4" />
            Filters
          </Button>
          <div className="text-sm font-medium text-gray-500 border-l border-gray-200 pl-4 ml-1">
            {employees.length} members
          </div>
        </div>
      </div>
      
      {/* Data Table Area */}
      {employees.length === 0 ? (
        <div className="bg-white rounded-xl border border-gray-200 shadow-sm p-12">
          <EmptyState 
            title="No employees found"
            description={searchKeyword ? "No employees match your search criteria." : "There are currently no employees in your organization."}
            icon={<Users className="w-8 h-8 text-gray-400" />}
          />
        </div>
      ) : (
        <div className="flex flex-col space-y-4">
          <div className="bg-white rounded-xl border border-gray-200 shadow-sm overflow-hidden">
            <Table>
              <TableHeader>
                <TableRow className="bg-gray-50 hover:bg-gray-50">
                  <TableHead className="font-semibold text-gray-900 py-4">Employee</TableHead>
                  <TableHead className="font-semibold text-gray-900 py-4">Role</TableHead>
                  <TableHead className="font-semibold text-gray-900 py-4">Status</TableHead>
                  <TableHead className="font-semibold text-gray-900 py-4">Joined</TableHead>
                  <TableHead className="text-right font-semibold text-gray-900 py-4">Actions</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {employees.map((emp) => (
                  <TableRow 
                    key={emp.id} 
                    className="cursor-pointer group hover:bg-gray-50 transition-colors"
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
                          {emp.employment_type?.replace('_', ' ') || "-"}
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
                      <RequireRole allowedRoles={["ORG_ADMIN", "HR_ADMIN"]}>
                        <DropdownMenu 
                          items={[
                            { label: "View Profile", onClick: (e) => { e.stopPropagation(); setSelectedEmployee(emp); } },
                            { label: "Edit Details", onClick: (e) => { e.stopPropagation(); router.push(`/dashboard/hr/${emp.id}`); } },
                            emp.employment_status === "ACTIVE" 
                              ? { label: "Deactivate", variant: "danger", onClick: (e) => handleDeactivate(e, emp.id) }
                              : { label: "Reactivate", onClick: (e) => handleReactivate(e, emp.id) }
                          ]}
                        />
                      </RequireRole>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </div>
          
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

      {/* Employee Detail Drawer */}
      <Drawer
        isOpen={!!selectedEmployee}
        onClose={() => setSelectedEmployee(null)}
        title="Employee Profile"
        description="Detailed view of employee information and access roles."
      >
        {selectedEmployee && (
          <div className="space-y-8 py-2">
            
            <div className="flex flex-col items-center justify-center text-center space-y-4 py-4">
               <div className="h-24 w-24 rounded-full bg-primary/10 text-primary flex items-center justify-center font-bold text-3xl shadow-sm border border-primary/20">
                  {selectedEmployee.first_name[0]}{selectedEmployee.last_name[0]}
               </div>
               <div>
                 <h3 className="text-xl font-bold text-foreground">{selectedEmployee.first_name} {selectedEmployee.last_name}</h3>
                 <p className="text-sm text-muted-foreground mt-1">{selectedEmployee.employee_code}</p>
                 <div className="mt-3 flex justify-center gap-2">
                   <Badge variant={selectedEmployee.employment_status === "ACTIVE" ? "success" : "secondary" as any}>
                     {selectedEmployee.employment_status}
                   </Badge>
                   <Badge variant="outline">
                     {selectedEmployee.employment_type?.replace('_', ' ')}
                   </Badge>
                 </div>
               </div>
            </div>

            <div className="h-px bg-border w-full" />

            <div className="space-y-6">
              
              <div>
                <h4 className="text-sm font-semibold text-foreground flex items-center gap-2 mb-4">
                  <Briefcase className="w-4 h-4 text-muted-foreground" />
                  Employment Details
                </h4>
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <span className="text-xs text-muted-foreground block mb-1">Type</span>
                    <span className="text-sm font-medium text-foreground">{selectedEmployee.employment_type?.replace('_', ' ') || "-"}</span>
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

            <div className="pt-6 mt-8 border-t border-border flex justify-end gap-3">
              <Button variant="outline" onClick={() => setSelectedEmployee(null)}>
                Close
              </Button>
              <RequireRole allowedRoles={["ORG_ADMIN", "HR_ADMIN"]}>
                <Button onClick={() => router.push(`/dashboard/hr/${selectedEmployee.id}`)}>
                  Edit Employee
                </Button>
              </RequireRole>
            </div>
          </div>
        )}
      </Drawer>
    </div>
  );
}
