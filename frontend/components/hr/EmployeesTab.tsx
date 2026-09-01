import { useEffect, useState } from "react";
import { hrRepository } from "@/repositories/hrRepository";
import { EmployeeResponse } from "@/types/hr";
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

export function EmployeesTab({ refreshTrigger = 0 }: { refreshTrigger?: number }) {
  const [employees, setEmployees] = useState<EmployeeResponse[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

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
  }, [refreshTrigger]);

  if (isLoading) {
    return <LoadingState message="Loading employees..." className="py-12" />;
  }

  if (error) {
    return <ErrorState message={error} onRetry={fetchEmployees} />;
  }

  const getStatusVariant = (status: string) => {
    switch (status) {
      case "ACTIVE":
        return "success";
      case "INACTIVE":
      case "TERMINATED":
      case "RESIGNED":
        return "secondary";
      default:
        return "default";
    }
  };

  return (
    <div className="space-y-6 mt-6">
      <div className="flex items-center justify-between">
        <h2 className="text-xl font-semibold tracking-tight text-gray-900">Employees</h2>
      </div>

      {employees.length === 0 ? (
        <EmptyState
          title="No employees found"
          description="There are currently no active employees in this organization."
          icon={<Users className="w-6 h-6" />}
        />
      ) : (
        <div className="border rounded-lg overflow-hidden bg-white">
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Employee Code</TableHead>
                <TableHead>First Name</TableHead>
                <TableHead>Last Name</TableHead>
                <TableHead>Employment Type</TableHead>
                <TableHead>Date of Joining</TableHead>
                <TableHead>Status</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {employees.map((emp) => (
                <TableRow key={emp.id}>
                  <TableCell className="font-medium">{emp.employee_code}</TableCell>
                  <TableCell>{emp.first_name}</TableCell>
                  <TableCell>{emp.last_name}</TableCell>
                  <TableCell>{emp.employment_type.replace("_", " ")}</TableCell>
                  <TableCell>{emp.joining_date}</TableCell>
                  <TableCell>
                    <Badge variant={getStatusVariant(emp.employment_status) as any}>
                      {emp.employment_status}
                    </Badge>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </div>
      )}
    </div>
  );
}
