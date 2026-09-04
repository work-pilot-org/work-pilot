import { hrApi } from "@/lib/axios";
import { EmployeeResponse } from "@/types/hr";
import axios from "axios";
import { ApiError } from "@/types/auth"; // Reusing ApiError


const handleApiError = (err: unknown, defaultMessage: string): never => {
  if (axios.isAxiosError(err) && err.response?.data) {
    const detail = (err.response.data as import('@/types/auth').ApiError).detail;
    if (typeof detail === 'string') {
      throw new Error(detail);
    } else if (Array.isArray(detail)) {
      const messages = detail.map(d => {
        const field = d.loc[d.loc.length - 1];
        return `${field}: ${d.msg}`;
      });
      throw new Error(messages.join(', '));
    }
  }
  throw new Error(err instanceof Error ? err.message : defaultMessage);
};

export const hrRepository = {
  async getEmployees(): Promise<EmployeeResponse[]> {
    try {
      const response = await hrApi.get<EmployeeResponse[]>("/employees");
      return response.data;
    } catch (err: unknown) {
      return handleApiError(err, "Failed to fetch employees.");
    }
  },

  async getMyProfile(): Promise<EmployeeResponse> {
    try {
      const response = await hrApi.get<EmployeeResponse>("/employees/me");
      return response.data;
    } catch (err: unknown) {
      return handleApiError(err, "Failed to fetch your profile.");
    }
  },

  async getMyTodayAttendance(): Promise<import("@/types/hr").AttendanceResponse | null> {
    try {
      const response = await hrApi.get<import("@/types/hr").AttendanceResponse | null>("/attendance/me/today");
      return response.data;
    } catch (err: unknown) {
      if (axios.isAxiosError(err)) {
        if (err.response) {
          if (err.response.status === 401) throw new Error("Authentication failed.");
          if (err.response.status === 403) throw new Error("Authorization failed.");
          if (err.response.status >= 500) throw new Error("Server error. Service might be temporarily unavailable.");
          
          const detail = (err.response.data as ApiError)?.detail;
          throw new Error(typeof detail === "string" ? detail : "Failed to fetch your attendance.");
        } else {
          throw new Error("Network connection error.");
        }
      }
      throw new Error(err instanceof Error ? err.message : "An unexpected error occurred.");
    }
  },


  async searchEmployees(keyword: string, page: number = 1, size: number = 10): Promise<EmployeeResponse[]> {
    try {
      const response = await hrApi.get<EmployeeResponse[]>("/employees/search/", {
        params: { keyword, page, size }
      });
      return response.data;
    } catch (err: unknown) {
      return handleApiError(err, "Failed to search employees.");
    }
  },

  async getEmployeeById(id: string): Promise<EmployeeResponse> {
    try {
      const response = await hrApi.get<EmployeeResponse>(`/employees/${id}`);
      return response.data;
    } catch (err: unknown) {
      return handleApiError(err, "Failed to fetch employee details.");
    }
  },

  async createEmployee(employee: Partial<EmployeeResponse>): Promise<EmployeeResponse> {
    try {
      const response = await hrApi.post<EmployeeResponse>("/employees", employee);
      return response.data;
    } catch (err: unknown) {
      return handleApiError(err, "Failed to create employee.");
    }
  },

  async onboardEmployee(employee: import("@/types/hr").EmployeeCreateRequest): Promise<EmployeeResponse> {
    try {
      const response = await hrApi.post<EmployeeResponse>("/employees/onboard", employee);
      return response.data;
    } catch (err: unknown) {
      return handleApiError(err, "Failed to onboard employee.");
    }
  },

  async updateEmployee(id: string, employee: Partial<EmployeeResponse>): Promise<EmployeeResponse> {
    try {
      const response = await hrApi.put<EmployeeResponse>(`/employees/${id}`, employee);
      return response.data;
    } catch (err: unknown) {
      return handleApiError(err, "Failed to update employee.");
    }
  },

  async deleteEmployee(id: string): Promise<EmployeeResponse> {
    try {
      const response = await hrApi.delete<EmployeeResponse>(`/employees/${id}`);
      return response.data;
    } catch (err: unknown) {
      return handleApiError(err, "Failed to delete employee.");
    }
  },

  async getTodayAttendance(): Promise<import("@/types/hr").AttendanceResponse[]> {
    try {
      const response = await hrApi.get<import("@/types/hr").AttendanceResponse[]>("/attendance/today");
      return response.data;
    } catch (err: unknown) {
      return handleApiError(err, "Failed to fetch today's attendance.");
    }
  },

  async checkIn(employeeId: string): Promise<import("@/types/hr").AttendanceResponse> {
    try {
      const response = await hrApi.post<import("@/types/hr").AttendanceResponse>("/attendance/check-in", { employee_id: employeeId });
      return response.data;
    } catch (err: unknown) {
      return handleApiError(err, "Failed to check in.");
    }
  },

  async checkOut(employeeId: string): Promise<import("@/types/hr").AttendanceResponse> {
    try {
      const response = await hrApi.post<import("@/types/hr").AttendanceResponse>("/attendance/check-out", { employee_id: employeeId });
      return response.data;
    } catch (err: unknown) {
      return handleApiError(err, "Failed to check out.");
    }
  },

  async getLeaveRequests(): Promise<import("@/types/hr").LeaveRequestResponse[]> {
    try {
      const response = await hrApi.get<import("@/types/hr").LeaveRequestResponse[]>("/leave-requests");
      return response.data;
    } catch (err: unknown) {
      return handleApiError(err, "Failed to fetch leave requests.");
    }
  },

  async getDepartments(): Promise<import("@/types/hr").DepartmentResponse[]> {
    try {
      const response = await hrApi.get<import("@/types/hr").DepartmentResponse[]>("/organization/departments");
      return response.data;
    } catch (err: unknown) {
      return handleApiError(err, "Failed to fetch departments.");
    }
  },

  async createDepartment(data: any): Promise<import("@/types/hr").DepartmentResponse> {
    const response = await hrApi.post("/organization/departments", data);
    return response.data;
  },
  async updateDepartment(id: number, data: any): Promise<import("@/types/hr").DepartmentResponse> {
    const response = await hrApi.put(`/organization/departments/${id}`, data);
    return response.data;
  },
  async deleteDepartment(id: number): Promise<void> {
    await hrApi.delete(`/organization/departments/${id}`);
  },

  async getDesignations(): Promise<import("@/types/hr").DesignationResponse[]> {
    const response = await hrApi.get("/organization/designations");
    return response.data;
  },
  async createDesignation(data: Partial<import("@/types/hr").DesignationResponse>): Promise<import("@/types/hr").DesignationResponse> {
    const response = await hrApi.post("/organization/designations", data);
    return response.data;
  },
  async updateDesignation(id: number, data: Partial<import("@/types/hr").DesignationResponse>): Promise<import("@/types/hr").DesignationResponse> {
    const response = await hrApi.put(`/organization/designations/${id}`, data);
    return response.data;
  },
  async deleteDesignation(id: number): Promise<void> {
    await hrApi.delete(`/organization/designations/${id}`);
  },

  async getBranches(): Promise<import("@/types/hr").BranchResponse[]> {
    const response = await hrApi.get("/organization/branches");
    return response.data;
  },
  async getShifts(): Promise<import("@/types/hr").ShiftResponse[]> {
    const response = await hrApi.get("/organization/shifts");
    return response.data;
  },

  async getLeaveTypes(): Promise<import("@/types/hr").LeaveTypeResponse[]> {
    const response = await hrApi.get("/leave-types");
    return response.data;
  },

  async createLeaveType(data: any): Promise<import("@/types/hr").LeaveTypeResponse> {
    const response = await hrApi.post("/leave-types", data);
    return response.data;
  },

  async updateLeaveRequestStatus(id: string, status: import("@/types/hr").LeaveStatus, review_comments: string = ""): Promise<import("@/types/hr").LeaveRequestResponse> {
    const response = await hrApi.patch(`/leave-requests/${id}/status`, { status, review_comments });
    return response.data;
  },

  async getLeaveBalances(): Promise<import("@/types/hr").LeaveBalanceResponse[]> {
    const response = await hrApi.get("/leave-balances");
    return response.data;
  },

  async getHolidays(): Promise<import("@/types/hr").HolidayResponse[]> {
    const response = await hrApi.get("/holidays");
    return response.data;
  },

  async getOrganizationLeaveReport(): Promise<import("@/types/hr").OrganizationLeaveReportResponse> {
    const response = await hrApi.get("/leave/reports");
    return response.data;
  },

  async getLeavePolicies(): Promise<import("@/types/hr").LeavePolicyResponse[]> {
    const response = await hrApi.get("/leave-policies");
    return response.data;
  },

  async getAttendancePolicies(): Promise<import("@/types/hr").AttendancePolicyResponse[]> {
    const response = await hrApi.get("/attendance-policies");
    return response.data;
  },

  async getShiftPolicies(): Promise<import("@/types/hr").ShiftPolicyResponse[]> {
    const response = await hrApi.get("/shift-policies");
    return response.data;
  },

  async getHolidayPolicies(): Promise<import("@/types/hr").HolidayPolicyResponse[]> {
    const response = await hrApi.get("/holiday-policies");
    return response.data;
  },

  async getProbationPolicies(): Promise<import("@/types/hr").ProbationPolicyResponse[]> {
    const response = await hrApi.get("/probation-policies");
    return response.data;
  }
};

