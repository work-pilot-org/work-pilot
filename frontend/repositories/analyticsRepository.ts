import { analyticsApi } from "@/lib/axios";
import {
  AttendanceSummaryResponse,
  HeadcountResponse,
  LeaveUtilizationResponse,
  TicketSummaryResponse,
  WorkflowPerformanceResponse
} from "@/types/analytics";
import axios from "axios";

const handleApiError = (err: unknown, defaultMessage: string): never => {
  if (axios.isAxiosError(err) && err.response?.data) {
    const detail = err.response.data.detail;
    if (typeof detail === 'string') {
      throw new Error(detail);
    } else if (Array.isArray(detail)) {
      const messages = detail.map((d: any) => {
        const field = d.loc[d.loc.length - 1];
        return `${field}: ${d.msg}`;
      });
      throw new Error(messages.join(', '));
    }
  }
  throw new Error(err instanceof Error ? err.message : defaultMessage);
};

export const analyticsRepository = {
  async getHrAttendanceSummary(): Promise<AttendanceSummaryResponse> {
    try {
      const response = await analyticsApi.get<AttendanceSummaryResponse>("/analytics/hr/attendance-summary");
      return response.data;
    } catch (err: unknown) {
      return handleApiError(err, "Failed to fetch attendance summary.");
    }
  },

  async getHrLeaveUtilization(): Promise<LeaveUtilizationResponse> {
    try {
      const response = await analyticsApi.get<LeaveUtilizationResponse>("/analytics/hr/leave-utilization");
      return response.data;
    } catch (err: unknown) {
      return handleApiError(err, "Failed to fetch leave utilization.");
    }
  },

  async getHrHeadcount(): Promise<HeadcountResponse> {
    try {
      const response = await analyticsApi.get<HeadcountResponse>("/analytics/hr/headcount");
      return response.data;
    } catch (err: unknown) {
      return handleApiError(err, "Failed to fetch headcount.");
    }
  },

  async getItTicketSummary(): Promise<TicketSummaryResponse> {
    try {
      const response = await analyticsApi.get<TicketSummaryResponse>("/analytics/it/ticket-summary");
      return response.data;
    } catch (err: unknown) {
      return handleApiError(err, "Failed to fetch IT ticket summary.");
    }
  },

  async getWorkflowPerformance(): Promise<WorkflowPerformanceResponse> {
    try {
      const response = await analyticsApi.get<WorkflowPerformanceResponse>("/analytics/workflows/performance");
      return response.data;
    } catch (err: unknown) {
      return handleApiError(err, "Failed to fetch workflow performance.");
    }
  },
};
