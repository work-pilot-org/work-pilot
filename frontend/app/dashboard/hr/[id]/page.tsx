"use client";

import { useEffect, useState } from "react";
import { useParams, useRouter } from "next/navigation";
import { hrRepository } from "@/repositories/hrRepository";
import { EmployeeResponse } from "@/types/hr";
import { LoadingState } from "@/components/common/LoadingState";
import { ErrorState } from "@/components/common/ErrorState";
import { EmptyState } from "@/components/common/EmptyState";
import { Badge } from "@/components/ui/Badge";
import { Button } from "@/components/ui/Button";
import { User } from "lucide-react";

export default function EmployeeDetailsPage() {
  const params = useParams();
  const router = useRouter();
  const employeeId = params.id as string;

  const [employee, setEmployee] = useState<EmployeeResponse | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchEmployee = async () => {
    if (!employeeId) return;
    try {
      setIsLoading(true);
      setError(null);
      const data = await hrRepository.getEmployeeById(employeeId);
      setEmployee(data);
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : "Failed to load employee details.");
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchEmployee();
  }, [employeeId]);

  if (isLoading) {
    return <LoadingState message="Loading employee details..." className="py-12" />;
  }

  if (error) {
    return (
      <div className="space-y-4">
        <ErrorState message={error} onRetry={fetchEmployee} />
        <Button variant="outline" onClick={() => router.push("/dashboard/hr")}>
          &larr; Back to Employees
        </Button>
      </div>
    );
  }

  if (!employee) {
    return (
      <EmptyState 
        title="Employee not found"
        description="The employee you are looking for does not exist."
        icon={<User className="w-6 h-6" />}
      />
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-4">
          <button 
            onClick={() => router.push("/dashboard/hr")}
            className="text-muted-foreground hover:text-foreground transition-colors"
          >
            &larr; Back
          </button>
          <h1 className="text-2xl font-bold tracking-tight text-foreground">
            {employee.first_name} {employee.last_name}
          </h1>
        </div>
        <Badge variant={employee.employment_status === "ACTIVE" ? "success" : "secondary"}>
          {employee.employment_status}
        </Badge>
      </div>

      <div className="bg-white border border-border rounded-lg overflow-hidden shadow-sm">
        <div className="px-6 py-5 border-b border-border bg-muted/30">
          <h3 className="text-lg leading-6 font-medium text-foreground">
            Employee Information
          </h3>
        </div>
        <div className="px-6 py-5">
          <dl className="grid grid-cols-1 gap-x-4 gap-y-8 sm:grid-cols-2">
            <div className="sm:col-span-1">
              <dt className="text-sm font-medium text-muted-foreground">Employee Code</dt>
              <dd className="mt-1 text-sm font-medium text-foreground">{employee.employee_code}</dd>
            </div>
            <div className="sm:col-span-1">
              <dt className="text-sm font-medium text-muted-foreground">Employment Type</dt>
              <dd className="mt-1 text-sm text-foreground">{employee.employment_type}</dd>
            </div>
            <div className="sm:col-span-1">
              <dt className="text-sm font-medium text-muted-foreground">Joining Date</dt>
              <dd className="mt-1 text-sm text-foreground">{employee.joining_date}</dd>
            </div>
            <div className="sm:col-span-1">
              <dt className="text-sm font-medium text-muted-foreground">Date of Birth</dt>
              <dd className="mt-1 text-sm text-foreground">{employee.date_of_birth || "N/A"}</dd>
            </div>
            <div className="sm:col-span-1">
              <dt className="text-sm font-medium text-muted-foreground">Phone</dt>
              <dd className="mt-1 text-sm text-foreground">{employee.phone || "N/A"}</dd>
            </div>
            <div className="sm:col-span-1">
              <dt className="text-sm font-medium text-muted-foreground">Gender</dt>
              <dd className="mt-1 text-sm text-foreground">{employee.gender || "N/A"}</dd>
            </div>
            <div className="sm:col-span-1">
              <dt className="text-sm font-medium text-muted-foreground">Work Location</dt>
              <dd className="mt-1 text-sm text-foreground">{employee.work_location || "N/A"}</dd>
            </div>
          </dl>
        </div>
      </div>
    </div>
  );
}
