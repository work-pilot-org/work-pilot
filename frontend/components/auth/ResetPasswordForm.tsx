"use client";

import { useState } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import * as z from "zod";
import { Lock, RefreshCw, Loader2 } from "lucide-react";
import { resetPasswordUseCase } from "@/use-cases/auth/resetPassword";
import { useRouter } from "next/navigation";

const resetPasswordSchema = z
  .object({
    new_password: z.string().min(8, "Password must be at least 8 characters long"),
    confirm_password: z.string().min(1, "Please confirm your password"),
  })
  .refine((data) => data.new_password === data.confirm_password, {
    message: "Passwords do not match",
    path: ["confirm_password"],
  });

type ResetPasswordFormData = z.infer<typeof resetPasswordSchema>;

interface ResetPasswordFormProps {
  token: string;
}

export default function ResetPasswordForm({ token }: ResetPasswordFormProps) {
  const router = useRouter();
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [successMsg, setSuccessMsg] = useState<string | null>(null);

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<ResetPasswordFormData>({
    resolver: zodResolver(resetPasswordSchema),
    defaultValues: {
      new_password: "",
      confirm_password: "",
    },
  });

  const onSubmit = async (data: ResetPasswordFormData) => {
    if (isLoading) return;
    if (!token) {
      setError("Reset token is missing. Please check your recovery email link.");
      return;
    }

    setIsLoading(true);
    setError(null);
    setSuccessMsg(null);

    const result = await resetPasswordUseCase({
      token,
      new_password: data.new_password,
    });

    if (!result.success) {
      setError(result.error || "An error occurred");
      setIsLoading(false);
    } else {
      setSuccessMsg("Password reset successfully. Redirecting you to login...");
      setTimeout(() => {
        router.replace("/login");
      }, 2500);
    }
  };

  if (!token) {
    return (
      <div className="bg-red-50 text-red-700 p-4 rounded-xl text-sm font-medium text-center">
        Reset token is missing or invalid. Please check your password recovery link.
      </div>
    );
  }

  return (
    <form className="space-y-5" onSubmit={handleSubmit(onSubmit)}>
      {/* New Password */}
      <div className="space-y-2">
        <label htmlFor="new_password" className="block text-[13px] font-medium text-gray-700">New Password</label>
        <div className="relative">
          <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none">
            <Lock className="h-4 w-4 text-gray-400" />
          </div>
          <input
            type="password"
            id="new_password"
            placeholder="••••••••"
            {...register("new_password")}
            className="block w-full pl-10 pr-3.5 py-2.5 border border-gray-200 rounded-lg text-[14px] text-black placeholder:text-gray-300 focus:outline-none focus:ring-2 focus:ring-[#2a2468] focus:border-transparent transition-all bg-white tracking-widest"
          />
        </div>
        {errors.new_password && (
          <p className="text-red-500 text-xs font-medium mt-1">{errors.new_password.message}</p>
        )}
      </div>

      {/* Confirm Password */}
      <div className="space-y-2">
        <label htmlFor="confirm_password" className="block text-[13px] font-medium text-gray-700">Confirm Password</label>
        <div className="relative">
          <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none">
            <RefreshCw className="h-4 w-4 text-gray-400" />
          </div>
          <input
            type="password"
            id="confirm_password"
            placeholder="••••••••"
            {...register("confirm_password")}
            className="block w-full pl-10 pr-3.5 py-2.5 border border-gray-200 rounded-lg text-[14px] text-black placeholder:text-gray-300 focus:outline-none focus:ring-2 focus:ring-[#2a2468] focus:border-transparent transition-all bg-white tracking-widest"
          />
        </div>
        {errors.confirm_password && (
          <p className="text-red-500 text-xs font-medium mt-1">{errors.confirm_password.message}</p>
        )}
      </div>

      {/* Feedback messages */}
      {error && (
        <div className="text-red-500 text-sm font-medium mt-2">
          {error}
        </div>
      )}
      
      {successMsg && (
        <div className="text-green-600 text-sm font-medium mt-2">
          {successMsg}
        </div>
      )}

      {/* Submit Button */}
      <button
        type="submit"
        disabled={isLoading}
        className="w-full bg-[#36307a] hover:bg-[#2a2468] text-white text-[14px] font-bold py-3.5 rounded-xl shadow-sm transition-all mt-4 disabled:opacity-70 flex items-center justify-center cursor-pointer"
      >
        {isLoading ? <Loader2 className="w-5 h-5 animate-spin" /> : "Reset Password"}
      </button>
    </form>
  );
}
