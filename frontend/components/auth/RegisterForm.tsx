"use client";

import { useState } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import * as z from "zod";
import { User, Mail, Building, Lock, RefreshCw, Loader2, Eye, EyeOff } from "lucide-react";
import { registerUseCase } from "@/use-cases/auth/register";
import { useRouter } from "next/navigation";

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
    defaultValues: {
      company_name: "",
      full_name: "",
      email: "",
      password: "",
      confirm_password: "",
    },
  });

  const generateAndSetPassword = () => {
    const chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*()_+";
    let pwd = "";
    for (let i = 0; i < 14; i++) {
      pwd += chars.charAt(Math.floor(Math.random() * chars.length));
    }
    // Guarantee complex characters
    pwd += "A1!";
    
    // Automatically set values and keep passwords hidden initially
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
      {/* Company Name */}
      <div className="space-y-2">
        <label className="block text-[13px] font-medium text-gray-700">Company Name</label>
        <div className="relative">
          <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none">
            <Building className="h-4 w-4 text-gray-400" />
          </div>
          <input
            type="text"
            placeholder="Workpilot Inc."
            {...register("company_name")}
            className="block w-full pl-10 pr-3.5 py-2.5 border border-gray-200 rounded-lg text-[14px] text-black placeholder:text-gray-300 focus:outline-none focus:ring-2 focus:ring-[#2a2468] focus:border-transparent transition-all bg-white"
          />
        </div>
        {errors.company_name && <p className="text-red-500 text-[11px] font-medium mt-1">{errors.company_name.message}</p>}
      </div>

      {/* Full Name */}
      <div className="space-y-2">
        <label className="block text-[13px] font-medium text-gray-700">Full Name</label>
        <div className="relative">
          <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none">
            <User className="h-4 w-4 text-gray-400" />
          </div>
          <input
            type="text"
            placeholder="John Doe"
            {...register("full_name")}
            className="block w-full pl-10 pr-3.5 py-2.5 border border-gray-200 rounded-lg text-[14px] text-black placeholder:text-gray-300 focus:outline-none focus:ring-2 focus:ring-[#2a2468] focus:border-transparent transition-all bg-white"
          />
        </div>
        {errors.full_name && <p className="text-red-500 text-[11px] font-medium mt-1">{errors.full_name.message}</p>}
      </div>

      {/* Work Email */}
      <div className="space-y-2">
        <label className="block text-[13px] font-medium text-gray-700">Work Email</label>
        <div className="relative">
          <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none">
            <Mail className="h-4 w-4 text-gray-400" />
          </div>
          <input
            type="email"
            placeholder="name@company.com"
            {...register("email")}
            className="block w-full pl-10 pr-3.5 py-2.5 border border-gray-200 rounded-lg text-[14px] text-black placeholder:text-gray-300 focus:outline-none focus:ring-2 focus:ring-[#2a2468] focus:border-transparent transition-all bg-white"
          />
        </div>
        {errors.email && <p className="text-red-500 text-[11px] font-medium mt-1">{errors.email.message}</p>}
      </div>

      {/* Password and Confirm Password Row */}
      <div className="relative">
        <div className="grid grid-cols-2 gap-4">
          <div className="space-y-2">
            <div className="flex items-center justify-between">
              <label className="block text-[13px] font-medium text-gray-700">Password</label>
              <div className="flex items-center gap-1">
                <button
                  type="button"
                  onClick={clearPassword}
                  className="text-gray-500 hover:text-red-600 hover:bg-red-50 px-1.5 py-0.5 rounded text-[11px] font-bold transition-colors"
                >
                  Clear
                </button>
                <button
                  type="button"
                  onClick={generateAndSetPassword}
                  className="text-[#36307a] hover:bg-[#36307a]/10 px-1.5 py-0.5 rounded text-[11px] font-bold transition-colors"
                >
                  Generate
                </button>
              </div>
            </div>
            <div className="relative">
              <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none">
                <Lock className="h-4 w-4 text-gray-400" />
              </div>
              <input
                type={showPassword ? "text" : "password"}
                placeholder="••••••••"
                {...register("password")}
                className="block w-full pl-10 pr-10 py-2.5 border border-gray-200 rounded-lg text-[14px] text-black placeholder:text-gray-300 focus:outline-none focus:ring-2 focus:ring-[#2a2468] focus:border-transparent transition-all bg-white"
              />
              <button 
                type="button"
                onClick={() => setShowPassword(!showPassword)}
                className="absolute inset-y-0 right-0 pr-3.5 flex items-center text-gray-400 hover:text-gray-600"
              >
                {showPassword ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
              </button>
            </div>
            {errors.password && <p className="text-red-500 text-[11px] font-medium mt-1">{errors.password.message}</p>}
          </div>

          <div className="space-y-2">
            <label className="block text-[13px] font-medium text-gray-700">Confirm Password</label>
            <div className="relative">
              <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none">
                <RefreshCw className="h-4 w-4 text-gray-400" />
              </div>
              <input
                type={showConfirmPassword ? "text" : "password"}
                placeholder="••••••••"
                {...register("confirm_password")}
                className="block w-full pl-10 pr-10 py-2.5 border border-gray-200 rounded-lg text-[14px] text-black placeholder:text-gray-300 focus:outline-none focus:ring-2 focus:ring-[#2a2468] focus:border-transparent transition-all bg-white"
              />
              <button 
                type="button"
                onClick={() => setShowConfirmPassword(!showConfirmPassword)}
                className="absolute inset-y-0 right-0 pr-3.5 flex items-center text-gray-400 hover:text-gray-600"
              >
                {showConfirmPassword ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
              </button>
            </div>
            {errors.confirm_password && <p className="text-red-500 text-[11px] font-medium mt-1">{errors.confirm_password.message}</p>}
          </div>
        </div>
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
        {isLoading ? <Loader2 className="w-5 h-5 animate-spin" /> : "Create Account"}
      </button>
    </form>
  );
}
