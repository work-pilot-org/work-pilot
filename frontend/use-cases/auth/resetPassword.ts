import { ResetPasswordRequest, ResetPasswordResponse } from "@/types/auth";
import { authRepository } from "@/repositories/authRepository";

export const resetPasswordUseCase = async (
  data: ResetPasswordRequest
): Promise<{ success: boolean; data?: ResetPasswordResponse; error?: string }> => {
  if (!data.token) {
    return { success: false, error: "Reset token is required." };
  }

  if (!data.new_password) {
    return { success: false, error: "New password is required." };
  }

  if (data.new_password.length < 8) {
    return { success: false, error: "Password must be at least 8 characters long." };
  }

  try {
    const result = await authRepository.resetPassword(data);
    return { success: true, data: result };
  } catch (err: any) {
    return { success: false, error: err.message || "An unexpected error occurred." };
  }
};
