import { RegisterRequest, RegisterResponse } from "@/types/auth";

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
};
