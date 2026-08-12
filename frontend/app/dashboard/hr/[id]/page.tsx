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
import { User, ArrowLeft, Mail, Phone, Calendar, Briefcase, MapPin, Building2, UserCircle2, Clock } from "lucide-react";
import { DropdownMenu } from "@/components/ui/DropdownMenu";

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
    return <LoadingState message="Loading employee profile..." className="py-12" />;
  }

  if (error) {
    return (
      <div className="space-y-4 max-w-7xl mx-auto">
        <ErrorState message={error} onRetry={fetchEmployee} />
        <Button variant="outline" onClick={() => router.push("/dashboard/hr")}>
          <ArrowLeft className="w-4 h-4 mr-2" />
          Back to Employees
        </Button>
      </div>
    );
  }

  if (!employee) {
    return (
      <EmptyState 
        title="Employee not found"
        description="The employee record you are looking for does not exist or has been removed."
        icon={<User className="w-8 h-8 text-muted-foreground" />}
      />
    );
  }

  const getInitials = (first: string, last: string) => {
    return `${first?.[0] || ""}${last?.[0] || ""}`.toUpperCase();
  };

  return (
    <div className="flex flex-col h-full space-y-6 max-w-7xl mx-auto pb-12">
      
      {/* Header Context */}
      <div className="flex items-center space-x-2 text-sm text-muted-foreground mb-2">
        <button onClick={() => router.push("/dashboard/hr")} className="hover:text-foreground transition-colors">
          People
        </button>
        <span>/</span>
        <span className="text-foreground">{employee.first_name} {employee.last_name}</span>
      </div>

      {/* Main Profile Header */}
      <div className="bg-surface border border-border-strong rounded-xl shadow-sm overflow-hidden">
        <div className="h-32 bg-surface-hover/50 border-b border-border w-full relative">
          <div className="absolute right-6 top-6">
            <Badge variant={employee.employment_status === "ACTIVE" ? "success" : "secondary"} className="shadow-sm">
              {employee.employment_status}
            </Badge>
          </div>
        </div>
        
        <div className="px-6 sm:px-8 pb-8 flex flex-col sm:flex-row gap-6 sm:items-end relative -mt-12">
          <div className="w-24 h-24 rounded-2xl bg-primary text-primary-foreground flex items-center justify-center text-3xl font-bold border-4 border-surface shadow-md shrink-0">
            {getInitials(employee.first_name, employee.last_name)}
          </div>
          
          <div className="flex-1 space-y-1">
            <h1 className="text-3xl font-bold tracking-tight text-foreground">
              {employee.first_name} {employee.last_name}
            </h1>
            <p className="text-muted-foreground font-medium flex items-center gap-2">
              <Briefcase className="w-4 h-4" />
              {employee.employment_type} • {employee.employee_code}
            </p>
          </div>
          
          <div className="flex items-center gap-3 shrink-0 pt-4 sm:pt-0">
            <Button variant="outline" className="shadow-sm" onClick={() => router.push(`/dashboard/hr/${employee.id}/edit`)}>
              Edit Profile
            </Button>
            <DropdownMenu 
              items={[
                { label: "Request Leave", onClick: () => {} },
                { label: "View Timesheets", onClick: () => {} },
                { label: "Generate Report", onClick: () => {} },
                { label: "Deactivate", onClick: () => {} }
              ]}
            />
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        
        {/* Left Col: Contact & Meta */}
        <div className="lg:col-span-1 space-y-6">
          <div className="bg-surface border border-border-strong rounded-xl shadow-sm p-6 space-y-6">
            <h3 className="text-sm font-semibold text-foreground uppercase tracking-wider">Contact Information</h3>
            <div className="space-y-4">
              <div className="flex items-start gap-3">
                <Phone className="w-4 h-4 text-muted-foreground mt-0.5" />
                <div>
                  <p className="text-xs text-muted-foreground">Phone</p>
                  <p className="text-sm font-medium text-foreground">{employee.phone || "Not provided"}</p>
                </div>
              </div>
              <div className="flex items-start gap-3">
                <MapPin className="w-4 h-4 text-muted-foreground mt-0.5" />
                <div>
                  <p className="text-xs text-muted-foreground">Location</p>
                  <p className="text-sm font-medium text-foreground">{employee.work_location || "Remote"}</p>
                </div>
              </div>
            </div>
          </div>
          
          <div className="bg-surface border border-border-strong rounded-xl shadow-sm p-6 space-y-6">
            <h3 className="text-sm font-semibold text-foreground uppercase tracking-wider">Personal Details</h3>
            <div className="space-y-4">
              <div className="flex items-start gap-3">
                <UserCircle2 className="w-4 h-4 text-muted-foreground mt-0.5" />
                <div>
                  <p className="text-xs text-muted-foreground">Gender</p>
                  <p className="text-sm font-medium text-foreground">{employee.gender || "Not specified"}</p>
                </div>
              </div>
              <div className="flex items-start gap-3">
                <Calendar className="w-4 h-4 text-muted-foreground mt-0.5" />
                <div>
                  <p className="text-xs text-muted-foreground">Date of Birth</p>
                  <p className="text-sm font-medium text-foreground">{employee.date_of_birth || "Not specified"}</p>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Right Col: Employment Context */}
        <div className="lg:col-span-2 space-y-6">
          <div className="bg-surface border border-border-strong rounded-xl shadow-sm">
            <div className="px-6 py-4 border-b border-border">
              <h3 className="text-sm font-semibold text-foreground uppercase tracking-wider">Employment Context</h3>
            </div>
            <div className="p-6 grid grid-cols-1 sm:grid-cols-2 gap-8">
              <div>
                <div className="flex items-center gap-2 mb-1 text-muted-foreground">
                  <Building2 className="w-4 h-4" />
                  <span className="text-xs font-medium">Department</span>
                </div>
                <p className="text-sm font-semibold text-foreground mt-1">Pending Assignment</p>
              </div>
              <div>
                <div className="flex items-center gap-2 mb-1 text-muted-foreground">
                  <Briefcase className="w-4 h-4" />
                  <span className="text-xs font-medium">Designation</span>
                </div>
                <p className="text-sm font-semibold text-foreground mt-1">Pending Assignment</p>
              </div>
              <div>
                <div className="flex items-center gap-2 mb-1 text-muted-foreground">
                  <Clock className="w-4 h-4" />
                  <span className="text-xs font-medium">Joining Date</span>
                </div>
                <p className="text-sm font-semibold text-foreground mt-1">{employee.joining_date}</p>
              </div>
            </div>
          </div>
          
          {/* Quick Actions Context */}
          <div className="bg-surface-hover/30 border border-border rounded-xl p-6 flex items-center justify-between">
            <div className="flex items-center gap-4">
              <div className="w-10 h-10 rounded-full bg-primary/10 flex items-center justify-center">
                <span className="text-primary font-bold text-lg">AI</span>
              </div>
              <div>
                <h4 className="text-sm font-medium text-foreground">Ask WorkPilot about this employee</h4>
                <p className="text-xs text-muted-foreground mt-0.5">Quickly retrieve history, performance, or leave data.</p>
              </div>
            </div>
            <Button variant="outline" size="sm" className="shadow-sm" onClick={() => router.push('/dashboard/chat')}>
              Open AI Workspace
            </Button>
          </div>
          
        </div>
      </div>
    </div>
  );
}
