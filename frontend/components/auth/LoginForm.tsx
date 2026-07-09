"use client";

import { useState } from "react";
import { Mail, Lock, Loader2 } from "lucide-react";
import { executeLogin } from "@/use-cases/auth/login";
import { useAuthStore } from "@/store/authStore";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { getTenantDomainUrl } from "@/lib/auth";

export const LoginForm = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const router = useRouter();
  
  const { isLoading, error } = useAuthStore();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const result = await executeLogin({ email, password });
      
      // Redirect to the tenant-specific subdomain
      if (result.user.domain) {
        let url = getTenantDomainUrl(result.user.domain, "/");
        if (result.ssoToken) {
          url += `?sso_token=${result.ssoToken}`;
        }
        window.location.href = url;
      } else {
        router.push("/");
      }
    } catch (err) {
      console.error("Login failed", err);
    }
  };

  return (
    <form className="space-y-5" onSubmit={handleSubmit}>
      
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
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
            placeholder="name@company.com"
            className="block w-full pl-10 pr-3.5 py-2.5 border border-gray-200 rounded-lg text-[14px] text-black placeholder:text-gray-300 focus:outline-none focus:ring-2 focus:ring-[#2a2468] focus:border-transparent transition-all bg-white"
          />
        </div>
      </div>

      {/* Password */}
      <div className="space-y-2">
        <div className="flex items-center justify-between">
          <label className="block text-[13px] font-medium text-gray-700">Password</label>
          <Link href="/forgot-password" className="text-[13px] font-medium text-[#36307a] hover:underline">
            Forgot password?
          </Link>
        </div>
        <div className="relative">
          <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none">
            <Lock className="h-4 w-4 text-gray-400" />
          </div>
          <input
            type="password"
            name="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
            placeholder="••••••••"
            className="block w-full pl-10 pr-3.5 py-2.5 border border-gray-200 rounded-lg text-[14px] text-black placeholder:text-gray-300 focus:outline-none focus:ring-2 focus:ring-[#2a2468] focus:border-transparent transition-all bg-white tracking-widest"
          />
        </div>
      </div>

      {/* Feedback messages */}
      {error && (
        <div className="text-red-500 text-sm font-medium mt-2">
          {error}
        </div>
      )}
      
      {/* Submit Button */}
      <button
        type="submit"
        disabled={isLoading}
        className="w-full bg-[#36307a] hover:bg-[#2a2468] text-white text-[14px] font-bold py-3.5 rounded-xl shadow-sm transition-all mt-4 disabled:opacity-70 flex items-center justify-center"
      >
        {isLoading ? <Loader2 className="w-5 h-5 animate-spin" /> : "Sign in"}
      </button>

      <p className="text-center text-xs text-gray-400 mt-4">
        Test: test@example.com / password
      </p>
    </form>
  );
};
