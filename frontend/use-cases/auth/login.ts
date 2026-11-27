import { LoginCredentials, PreAuthResponse, LoginResponse } from "@/types/auth";
import { authRepository } from "@/repositories/authRepository";
import { useAuthStore } from "@/store/authStore";

export const executeLogin = async (
  credentials: LoginCredentials
): Promise<LoginResponse | PreAuthResponse> => {
  const { setLoading, setError, setUser } = useAuthStore.getState();

  try {
    setLoading(true);
    setError(null);

    console.log("[AUTH] Login");
    const response = await authRepository.login(credentials);

    if ("mfa_required" in response) {
      return response as PreAuthResponse;
    }

    // Update global state — the page (LoginForm) handles the redirect.
    setUser(response.user, response.token);

    return response as LoginResponse;
  } catch (error: unknown) {
    const errorMsg = error instanceof Error ? error.message : "Failed to login";
    setError(errorMsg);
    throw error;
  } finally {
    setLoading(false);
  }
};
