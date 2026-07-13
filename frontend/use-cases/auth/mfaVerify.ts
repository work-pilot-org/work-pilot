import { authRepository } from "@/repositories/authRepository";
import { LoginResponse } from "@/types/auth";
import { useAuthStore } from "@/store/authStore";

export const mfaVerifyUseCase = async (
  code: string,
  mfaToken?: string
): Promise<{
  success: boolean;
  data?: LoginResponse;
  error?: string;
}> => {
  if (!code || code.length !== 6) {
    return { success: false, error: "Verification code must be 6 digits." };
  }

  try {
    const result = await authRepository.mfaVerify(code, mfaToken);
    
    // If we received user and token (successful login verification), update store
    if (result.user && result.token) {
      const { setUser } = useAuthStore.getState();
      setUser(result.user, result.token);
    }
    
    return { success: true, data: result };
  } catch (err: any) {
    return { success: false, error: err.message || "An unexpected error occurred." };
  }
};
