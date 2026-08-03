export interface WorkflowResponse {
  id: string;
  name: string;
  description?: string;
  is_active: boolean;
  created_by: string;
  created_at: string;
  updated_at: string;
}

export interface WorkflowStepResponse {
  id: string;
  workflow_id: string;
  step_order: number;
  step_name: string;
  approver_role: string;
}

export interface WorkflowExecutionResponse {
  id: string;
  workflow_id: string;
  entity_type: string;
  entity_id: string;
  current_step: number;
  status: "pending" | "completed" | "rejected" | "cancelled";
  started_by: string;
  created_at: string;
}

export interface ApprovalResponse {
  id: string;
  execution_id: string;
  approver_id: string;
  decision: "pending" | "approved" | "rejected" | "cancelled";
  comments?: string;
  decided_at?: string;
}
