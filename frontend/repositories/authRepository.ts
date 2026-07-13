import { 
  RegisterRequest, 
  RegisterResponse, 
  ForgotPasswordRequest, 
  ForgotPasswordResponse, 
  ResetPasswordRequest, 
  ResetPasswordResponse,
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

  async login(data: import("@/types/auth").LoginCredentials): Promise<import("@/types/auth").LoginResponse> {
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
      return {
        mfaRequired: true,
        mfaToken: result.mfa_token
      };
    }

    return {
      user: {
        id: result.user_id,
        email: result.email,
        name: result.company_name,
        schemaName: result.schema_name,
        domain: result.domain
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
        domain: result.domain
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

  async mfaSetup(): Promise<import("@/types/auth").MFASetupResponse> {
    const { useAuthStore } = await import("@/store/authStore");
    const token = useAuthStore.getState().token;
    try {
      const response = await api.post<import("@/types/auth").MFASetupResponse>(
        "/auth/mfa/setup",
        {},
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );
      return response.data;
    } catch (err: any) {
      if (axios.isAxiosError(err) && err.response?.data) {
        const detail = (err.response.data as ApiError).detail;
        throw new Error(typeof detail === "string" ? detail : "Failed to setup MFA.");
      }
      throw new Error(err.message || "An unexpected error occurred.");
    }
  },

  async mfaVerify(code: string, mfaToken?: string): Promise<import("@/types/auth").LoginResponse> {
    const { useAuthStore } = await import("@/store/authStore");
    const token = useAuthStore.getState().token;
    try {
      const headers: Record<string, string> = {};
      if (token) {
        headers["Authorization"] = `Bearer ${token}`;
      }
      const response = await api.post(
        "/auth/mfa/verify",
        { code, mfa_token: mfaToken },
        { headers }
      );
      const result = response.data;
      if (result.access_token) {
        return {
          user: {
            id: result.user_id,
            email: result.email,
            name: result.company_name,
            schemaName: result.schema_name,
            domain: result.domain
          },
          token: result.access_token,
          ssoToken: result.sso_token
        };
      }
      return result;
    } catch (err: any) {
      if (axios.isAxiosError(err) && err.response?.data) {
        const detail = (err.response.data as ApiError).detail;
        throw new Error(typeof detail === "string" ? detail : "Failed to verify code.");
      }
      throw new Error(err.message || "An unexpected error occurred.");
    }
  },

  async mfaDisable(code: string): Promise<void> {
    const { useAuthStore } = await import("@/store/authStore");
    const token = useAuthStore.getState().token;
    try {
      await api.post(
        "/auth/mfa/disable",
        { code },
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );
    } catch (err: any) {
      if (axios.isAxiosError(err) && err.response?.data) {
        const detail = (err.response.data as ApiError).detail;
        throw new Error(typeof detail === "string" ? detail : "Failed to disable MFA.");
      }
      throw new Error(err.message || "An unexpected error occurred.");
    }
  },

  async mfaStatus(): Promise<{ enabled: boolean }> {
    const { useAuthStore } = await import("@/store/authStore");
    const token = useAuthStore.getState().token;
    try {
      const response = await api.get<{ enabled: boolean }>(
        "/auth/mfa/status",
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );
      return response.data;
    } catch (err: any) {
      if (axios.isAxiosError(err) && err.response?.data) {
        const detail = (err.response.data as ApiError).detail;
        throw new Error(typeof detail === "string" ? detail : "Failed to fetch MFA status.");
      }
      throw new Error(err.message || "An unexpected error occurred.");
    }
  }
};

