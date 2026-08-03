import { hrApi } from "@/lib/axios";
import { EmployeeResponse } from "@/types/hr";
import axios from "axios";
import { ApiError } from "@/types/auth"; // Reusing ApiError

export const hrRepository = {
  async getEmployees(): Promise<EmployeeResponse[]> {
    try {
      const response = await hrApi.get<EmployeeResponse[]>("/employees");
      return response.data;
    } catch (err: unknown) {
      if (axios.isAxiosError(err) && err.response?.data) {
        const detail = (err.response.data as ApiError).detail;
        throw new Error(typeof detail === "string" ? detail : "Failed to fetch employees.");
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
      if (axios.isAxiosError(err) && err.response?.data) {
        const detail = (err.response.data as ApiError).detail;
        throw new Error(typeof detail === "string" ? detail : "Failed to search employees.");
      }
      throw new Error(err instanceof Error ? err.message : "An unexpected error occurred.");
    }
  },

  async getEmployeeById(id: string): Promise<EmployeeResponse> {
    try {
      const response = await hrApi.get<EmployeeResponse>(`/employees/${id}`);
      return response.data;
    } catch (err: unknown) {
      if (axios.isAxiosError(err) && err.response?.data) {
        const detail = (err.response.data as ApiError).detail;
        throw new Error(typeof detail === "string" ? detail : "Failed to fetch employee details.");
      }
      throw new Error(err instanceof Error ? err.message : "An unexpected error occurred.");
    }
  },

  async createEmployee(employee: Partial<EmployeeResponse>): Promise<EmployeeResponse> {
    try {
      const response = await hrApi.post<EmployeeResponse>("/employees", employee);
      return response.data;
    } catch (err: unknown) {
      if (axios.isAxiosError(err) && err.response?.data) {
        const detail = (err.response.data as ApiError).detail;
        throw new Error(typeof detail === "string" ? detail : "Failed to create employee.");
      }
      throw new Error(err instanceof Error ? err.message : "An unexpected error occurred.");
    }
  },

  async updateEmployee(id: string, employee: Partial<EmployeeResponse>): Promise<EmployeeResponse> {
    try {
      const response = await hrApi.put<EmployeeResponse>(`/employees/${id}`, employee);
      return response.data;
    } catch (err: unknown) {
      if (axios.isAxiosError(err) && err.response?.data) {
        const detail = (err.response.data as ApiError).detail;
        throw new Error(typeof detail === "string" ? detail : "Failed to update employee.");
      }
      throw new Error(err instanceof Error ? err.message : "An unexpected error occurred.");
    }
  },

  async deleteEmployee(id: string): Promise<EmployeeResponse> {
    try {
      const response = await hrApi.delete<EmployeeResponse>(`/employees/${id}`);
      return response.data;
    } catch (err: unknown) {
      if (axios.isAxiosError(err) && err.response?.data) {
        const detail = (err.response.data as ApiError).detail;
        throw new Error(typeof detail === "string" ? detail : "Failed to delete employee.");
      }
      throw new Error(err instanceof Error ? err.message : "An unexpected error occurred.");
    }
  },

  async getTodayAttendance(): Promise<import("@/types/hr").AttendanceResponse[]> {
    try {
      const response = await hrApi.get<import("@/types/hr").AttendanceResponse[]>("/attendance/today");
      return response.data;
    } catch (err: unknown) {
      if (axios.isAxiosError(err) && err.response?.data) {
        const detail = (err.response.data as ApiError).detail;
        throw new Error(typeof detail === "string" ? detail : "Failed to fetch today's attendance.");
      }
      throw new Error(err instanceof Error ? err.message : "An unexpected error occurred.");
    }
  },

  async checkIn(): Promise<import("@/types/hr").AttendanceResponse> {
    try {
      const response = await hrApi.post<import("@/types/hr").AttendanceResponse>("/attendance/check-in");
      return response.data;
    } catch (err: unknown) {
      if (axios.isAxiosError(err) && err.response?.data) {
        const detail = (err.response.data as ApiError).detail;
        throw new Error(typeof detail === "string" ? detail : "Failed to check in.");
      }
      throw new Error(err instanceof Error ? err.message : "An unexpected error occurred.");
    }
  },

  async checkOut(): Promise<import("@/types/hr").AttendanceResponse> {
    try {
      const response = await hrApi.post<import("@/types/hr").AttendanceResponse>("/attendance/check-out");
      return response.data;
    } catch (err: unknown) {
      if (axios.isAxiosError(err) && err.response?.data) {
        const detail = (err.response.data as ApiError).detail;
        throw new Error(typeof detail === "string" ? detail : "Failed to check out.");
      }
      throw new Error(err instanceof Error ? err.message : "An unexpected error occurred.");
    }
  },

  async getLeaveRequests(): Promise<import("@/types/hr").LeaveRequestResponse[]> {
    try {
      const response = await hrApi.get<import("@/types/hr").LeaveRequestResponse[]>("/leave-requests");
      return response.data;
    } catch (err: unknown) {
      if (axios.isAxiosError(err) && err.response?.data) {
        const detail = (err.response.data as ApiError).detail;
        throw new Error(typeof detail === "string" ? detail : "Failed to fetch leave requests.");
      }
      throw new Error(err instanceof Error ? err.message : "An unexpected error occurred.");
    }
  },

  async getDepartments(): Promise<import("@/types/hr").DepartmentResponse[]> {
    try {
      const response = await hrApi.get<import("@/types/hr").DepartmentResponse[]>("/organization/departments");
      return response.data;
    } catch (err: unknown) {
      if (axios.isAxiosError(err) && err.response?.data) {
        const detail = (err.response.data as ApiError).detail;
        throw new Error(typeof detail === "string" ? detail : "Failed to fetch departments.");
      }
      throw new Error(err instanceof Error ? err.message : "An unexpected error occurred.");
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

  async getDesignations(): Promise<any[]> {
    const response = await hrApi.get("/organization/designations");
    return response.data;
  },
  async createDesignation(data: any): Promise<any> {
    const response = await hrApi.post("/organization/designations", data);
    return response.data;
  },
  async updateDesignation(id: number, data: any): Promise<any> {
    const response = await hrApi.put(`/organization/designations/${id}`, data);
    return response.data;
  },
  async deleteDesignation(id: number): Promise<void> {
    await hrApi.delete(`/organization/designations/${id}`);
  },

  async getBranches(): Promise<any[]> {
    const response = await hrApi.get("/organization/branches");
    return response.data;
  },
  async getShifts(): Promise<any[]> {
    const response = await hrApi.get("/organization/shifts");
    return response.data;
  }
};

