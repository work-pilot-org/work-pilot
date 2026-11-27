export interface AttendanceSummary {
  status: string;
  worked_hours: number;
  overtime_hours: number;
  records: number;
}

export interface AttendanceSummaryResponse {
  tenant_id: string;
  summary: AttendanceSummary[];
}

export interface HeadcountSummary {
  status: string;
  count: number;
}

export interface HeadcountResponse {
  tenant_id: string;
  summary: HeadcountSummary[];
}

export interface LeaveUtilizationSummary {
  status: string;
  total_days: number;
  requests: number;
}

export interface LeaveUtilizationResponse {
  tenant_id: string;
  summary: LeaveUtilizationSummary[];
}

export interface TicketSummary {
  status: string;
  priority: string;
  tickets: number;
}

export interface TicketSummaryResponse {
  tenant_id: string;
  summary: TicketSummary[];
}

export interface WorkflowPerformance {
  workflow_name: string;
  workflow_type: string;
  execution_status: string;
  total_executions: number;
  avg_completion_minutes: number;
  max_completion_minutes: number;
}

export type WorkflowPerformanceResponse = WorkflowPerformance[];
