import { useState } from "react";
import { Button } from "@/components/ui/Button";
import { Input } from "@/components/ui/Input";
import { Label } from "@/components/ui/Label";
import { Role } from "@/types/invitation";
import { hrRepository } from "@/repositories/hrRepository";
import toast from "react-hot-toast";
import { EmployeeCreateRequest } from "@/types/hr";

interface InviteEmployeeModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSuccess: () => void;
}

export function InviteEmployeeModal({ isOpen, onClose, onSuccess }: InviteEmployeeModalProps) {
  const [email, setEmail] = useState("");
  const [role, setRole] = useState<string>("EMPLOYEE");
  const [employeeCode, setEmployeeCode] = useState("");
  const [firstName, setFirstName] = useState("");
  const [lastName, setLastName] = useState("");
  const [joiningDate, setJoiningDate] = useState("");
  const [employmentType, setEmploymentType] = useState("FULL_TIME");

  const [isSubmitting, setIsSubmitting] = useState(false);
  const [fieldErrors, setFieldErrors] = useState<Record<string, string>>({});

  if (!isOpen) return null;

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setFieldErrors({});
    if (!email || !employeeCode || !firstName || !lastName || !joiningDate) {
      toast.error("Please fill in all required fields.");
      return;
    }

    try {
      setIsSubmitting(true);
      
      const payload: EmployeeCreateRequest = {
        email: email.trim(),
        role,
        employee_code: employeeCode.trim(),
        first_name: firstName.trim(),
        last_name: lastName.trim(),
        joining_date: joiningDate, // Already in YYYY-MM-DD from <input type="date">
        employment_type: employmentType,
        employment_status: "ACTIVE"
      };

      await hrRepository.onboardEmployee(payload);
      toast.success("Employee onboarded and invitation sent successfully");
      
      // Reset form
      setEmail("");
      setRole("EMPLOYEE");
      setEmployeeCode("");
      setFirstName("");
      setLastName("");
      setJoiningDate("");
      setEmploymentType("FULL_TIME");
      
      onSuccess();
      onClose();
    } catch (error: unknown) {
      const errorMsg = error instanceof Error ? error.message : "Failed to onboard employee";
      toast.error(errorMsg);
      // Attempt to map backend validation messages to fields if it's a known format
      // Note: we just toast the error as per existing implementation but can parse fields if provided
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center overflow-y-auto overflow-x-hidden bg-black/50 p-4">
      <div className="relative w-full max-w-2xl rounded-lg bg-white shadow-lg max-h-[90vh] overflow-y-auto">
        <div className="sticky top-0 z-10 flex items-center justify-between border-b bg-white p-4">
          <h3 className="text-lg font-medium text-gray-900">Onboard & Invite Employee</h3>
          <button
            onClick={onClose}
            className="ml-auto inline-flex items-center rounded-lg bg-transparent p-1.5 text-sm text-gray-400 hover:bg-gray-200 hover:text-gray-900"
          >
            <svg className="h-5 w-5" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
              <path fillRule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clipRule="evenodd"></path>
            </svg>
          </button>
        </div>
        
        <form onSubmit={handleSubmit} className="p-4 space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label htmlFor="firstName">First Name</Label>
              <Input
                id="firstName"
                placeholder="John"
                value={firstName}
                onChange={(e) => setFirstName(e.target.value)}
                required
              />
            </div>
            
            <div className="space-y-2">
              <Label htmlFor="lastName">Last Name</Label>
              <Input
                id="lastName"
                placeholder="Doe"
                value={lastName}
                onChange={(e) => setLastName(e.target.value)}
                required
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="email">Email Address</Label>
              <Input
                id="email"
                type="email"
                placeholder="employee@company.com"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="employeeCode">Employee Code</Label>
              <Input
                id="employeeCode"
                placeholder="EMP001"
                value={employeeCode}
                onChange={(e) => setEmployeeCode(e.target.value)}
                required
              />
            </div>
            
            <div className="space-y-2">
              <Label htmlFor="joiningDate">Date of Joining</Label>
              <Input
                id="joiningDate"
                type="date"
                value={joiningDate}
                onChange={(e) => setJoiningDate(e.target.value)}
                required
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="employmentType">Employment Type</Label>
              <select
                id="employmentType"
                className="flex h-10 w-full rounded-md border border-gray-300 bg-white px-3 py-2 text-sm placeholder:text-gray-400 focus:outline-none focus:ring-2 focus:ring-indigo-500 disabled:cursor-not-allowed disabled:opacity-50"
                value={employmentType}
                onChange={(e) => setEmploymentType(e.target.value)}
                required
              >
                <option value="FULL_TIME">Full Time</option>
                <option value="PART_TIME">Part Time</option>
                <option value="CONTRACT">Contract</option>
                <option value="INTERN">Intern</option>
              </select>
            </div>
            
            <div className="space-y-2 md:col-span-2">
              <Label htmlFor="role">Role Authorization</Label>
              <select
                id="role"
                className="flex h-10 w-full rounded-md border border-gray-300 bg-white px-3 py-2 text-sm placeholder:text-gray-400 focus:outline-none focus:ring-2 focus:ring-indigo-500 disabled:cursor-not-allowed disabled:opacity-50"
                value={role}
                onChange={(e) => setRole(e.target.value)}
                required
              >
                <option value="EMPLOYEE">Employee</option>
                <option value="MANAGER">Manager</option>
                <option value="HR_ADMIN">HR Admin</option>
                <option value="IT_ADMIN">IT Admin</option>
              </select>
            </div>
          </div>
          
          <div className="flex justify-end space-x-2 pt-4 border-t mt-4">
            <Button type="button" variant="outline" onClick={onClose} disabled={isSubmitting}>
              Cancel
            </Button>
            <Button type="submit" disabled={isSubmitting}>
              {isSubmitting ? "Onboarding..." : "Onboard & Send Invitation"}
            </Button>
          </div>
        </form>
      </div>
    </div>
  );
}
