"use client";

import { useState } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import * as z from "zod";
import { Eye, EyeOff } from "lucide-react";
import { resetPasswordUseCase } from "@/use-cases/auth/resetPassword";
import { useRouter } from "next/navigation";
import { Button } from "@/components/ui/Button";
import { Input } from "@/components/ui/Input";
import { Label } from "@/components/ui/Label";

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
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<ResetPasswordFormData>({
    resolver: zodResolver(resetPasswordSchema),
    defaultValues: { new_password: "", confirm_password: "" },
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
      <div className="bg-destructive/10 text-destructive p-4 rounded-xl text-sm font-medium text-center">
        Reset token is missing or invalid. Please check your password recovery link.
      </div>
    );
  }

  return (
    <form className="space-y-5" onSubmit={handleSubmit(onSubmit)}>
      <div className="space-y-2">
        <Label htmlFor="new_password">New Password</Label>
        <div className="relative">
          <Input
            id="new_password"
            type={showPassword ? "text" : "password"}
            placeholder="••••••••"
            {...register("new_password")}
            error={!!errors.new_password}
            className="pr-10 tracking-widest"
          />
          <button 
            type="button"
            onClick={() => setShowPassword(!showPassword)}
            className="absolute inset-y-0 right-0 pr-3 flex items-center text-muted-foreground hover:text-foreground"
          >
            {showPassword ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
          </button>
        </div>
        {errors.new_password && (
          <p className="text-destructive text-xs font-medium mt-1">{errors.new_password.message}</p>
        )}
      </div>

      <div className="space-y-2">
        <Label htmlFor="confirm_password">Confirm Password</Label>
        <div className="relative">
          <Input
            id="confirm_password"
            type={showConfirmPassword ? "text" : "password"}
            placeholder="••••••••"
            {...register("confirm_password")}
            error={!!errors.confirm_password}
            className="pr-10 tracking-widest"
          />
          <button 
            type="button"
            onClick={() => setShowConfirmPassword(!showConfirmPassword)}
            className="absolute inset-y-0 right-0 pr-3 flex items-center text-muted-foreground hover:text-foreground"
          >
            {showConfirmPassword ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
          </button>
        </div>
        {errors.confirm_password && (
          <p className="text-destructive text-xs font-medium mt-1">{errors.confirm_password.message}</p>
        )}
      </div>

      {error && <div className="text-destructive text-sm font-medium mt-2">{error}</div>}
      {successMsg && <div className="text-green-600 text-sm font-medium mt-2">{successMsg}</div>}

      <Button type="submit" className="w-full mt-4" isLoading={isLoading}>
        Reset Password
      </Button>
    </form>
  );
}
