"use client";

import { useState } from "react";
import { User, Mail, Building, Lock, RefreshCw, Info, Loader2 } from "lucide-react";
import { registerUseCase } from "@/use-cases/auth/register";
import { RegisterRequest } from "@/types/auth";
import { useRouter } from "next/navigation";

export default function RegisterForm() {
  const [formData, setFormData] = useState<RegisterRequest>({
    company_name: "",
    full_name: "",
    email: "",
    password: "",
    confirm_password: "",
  });

  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [successMsg, setSuccessMsg] = useState<string | null>(null);
  const router = useRouter();

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setError(null);
    setSuccessMsg(null);

    const result = await registerUseCase(formData);

    if (!result.success) {
      setError(result.error || "An error occurred");
      setIsLoading(false);
    } else {
      setSuccessMsg(result.data?.message || "Successfully registered! Redirecting to login...");
      setTimeout(() => {
        router.push("/login");
      }, 1500);
    }

    setIsLoading(false);
  };

  return (
    <form className="space-y-5" onSubmit={handleSubmit}>
      
      {/* Company Name */}
      <div className="space-y-2">
        <label className="block text-[13px] font-medium text-gray-700">Company Name</label>
        <div className="relative">
          <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none">
            <Building className="h-4 w-4 text-gray-400" />
          </div>
          <input
            type="text"
            name="company_name"
            value={formData.company_name}
            onChange={handleChange}
            required
            placeholder="Tulip Inc."
            className="block w-full pl-10 pr-3.5 py-2.5 border border-gray-200 rounded-lg text-[14px] text-black placeholder:text-gray-300 focus:outline-none focus:ring-2 focus:ring-[#2a2468] focus:border-transparent transition-all bg-white"
          />
        </div>
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
            name="full_name"
            value={formData.full_name}
            onChange={handleChange}
            required
            placeholder="John Doe"
            className="block w-full pl-10 pr-3.5 py-2.5 border border-gray-200 rounded-lg text-[14px] text-black placeholder:text-gray-300 focus:outline-none focus:ring-2 focus:ring-[#2a2468] focus:border-transparent transition-all bg-white"
          />
        </div>
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
            name="email"
            value={formData.email}
            onChange={handleChange}
            required
            placeholder="name@company.com"
            className="block w-full pl-10 pr-3.5 py-2.5 border border-gray-200 rounded-lg text-[14px] text-black placeholder:text-gray-300 focus:outline-none focus:ring-2 focus:ring-[#2a2468] focus:border-transparent transition-all bg-white"
          />
        </div>
      </div>

      {/* Password and Confirm Password Row */}
      <div className="grid grid-cols-2 gap-4">
        <div className="space-y-2">
          <label className="block text-[13px] font-medium text-gray-700">Password</label>
          <div className="relative">
            <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none">
              <Lock className="h-4 w-4 text-gray-400" />
            </div>
            <input
              type="password"
              name="password"
              value={formData.password}
              onChange={handleChange}
              required
              minLength={8}
              placeholder="••••••••"
              className="block w-full pl-10 pr-3.5 py-2.5 border border-gray-200 rounded-lg text-[14px] text-black placeholder:text-gray-300 focus:outline-none focus:ring-2 focus:ring-[#2a2468] focus:border-transparent transition-all bg-white tracking-widest"
            />
          </div>
        </div>

        <div className="space-y-2">
          <label className="block text-[13px] font-medium text-gray-700">Confirm Password</label>
          <div className="relative">
            <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none">
              <RefreshCw className="h-4 w-4 text-gray-400" />
            </div>
            <input
              type="password"
              name="confirm_password"
              value={formData.confirm_password}
              onChange={handleChange}
              required
              minLength={8}
              placeholder="••••••••"
              className="block w-full pl-10 pr-3.5 py-2.5 border border-gray-200 rounded-lg text-[14px] text-black placeholder:text-gray-300 focus:outline-none focus:ring-2 focus:ring-[#2a2468] focus:border-transparent transition-all bg-white tracking-widest"
            />
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
        className="w-full bg-[#36307a] hover:bg-[#2a2468] text-white text-[14px] font-bold py-3.5 rounded-xl shadow-sm transition-all mt-4 disabled:opacity-70 flex items-center justify-center"
      >
        {isLoading ? <Loader2 className="w-5 h-5 animate-spin" /> : "Create Account"}
      </button>

    </form>
  );
}
