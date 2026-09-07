"use client";

import { useEffect, useState } from "react";
import { useParams, useRouter } from "next/navigation";
import { hrRepository } from "@/repositories/hrRepository";
import { Input } from "@/components/ui/Input";
import { Label } from "@/components/ui/Label";
import { Button } from "@/components/ui/Button";
import { RequireRole } from "@/components/RequireRole";
import { Users } from "lucide-react";
import { LoadingState } from "@/components/common/LoadingState";

export default function EditEmployeePage() {
  const router = useRouter();
  const params = useParams();
  const employeeId = params.id as string;
  
  const [isLoading, setIsLoading] = useState(true);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const [formData, setFormData] = useState({
    first_name: "",
    last_name: "",
    employee_code: "",
    phone: "",
    gender: "MALE",
    date_of_birth: "",
    joining_date: "",
    employment_type: "FULL_TIME",
    employment_status: "ACTIVE",
    work_location: "HEAD_OFFICE"
  });

  useEffect(() => {
    const fetchEmployee = async () => {
      try {
        setIsLoading(true);
        const data = await hrRepository.getEmployeeById(employeeId);
        setFormData({
          first_name: data.first_name || "",
          last_name: data.last_name || "",
          employee_code: data.employee_code || "",
          phone: data.phone || "",
          gender: data.gender || "MALE",
          date_of_birth: data.date_of_birth || "",
          joining_date: data.joining_date || "",
          employment_type: data.employment_type || "FULL_TIME",
          employment_status: data.employment_status || "ACTIVE",
          work_location: data.work_location || "HEAD_OFFICE"
        });
      } catch (err: unknown) {
        setError(err instanceof Error ? err.message : "Failed to load employee");
      } finally {
        setIsLoading(false);
      }
    };
    if (employeeId) fetchEmployee();
  }, [employeeId]);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    setFormData(prev => ({
      ...prev,
      [e.target.name]: e.target.value
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSubmitting(true);
    setError(null);
    try {
      await hrRepository.updateEmployee(employeeId, formData);
      router.push(`/dashboard/hr/${employeeId}`);
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : "Failed to update employee");
    } finally {
      setIsSubmitting(false);
    }
  };

  if (isLoading) {
    return <LoadingState message="Loading employee data..." className="py-12" />;
  }

  return (
    <RequireRole 
      allowedRoles={["ORG_ADMIN", "HR_ADMIN"]}
      fallback={
        <div className="flex flex-col items-center justify-center min-h-[400px] text-center px-4">
          <div className="w-16 h-16 bg-red-50 rounded-full flex items-center justify-center mb-4">
            <Users className="w-8 h-8 text-red-500" />
          </div>
          <h2 className="text-xl font-semibold text-gray-900 mb-2">Access Denied</h2>
          <p className="text-gray-500 max-w-md">
            You do not have permission to edit employees.
          </p>
        </div>
      }
    >
      <div className="space-y-6 max-w-4xl mx-auto">
        <div className="flex items-center justify-between">
          <div>
            <button 
              onClick={() => router.push(`/dashboard/hr/${employeeId}`)}
              className="text-sm text-muted-foreground hover:text-foreground transition-colors mb-2 inline-block"
            >
              &larr; Back to Employee
            </button>
            <h1 className="text-2xl font-bold tracking-tight text-foreground">Edit Employee</h1>
            <p className="text-muted-foreground mt-1">Update information for {formData.first_name} {formData.last_name}.</p>
          </div>
        </div>

        {error && (
          <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-md">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="bg-white border border-border rounded-lg shadow-sm p-6 space-y-8">
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="space-y-2">
              <Label htmlFor="first_name">First Name <span className="text-red-500">*</span></Label>
              <Input required id="first_name" name="first_name" value={formData.first_name} onChange={handleChange} placeholder="John" />
            </div>
            
            <div className="space-y-2">
              <Label htmlFor="last_name">Last Name <span className="text-red-500">*</span></Label>
              <Input required id="last_name" name="last_name" value={formData.last_name} onChange={handleChange} placeholder="Doe" />
            </div>

            <div className="space-y-2">
              <Label htmlFor="employee_code">Employee Code <span className="text-red-500">*</span></Label>
              <Input required id="employee_code" name="employee_code" value={formData.employee_code} onChange={handleChange} placeholder="EMP-001" />
            </div>

            <div className="space-y-2">
              <Label htmlFor="phone">Phone Number</Label>
              <Input id="phone" name="phone" value={formData.phone} onChange={handleChange} placeholder="+1 234 567 8900" />
            </div>

            <div className="space-y-2">
              <Label htmlFor="date_of_birth">Date of Birth</Label>
              <Input type="date" id="date_of_birth" name="date_of_birth" value={formData.date_of_birth} onChange={handleChange} />
            </div>

            <div className="space-y-2">
              <Label htmlFor="joining_date">Joining Date <span className="text-red-500">*</span></Label>
              <Input required type="date" id="joining_date" name="joining_date" value={formData.joining_date} onChange={handleChange} />
            </div>

            <div className="space-y-2">
              <Label htmlFor="gender">Gender</Label>
              <select 
                id="gender" 
                name="gender" 
                value={formData.gender} 
                onChange={handleChange}
                className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
              >
                <option value="MALE">Male</option>
                <option value="FEMALE">Female</option>
                <option value="OTHER">Other</option>
              </select>
            </div>

            <div className="space-y-2">
              <Label htmlFor="employment_type">Employment Type</Label>
              <select 
                id="employment_type" 
                name="employment_type" 
                value={formData.employment_type} 
                onChange={handleChange}
                className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
              >
                <option value="FULL_TIME">Full Time</option>
                <option value="PART_TIME">Part Time</option>
                <option value="CONTRACT">Contract</option>
                <option value="INTERN">Intern</option>
              </select>
            </div>
            
            <div className="space-y-2">
              <Label htmlFor="employment_status">Status</Label>
              <select 
                id="employment_status" 
                name="employment_status" 
                value={formData.employment_status} 
                onChange={handleChange}
                className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
              >
                <option value="ACTIVE">Active</option>
                <option value="ON_LEAVE">On Leave</option>
                <option value="TERMINATED">Terminated</option>
              </select>
            </div>
            
            <div className="space-y-2">
              <Label htmlFor="work_location">Work Location</Label>
              <Input id="work_location" name="work_location" value={formData.work_location} onChange={handleChange} placeholder="e.g. New York, Remote" />
            </div>
          </div>

          <div className="flex justify-end gap-4 pt-4 border-t border-border">
            <Button type="button" variant="outline" onClick={() => router.push(`/dashboard/hr/${employeeId}`)}>
              Cancel
            </Button>
            <Button type="submit" disabled={isSubmitting}>
              {isSubmitting ? "Saving..." : "Save Changes"}
            </Button>
          </div>
        </form>
      </div>
    </RequireRole>
  );
}
