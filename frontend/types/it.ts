export interface TicketResponse {
  id: string;
  ticket_number: string;
  title: string;
  description: string;
  category: string;
  priority: string;
  status: string;
  source: string;
  requester_id: string;
  assigned_to?: string;
  resolution?: string;
  resolved_at?: string;
  closed_at?: string;
  created_at: string;
  updated_at: string;
}

export interface CreateTicketRequest {
  title: string;
  description: string;
  category: string;
  priority?: string;
}

export interface UpdateTicketRequest {
  title?: string;
  description?: string;
  category?: string;
  priority?: string;
}

export interface AssetResponse {
  id: string;
  name: string;
  type: string;
  status: string;
}

export type AccessRequestType = "VPN" | "APPLICATION" | "DATABASE";

export type AccessRequestStatus = "PENDING" | "APPROVED" | "REJECTED" | "REVOKED";

export interface AccessRequestResponse {
  id: string;
  request_type: AccessRequestType;
  target_resource: string;
  requested_by: string;
  status: AccessRequestStatus;
  approved_by?: string;
  reason?: string;
  created_at: string;
  updated_at: string;
}

export interface CreateAccessRequest {
  request_type: AccessRequestType;
  target_resource: string;
  requested_by: string;
  reason?: string;
}

export interface UpdateAccessRequest {
  target_resource?: string;
  reason?: string;
}
