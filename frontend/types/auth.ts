export interface RegisterRequest {
  company_name: string;
  full_name: string;
  email: string;
  password: string;
  confirm_password: string;
}

export interface RegisterResponse {
  message: string;
  tenant_id: number;
  company_name: string;
  domain: string;
}

export interface ApiError {
  detail: string | { loc: string[]; msg: string; type: string }[];
}

export interface ForgotPasswordRequest {
  email: string;
}

export interface ForgotPasswordResponse {
  message: string;
}

export interface ResetPasswordRequest {
  token: string;
  new_password: string;
}

export interface ResetPasswordResponse {
  message: string;
}
