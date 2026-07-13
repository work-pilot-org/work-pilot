import { 
  RegisterRequest, 
  RegisterResponse, 
  ForgotPasswordRequest, 
  ForgotPasswordResponse, 
  ResetPasswordResponse,
  PreAuthResponse,
  MFASetupResponse,
  MFALoginRequest,
  MFAEnableRequest,
  MFADisableRequest,
  ApiError
} from "@/types/auth";
import { api } from "@/lib/axios";
import axios from "axios";

// In a microservices architecture, you might have different URLs for different services,
// or a single API Gateway URL. Here we assume a dedicated environment variable for the auth service.
const AUTH_SERVICE_URL = process.env.NEXT_PUBLIC_AUTH_SERVICE_URL || "http://localhost:8000";

export const authRepository = {
  async register(data: RegisterRequest): Promise<RegisterResponse> {
    const response = await fetch(`${AUTH_SERVICE_URL}/auth/register`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    });

    const result = await response.json();

    if (!response.ok) {
      // The API returns validation errors in 'detail'
      throw new Error(
        typeof result.detail === "string"
          ? result.detail
          : "Failed to register. Please check your inputs."
      );
    }

    return result as RegisterResponse;
  },

  async login(data: import("@/types/auth").LoginCredentials): Promise<import("@/types/auth").LoginResponse | PreAuthResponse> {
    const response = await fetch(`${AUTH_SERVICE_URL}/auth/login`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      credentials: "include",
      body: JSON.stringify(data),
    });

    const result = await response.json();

    if (!response.ok) {
      throw new Error(
        typeof result.detail === "string"
          ? result.detail
          : "Failed to login. Please check your credentials."
      );
    }

    if (result.mfa_required) {
      return result as PreAuthResponse;
    }

    return {
      user: {
        id: result.user_id,
        email: result.email,
        name: result.company_name,
        schemaName: result.schema_name,
        domain: result.domain,
        isMfaEnabled: result.is_mfa_enabled
      },
      token: result.access_token,
      ssoToken: result.sso_token
    };
  },

  async loginMfa(data: MFALoginRequest): Promise<import("@/types/auth").LoginResponse> {
    const response = await fetch(`${AUTH_SERVICE_URL}/auth/login/mfa`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      credentials: "include",
      body: JSON.stringify(data),
    });

    const result = await response.json();

    if (!response.ok) {
      throw new Error(
        typeof result.detail === "string"
          ? result.detail
          : "Invalid MFA code."
      );
    }

    return {
      user: {
        id: result.user_id,
        email: result.email,
        name: result.company_name,
        schemaName: result.schema_name,
        domain: result.domain,
        isMfaEnabled: result.is_mfa_enabled
      },
      token: result.access_token,
      ssoToken: result.sso_token
    };
  },

  async exchangeSsoToken(ssoToken: string): Promise<void> {
    const response = await fetch(`${AUTH_SERVICE_URL}/auth/sso-exchange`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      credentials: "include",
      body: JSON.stringify({ sso_token: ssoToken }),
    });

    if (!response.ok) {
      const text = await response.text();
      console.error("SSO exchange failed with status", response.status, "body:", text);
      throw new Error("SSO exchange failed");
    }
  },

  async refreshToken(): Promise<import("@/types/auth").LoginResponse> {
    const response = await fetch(`${AUTH_SERVICE_URL}/auth/refresh`, {
      method: "POST",
      credentials: "include",
    });

    if (!response.ok) {
      throw new Error("Failed to refresh token");
    }
    
    const result = await response.json();
    return {
      user: {
        id: result.user_id,
        email: result.email,
        name: result.company_name,
        schemaName: result.schema_name,
        domain: result.domain,
        isMfaEnabled: result.is_mfa_enabled
      },
      token: result.access_token,
      ssoToken: result.sso_token
    };
  },

  async logout(): Promise<void> {
    await fetch(`${AUTH_SERVICE_URL}/auth/logout`, {
      method: "POST",
      credentials: "include",
    });
  },

    
  async forgotPassword(data: ForgotPasswordRequest): Promise<ForgotPasswordResponse> {
    try {
      const response = await api.post<ForgotPasswordResponse>("/auth/forgot-password", data);
      return response.data;
    } catch (err: any) {
      if (axios.isAxiosError(err) && err.response?.data) {
        const detail = (err.response.data as ApiError).detail;
        throw new Error(typeof detail === "string" ? detail : "Failed to process forgot password request.");
      }
      throw new Error(err.message || "An unexpected error occurred.");
    }
  },

  async resetPassword(data: ResetPasswordRequest): Promise<ResetPasswordResponse> {
    try {
      const response = await api.post<ResetPasswordResponse>("/auth/reset-password", data);
      return response.data;
    } catch (err: any) {
      if (axios.isAxiosError(err) && err.response?.data) {
        const detail = (err.response.data as ApiError).detail;
        throw new Error(typeof detail === "string" ? detail : "Failed to reset password.");
      }
      throw new Error(err.message || "An unexpected error occurred.");
    }
  },

  async setupMfa(): Promise<MFASetupResponse> {
    const response = await api.post<MFASetupResponse>("/auth/mfa/setup");
    return response.data;
  },

  async enableMfa(data: MFAEnableRequest): Promise<void> {
    await api.post("/auth/mfa/enable", data);
  },

  async disableMfa(data: MFADisableRequest): Promise<void> {
    await api.post("/auth/mfa/disable", data);
  }
};

