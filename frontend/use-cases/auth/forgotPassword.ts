import { ForgotPasswordRequest, ForgotPasswordResponse } from "@/types/auth";
import { authRepository } from "@/repositories/authRepository";

export const forgotPasswordUseCase = async (
  data: ForgotPasswordRequest
): Promise<{ success: boolean; data?: ForgotPasswordResponse; error?: string }> => {
  if (!data.email) {
    return { success: false, error: "Email is required." };
  }

  try {
    const result = await authRepository.forgotPassword(data);
    return { success: true, data: result };
  } catch (err: any) {
    return { success: false, error: err.message || "An unexpected error occurred." };
  }
};
