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
  }
};

