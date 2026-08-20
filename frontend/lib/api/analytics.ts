import { analyticsApi } from "../axios";

export const getAttendanceSummary = async () => {
  const response = await analyticsApi.get("/analytics/hr/attendance-summary");
  return response.data;
};

export const getLeaveUtilization = async (period?: string, department?: string) => {
  const params = new URLSearchParams();
  if (period) params.append("period", period);
  if (department) params.append("department", department);
  const response = await analyticsApi.get(`/analytics/hr/leave-utilization?${params.toString()}`);
  return response.data;
};

export const getHeadcount = async (department?: string, employment_type?: string) => {
  const params = new URLSearchParams();
  if (department) params.append("department", department);
  if (employment_type) params.append("employment_type", employment_type);
  const response = await analyticsApi.get(`/analytics/hr/headcount?${params.toString()}`);
  return response.data;
};

export const getTicketSummary = async (period?: string, category?: string) => {
  const params = new URLSearchParams();
  if (period) params.append("period", period);
  if (category) params.append("category", category);
  const response = await analyticsApi.get(`/analytics/it/ticket-summary?${params.toString()}`);
  return response.data;
};

export const getAssetAssignments = async (status?: string, category?: string) => {
  const params = new URLSearchParams();
  if (status) params.append("status", status);
  if (category) params.append("category", category);
  const response = await analyticsApi.get(`/analytics/it/asset-assignments?${params.toString()}`);
  return response.data;
};

export const getWorkflowPerformance = async (workflow_id?: string, execution_status?: string) => {
  const params = new URLSearchParams();
  if (workflow_id) params.append("workflow_id", workflow_id);
  if (execution_status) params.append("execution_status", execution_status);
  const response = await analyticsApi.get(`/analytics/workflows/performance?${params.toString()}`);
  return response.data;
};

export const getWorkflowBottlenecks = async (workflow_id?: string, step_order?: number, status?: string) => {
  const params = new URLSearchParams();
  if (workflow_id) params.append("workflow_id", workflow_id);
  if (step_order) params.append("step_order", step_order.toString());
  if (status) params.append("status", status);
  const response = await analyticsApi.get(`/analytics/workflows/bottlenecks?${params.toString()}`);
  return response.data;
};
