import { RegisterRequest, RegisterResponse } from "@/types/auth";
import { authRepository } from "@/repositories/authRepository";

export const registerUseCase = async (
  data: RegisterRequest
): Promise<{ success: boolean; data?: RegisterResponse; error?: string }> => {
  // Business logic validation
  if (data.password !== data.confirm_password) {
    return { success: false, error: "Passwords do not match." };
  }

  if (data.password.length < 8) {
    return { success: false, error: "Password must be at least 8 characters long." };
  }

  try {
    const result = await authRepository.register(data);
    return { success: true, data: result };
  } catch (err: any) {
    return { success: false, error: err.message || "An unexpected error occurred." };
  }
};
