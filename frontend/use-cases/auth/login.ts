import { LoginCredentials } from "@/types/auth";
import { authRepository } from "@/repositories/authRepository";
import { useAuthStore } from "@/store/authStore";

export const executeLogin = async (credentials: LoginCredentials) => {
  const { setLoading, setError, setUser } = useAuthStore.getState();
  
  try {
    setLoading(true);
    setError(null);
    
    // Call the data layer
    const response = await authRepository.login(credentials);
    
    // Update global state
    setUser(response.user, response.token);
    
    // Optionally return response if the caller needs it
    return response;
  } catch (error: any) {
    setError(error.message || "Failed to login");
    throw error;
  } finally {
    setLoading(false);
  }
};
