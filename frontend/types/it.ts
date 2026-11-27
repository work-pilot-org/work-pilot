export type TicketStatus = "OPEN" | "IN_PROGRESS" | "ON_HOLD" | "RESOLVED" | "CLOSED" | "CANCELLED";
export type TicketPriority = "LOW" | "MEDIUM" | "HIGH" | "CRITICAL";
export type TicketCategory = "HARDWARE" | "SOFTWARE" | "NETWORK" | "VPN" | "ACCESS_CONTROL" | "EMAIL" | "SECURITY" | "LICENSE" | "PRINTER" | "OTHER";
export type TicketSource = "WEB" | "MOBILE" | "EMAIL" | "AI_AGENT" | "ADMIN";
export type TicketResolution = "FIXED" | "WORKAROUND" | "DUPLICATE" | "CANNOT_REPRODUCE" | "NOT_AN_ISSUE";

export interface TicketResponse {
  id: string;
  ticket_number: string;
  title: string;
  description: string;
  category: TicketCategory;
  priority: TicketPriority;
  status: TicketStatus;
  source: TicketSource;
  requester_id: string;
  assigned_to?: string;
  resolution?: TicketResolution;
  resolved_at?: string;
  closed_at?: string;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface CreateTicketRequest {
  title: string;
  description: string;
  category: TicketCategory;
  priority?: TicketPriority;
  source?: TicketSource;
}

export interface UpdateTicketRequest {
  title?: string;
  description?: string;
  category?: TicketCategory;
  priority?: TicketPriority;
}

export interface UpdateTicketStatusRequest {
  status: TicketStatus;
  resolution?: TicketResolution;
}

export interface AssignTicketRequest {
  assigned_to: string;
}

export type AssetCategory = "LAPTOP" | "DESKTOP" | "MONITOR" | "PHONE" | "OTHER";
export type AssetStatus = "AVAILABLE" | "ASSIGNED" | "UNDER_MAINTENANCE" | "DISPOSED";

export interface AssetResponse {
  id: string;
  name: string;
  serial_number: string;
  category: AssetCategory;
  status: AssetStatus;
  assigned_to?: string;
  created_at: string;
  updated_at: string;
}

export interface CreateAssetRequest {
  name: string;
  serial_number: string;
  category: AssetCategory;
  status?: AssetStatus;
}

export interface UpdateAssetRequest {
  name?: string;
  serial_number?: string;
  category?: AssetCategory;
  status?: AssetStatus;
}

export interface AssignAssetRequest {
  assigned_to: string;
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
