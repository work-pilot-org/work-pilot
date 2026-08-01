export interface WorkflowResponse {
  id: string;
  name: string;
  description?: string;
  status: string;
  created_at: string;
}

export interface WorkflowExecutionResponse {
  id: string;
  workflow_id: string;
  status: string;
  started_at: string;
  completed_at?: string;
}
