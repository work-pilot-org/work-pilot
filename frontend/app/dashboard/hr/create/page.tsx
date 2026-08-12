"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { hrRepository } from "@/repositories/hrRepository";
import { Input } from "@/components/ui/Input";
import { Label } from "@/components/ui/Label";
import { Button } from "@/components/ui/Button";
import { RequireRole } from "@/components/RequireRole";
import { Users, Save, X, UserPlus, ShieldAlert } from "lucide-react";

export default function CreateEmployeePage() {
  const router = useRouter();
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
    work_location: "HEAD_OFFICE",
    email: "",
    role: "EMPLOYEE"
  });

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
      await hrRepository.onboardEmployee(formData);
      router.push("/dashboard/hr");
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : "Failed to onboard employee");
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <RequireRole 
      allowedRoles={["TENANT_ADMIN", "HR_ADMIN"]}
      fallback={
        <div className="flex flex-col items-center justify-center min-h-[400px] text-center px-4 bg-surface rounded-xl border border-border-strong shadow-sm p-12">
          <div className="w-16 h-16 bg-destructive/10 rounded-full flex items-center justify-center mb-4">
            <ShieldAlert className="w-8 h-8 text-destructive" />
          </div>
          <h2 className="text-xl font-semibold text-foreground mb-2">Access Restricted</h2>
          <p className="text-muted-foreground max-w-md">
            You do not have the required permissions to provision new employee accounts.
          </p>
        </div>
      }
    >
      <div className="flex flex-col h-full space-y-6 max-w-4xl mx-auto pb-12">
        
        {/* Header */}
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div>
            <div className="flex items-center gap-2 text-sm text-muted-foreground mb-1">
              <button onClick={() => router.push("/dashboard/hr")} className="hover:text-foreground transition-colors">Directory</button>
              <span>/</span>
              <span className="text-foreground font-medium">New Record</span>
            </div>
            <h1 className="text-3xl font-bold tracking-tight text-foreground flex items-center gap-2">
              <UserPlus className="w-6 h-6 text-primary" />
              Onboard Employee
            </h1>
          </div>
        </div>

        {error && (
          <div className="bg-destructive/10 border border-destructive/30 text-destructive px-4 py-3 rounded-lg shadow-sm flex items-center gap-2 text-sm font-medium">
            <ShieldAlert className="w-4 h-4" />
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-6">
          <div className="bg-surface border border-border-strong rounded-xl shadow-sm overflow-hidden">
            <div className="px-6 py-4 border-b border-border bg-surface-hover/30">
              <h3 className="text-sm font-semibold text-foreground uppercase tracking-wider">Identity & Access</h3>
            </div>
            <div className="p-6 grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="space-y-2">
                <Label htmlFor="first_name">First Name <span className="text-destructive">*</span></Label>
                <Input required id="first_name" name="first_name" value={formData.first_name} onChange={handleChange} placeholder="First name" className="shadow-sm" />
              </div>
              <div className="space-y-2">
                <Label htmlFor="last_name">Last Name <span className="text-destructive">*</span></Label>
                <Input required id="last_name" name="last_name" value={formData.last_name} onChange={handleChange} placeholder="Last name" className="shadow-sm" />
              </div>
              <div className="space-y-2">
                <Label htmlFor="email">Work Email <span className="text-destructive">*</span></Label>
                <Input required type="email" id="email" name="email" value={formData.email} onChange={handleChange} placeholder="name@company.com" className="shadow-sm" />
              </div>
              <div className="space-y-2">
                <Label htmlFor="role">System Role <span className="text-destructive">*</span></Label>
                <select id="role" name="role" value={formData.role} onChange={handleChange} className="flex h-9 w-full rounded-md border border-border bg-surface px-3 py-1 text-sm shadow-sm transition-colors focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-primary">
                  <option value="EMPLOYEE">Standard Employee</option>
                  <option value="MANAGER">Manager</option>
                  <option value="HR_ADMIN">HR Administrator</option>
                  <option value="IT_ADMIN">IT Administrator</option>
                </select>
              </div>
            </div>
          </div>

          <div className="bg-surface border border-border-strong rounded-xl shadow-sm overflow-hidden">
            <div className="px-6 py-4 border-b border-border bg-surface-hover/30">
              <h3 className="text-sm font-semibold text-foreground uppercase tracking-wider">Employment Details</h3>
            </div>
            <div className="p-6 grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="space-y-2">
                <Label htmlFor="employee_code">Employee Code <span className="text-destructive">*</span></Label>
                <Input required id="employee_code" name="employee_code" value={formData.employee_code} onChange={handleChange} placeholder="e.g. EMP-001" className="shadow-sm" />
              </div>
              <div className="space-y-2">
                <Label htmlFor="joining_date">Joining Date <span className="text-destructive">*</span></Label>
                <Input required type="date" id="joining_date" name="joining_date" value={formData.joining_date} onChange={handleChange} className="shadow-sm" />
              </div>
              <div className="space-y-2">
                <Label htmlFor="employment_type">Employment Type</Label>
                <select id="employment_type" name="employment_type" value={formData.employment_type} onChange={handleChange} className="flex h-9 w-full rounded-md border border-border bg-surface px-3 py-1 text-sm shadow-sm transition-colors focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-primary">
                  <option value="FULL_TIME">Full Time</option>
                  <option value="PART_TIME">Part Time</option>
                  <option value="CONTRACT">Contract</option>
                  <option value="INTERN">Intern</option>
                </select>
              </div>
              <div className="space-y-2">
                <Label htmlFor="employment_status">Initial Status</Label>
                <select id="employment_status" name="employment_status" value={formData.employment_status} onChange={handleChange} className="flex h-9 w-full rounded-md border border-border bg-surface px-3 py-1 text-sm shadow-sm transition-colors focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-primary">
                  <option value="ACTIVE">Active</option>
                  <option value="ON_LEAVE">On Leave</option>
                </select>
              </div>
              <div className="space-y-2 md:col-span-2">
                <Label htmlFor="work_location">Work Location</Label>
                <Input id="work_location" name="work_location" value={formData.work_location} onChange={handleChange} placeholder="e.g. Head Office, Remote" className="shadow-sm" />
              </div>
            </div>
          </div>

          <div className="bg-surface border border-border-strong rounded-xl shadow-sm overflow-hidden">
            <div className="px-6 py-4 border-b border-border bg-surface-hover/30">
              <h3 className="text-sm font-semibold text-foreground uppercase tracking-wider">Personal Information</h3>
            </div>
            <div className="p-6 grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="space-y-2">
                <Label htmlFor="phone">Phone Number</Label>
                <Input id="phone" name="phone" value={formData.phone} onChange={handleChange} placeholder="+1 234 567 8900" className="shadow-sm" />
              </div>
              <div className="space-y-2">
                <Label htmlFor="date_of_birth">Date of Birth</Label>
                <Input type="date" id="date_of_birth" name="date_of_birth" value={formData.date_of_birth} onChange={handleChange} className="shadow-sm" />
              </div>
              <div className="space-y-2">
                <Label htmlFor="gender">Gender</Label>
                <select id="gender" name="gender" value={formData.gender} onChange={handleChange} className="flex h-9 w-full rounded-md border border-border bg-surface px-3 py-1 text-sm shadow-sm transition-colors focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-primary">
                  <option value="MALE">Male</option>
                  <option value="FEMALE">Female</option>
                  <option value="OTHER">Other</option>
                </select>
              </div>
            </div>
          </div>

          <div className="flex items-center justify-end gap-3 pt-2">
            <Button type="button" variant="ghost" onClick={() => router.push("/dashboard/hr")}>
              <X className="w-4 h-4 mr-2" />
              Cancel
            </Button>
            <Button type="submit" disabled={isSubmitting} className="shadow-sm min-w-[140px]">
              {isSubmitting ? "Provisioning..." : <><Save className="w-4 h-4 mr-2" /> Onboard Employee</>}
            </Button>
          </div>
        </form>
      </div>
    </RequireRole>
  );
}
