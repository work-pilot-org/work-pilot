"use client";

import { useState } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import * as z from "zod";
import { forgotPasswordUseCase } from "@/use-cases/auth/forgotPassword";
import { Button } from "@/components/ui/Button";
import { Input } from "@/components/ui/Input";
import { Label } from "@/components/ui/Label";

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
    defaultValues: { email: "" },
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
      <div className="space-y-2">
        <Label htmlFor="email">Work Email</Label>
        <Input
          id="email"
          type="email"
          placeholder="name@company.com"
          {...register("email")}
          error={!!errors.email}
        />
        {errors.email && (
          <p className="text-destructive text-xs font-medium mt-1">{errors.email.message}</p>
        )}
      </div>

      {error && <div className="text-destructive text-sm font-medium mt-2">{error}</div>}
      {successMsg && <div className="text-green-600 text-sm font-medium mt-2">{successMsg}</div>}

      <Button type="submit" className="w-full mt-4" isLoading={isLoading}>
        Send Reset Link
      </Button>
    </form>
  );
}
