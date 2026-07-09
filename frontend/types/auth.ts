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

<<<<<<< HEAD
export interface User {
  id: string;
  email: string;
  name?: string;
  schemaName?: string;
}

export interface LoginCredentials {
  email: string;
  password?: string;
}

export interface LoginResponse {
  user: User;
  token: string;
=======
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
>>>>>>> f173151 (feat(auth): implement forgot and reset password flow)
}
