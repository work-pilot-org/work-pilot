"use client";

import { useState } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import * as z from "zod";
import { Eye, EyeOff } from "lucide-react";
import { registerUseCase } from "@/use-cases/auth/register";
import { useRouter } from "next/navigation";
import { Button } from "@/components/ui/Button";
import { Input } from "@/components/ui/Input";
import { Label } from "@/components/ui/Label";

const registerSchema = z.object({
  company_name: z.string().min(2, "Company name must be at least 2 characters"),
  full_name: z.string().min(2, "Full name must be at least 2 characters"),
  email: z.string().email("Please enter a valid email address"),
  password: z.string().min(8, "Password must be at least 8 characters"),
  confirm_password: z.string().min(1, "Please confirm your password"),
}).refine((data) => data.password === data.confirm_password, {
  message: "Passwords do not match",
  path: ["confirm_password"],
});

type RegisterFormData = z.infer<typeof registerSchema>;

export default function RegisterForm() {
  const router = useRouter();
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [successMsg, setSuccessMsg] = useState<string | null>(null);
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);

  const {
    register,
    handleSubmit,
    setValue,
    formState: { errors },
  } = useForm<RegisterFormData>({
    resolver: zodResolver(registerSchema),
    defaultValues: { company_name: "", full_name: "", email: "", password: "", confirm_password: "" },
  });

  const generateAndSetPassword = () => {
    const chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*()_+";
    let pwd = "";
    for (let i = 0; i < 14; i++) {
      pwd += chars.charAt(Math.floor(Math.random() * chars.length));
    }
    pwd += "A1!";
    setValue("password", pwd, { shouldValidate: true });
    setValue("confirm_password", pwd, { shouldValidate: true });
    setShowPassword(false);
    setShowConfirmPassword(false);
  };

  const clearPassword = () => {
    setValue("password", "", { shouldValidate: true });
    setValue("confirm_password", "", { shouldValidate: true });
    setShowPassword(false);
    setShowConfirmPassword(false);
  };

  const onSubmit = async (data: RegisterFormData) => {
    setIsLoading(true);
    setError(null);
    setSuccessMsg(null);

    const result = await registerUseCase(data);

    if (!result.success) {
      setError(result.error || "An error occurred");
      setIsLoading(false);
    } else {
      setSuccessMsg(result.data?.message || "Successfully registered! Redirecting...");
      setTimeout(() => {
        router.push("/login");
      }, 1500);
    }
  };

  return (
    <form className="space-y-4" onSubmit={handleSubmit(onSubmit)}>
      <div className="space-y-2">
        <Label htmlFor="company_name">Company Name</Label>
        <Input
          id="company_name"
          type="text"
          placeholder="Workpilot Inc."
          {...register("company_name")}
          error={!!errors.company_name}
        />
        {errors.company_name && <p className="text-destructive text-xs">{errors.company_name.message}</p>}
      </div>

      <div className="space-y-2">
        <Label htmlFor="full_name">Full Name</Label>
        <Input
          id="full_name"
          type="text"
          placeholder="John Doe"
          {...register("full_name")}
          error={!!errors.full_name}
        />
        {errors.full_name && <p className="text-destructive text-xs">{errors.full_name.message}</p>}
      </div>

      <div className="space-y-2">
        <Label htmlFor="email">Work Email</Label>
        <Input
          id="email"
          type="email"
          placeholder="name@company.com"
          {...register("email")}
          error={!!errors.email}
        />
        {errors.email && <p className="text-destructive text-xs">{errors.email.message}</p>}
      </div>

      <div className="grid grid-cols-2 gap-4">
        <div className="space-y-2">
          <div className="flex items-center justify-between">
            <Label htmlFor="password">Password</Label>
            <div className="flex items-center gap-2">
              <button type="button" onClick={clearPassword} className="text-muted-foreground hover:text-destructive text-xs font-medium">Clear</button>
              <button type="button" onClick={generateAndSetPassword} className="text-primary hover:underline text-xs font-medium">Generate</button>
            </div>
          </div>
          <div className="relative">
            <Input
              id="password"
              type={showPassword ? "text" : "password"}
              placeholder="••••••••"
              {...register("password")}
              error={!!errors.password}
              className="pr-10"
            />
            <button 
              type="button"
              onClick={() => setShowPassword(!showPassword)}
              className="absolute inset-y-0 right-0 pr-3 flex items-center text-muted-foreground hover:text-foreground"
            >
              {showPassword ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
            </button>
          </div>
          {errors.password && <p className="text-destructive text-xs">{errors.password.message}</p>}
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
              className="pr-10"
            />
            <button 
              type="button"
              onClick={() => setShowConfirmPassword(!showConfirmPassword)}
              className="absolute inset-y-0 right-0 pr-3 flex items-center text-muted-foreground hover:text-foreground"
            >
              {showConfirmPassword ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
            </button>
          </div>
          {errors.confirm_password && <p className="text-destructive text-xs">{errors.confirm_password.message}</p>}
        </div>
      </div>

      {error && <div className="text-destructive text-sm font-medium mt-2 bg-destructive/10 p-3 rounded-md border border-destructive/20">{error}</div>}
      {successMsg && <div className="text-green-700 text-sm font-medium mt-2 bg-green-50 p-3 rounded-md border border-green-200">{successMsg}</div>}

      <Button type="submit" className="w-full mt-4" isLoading={isLoading}>
        Create Account
      </Button>
    </form>
  );
}
