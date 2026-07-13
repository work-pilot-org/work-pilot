import { authRepository } from "@/repositories/authRepository";
import { MFASetupResponse } from "@/types/auth";

export const mfaSetupUseCase = async (): Promise<{
  success: boolean;
  data?: MFASetupResponse;
  error?: string;
}> => {
  try {
    const result = await authRepository.mfaSetup();
    return { success: true, data: result };
  } catch (err: any) {
    return { success: false, error: err.message || "An unexpected error occurred." };
  }
};
