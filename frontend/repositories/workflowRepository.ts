import { workflowApi } from "@/lib/axios";
import { WorkflowResponse, WorkflowExecutionResponse } from "@/types/workflow";
import axios from "axios";
import { ApiError } from "@/types/auth";

export const workflowRepository = {
  async getWorkflows(): Promise<WorkflowResponse[]> {
    try {
      const response = await workflowApi.get<WorkflowResponse[]>("/workflows");
      return response.data;
    } catch (err: unknown) {
      if (axios.isAxiosError(err) && err.response?.data) {
        const detail = (err.response.data as ApiError).detail;
        throw new Error(typeof detail === "string" ? detail : "Failed to fetch workflows.");
      }
      throw new Error(err instanceof Error ? err.message : "An unexpected error occurred.");
    }
  },

  async getWorkflowExecutions(): Promise<WorkflowExecutionResponse[]> {
    try {
      const response = await workflowApi.get<WorkflowExecutionResponse[]>("/workflow-executions");
      return response.data;
    } catch (err: unknown) {
      if (axios.isAxiosError(err) && err.response?.data) {
        const detail = (err.response.data as ApiError).detail;
        throw new Error(typeof detail === "string" ? detail : "Failed to fetch executions.");
      }
      throw new Error(err instanceof Error ? err.message : "An unexpected error occurred.");
    }
  }
};
