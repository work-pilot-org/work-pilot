"use client";

import { useState } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import * as z from "zod";
import { Mail, Loader2 } from "lucide-react";
import { forgotPasswordUseCase } from "@/use-cases/auth/forgotPassword";

const forgotPasswordSchema = z.object({
  email: z.string().min(1, "Email is required").email("Invalid email address"),
});

type ForgotPasswordFormData = z.infer<typeof forgotPasswordSchema>;

export default function ForgotPasswordForm() {
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [successMsg, setSuccessMsg] = useState<string | null>(null);

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<ForgotPasswordFormData>({
    resolver: zodResolver(forgotPasswordSchema),
    defaultValues: {
      email: "",
    },
  });

  const onSubmit = async (data: ForgotPasswordFormData) => {
    if (isLoading) return;
    setIsLoading(true);
    setError(null);
    setSuccessMsg(null);

    const result = await forgotPasswordUseCase(data);

    if (!result.success) {
      setError(result.error || "An error occurred");
    } else {
      setSuccessMsg(result.data?.message || "If an account exists, a password reset email has been sent.");
    }

    setIsLoading(false);
  };

  return (
    <form className="space-y-5" onSubmit={handleSubmit(onSubmit)}>
      {/* Work Email */}
      <div className="space-y-2">
        <label htmlFor="email" className="block text-[13px] font-medium text-gray-700">Work Email</label>
        <div className="relative">
          <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none">
            <Mail className="h-4 w-4 text-gray-400" />
          </div>
          <input
            type="email"
            id="email"
            placeholder="name@company.com"
            {...register("email")}
            className="block w-full pl-10 pr-3.5 py-2.5 border border-gray-200 rounded-lg text-[14px] text-black placeholder:text-gray-300 focus:outline-none focus:ring-2 focus:ring-[#2a2468] focus:border-transparent transition-all bg-white"
          />
        </div>
        {errors.email && (
          <p className="text-red-500 text-xs font-medium mt-1">{errors.email.message}</p>
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
        {isLoading ? <Loader2 className="w-5 h-5 animate-spin" /> : "Send Reset Link"}
      </button>
    </form>
  );
}
