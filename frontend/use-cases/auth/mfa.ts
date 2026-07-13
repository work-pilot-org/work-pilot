import { MFALoginRequest, MFAEnableRequest, MFADisableRequest } from "@/types/auth";
import { authRepository } from "@/repositories/authRepository";
import { useAuthStore } from "@/store/authStore";

export const executeMfaLogin = async (data: MFALoginRequest) => {
  const { setLoading, setError, setUser } = useAuthStore.getState();
  
  try {
    setLoading(true);
    setError(null);
    
    // Call the data layer
    const response = await authRepository.loginMfa(data);
    
    // Update global state
    setUser(response.user, response.token);
    
    // Optionally return response if the caller needs it
    return response;
  } catch (error: any) {
    setError(error.message || "Invalid MFA code.");
    throw error;
  } finally {
    setLoading(false);
  }
};

export const executeSetupMfa = async () => {
  return await authRepository.setupMfa();
};

export const executeEnableMfa = async (data: MFAEnableRequest) => {
  await authRepository.enableMfa(data);
};

export const executeDisableMfa = async (data: MFADisableRequest) => {
  await authRepository.disableMfa(data);
};
