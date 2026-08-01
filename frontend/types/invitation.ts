export type Role = "ORG_ADMIN" | "HR_ADMIN" | "IT_ADMIN" | "MANAGER" | "EMPLOYEE";
export type InvitationStatus = "PENDING" | "ACCEPTED" | "EXPIRED" | "REVOKED";

export interface InvitationCreateRequest {
  email: string;
  role: Role;
}

export interface InvitationResponse {
  id: string;
  tenant_id: number;
  email: string;
  role: Role;
  status: InvitationStatus;
  expires_at: string;
  created_at: string;
  last_sent_at?: string;
  revoked_at?: string;
}

export interface InvitationValidateResponse {
  valid: boolean;
  expired: boolean;
  revoked: boolean;
  user_exists: boolean;
  company_name?: string;
  role?: Role;
  email?: string;
}

export interface AcceptInvitationRequest {
  token: string;
  full_name: string;
  password?: string;
  confirm_password?: string;
}
