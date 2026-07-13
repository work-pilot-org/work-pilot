"use client";

import { useState } from "react";
import { Mail, Lock, Loader2, Eye, EyeOff, ShieldCheck, ArrowLeft } from "lucide-react";
import { executeLogin } from "@/use-cases/auth/login";
import { executeMfaLogin } from "@/use-cases/auth/mfa";
import { useAuthStore } from "@/store/authStore";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { getTenantDomainUrl } from "@/lib/auth";

export const LoginForm = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  
  // MFA states
  const [preAuthToken, setPreAuthToken] = useState<string | null>(null);
  const [totpCode, setTotpCode] = useState("");
  
  const router = useRouter();
  
  const { isLoading, error } = useAuthStore();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      if (preAuthToken) {
        // Step 2: MFA Login
        const result = await executeMfaLogin({ preauth_token: preAuthToken, code: totpCode });
        handleLoginSuccess(result);
      } else {
        // Step 1: Password Login
        const result = await executeLogin({ email, password });
        
        if ("mfa_required" in result && result.mfa_required) {
          setPreAuthToken(result.preauth_token);
          return;
        }
        
        handleLoginSuccess(result as any);
      }
    } catch (err) {
      console.error("Login failed", err);
    }
  };

  const handleLoginSuccess = (result: any) => {
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
  };

  return (
    <form className="space-y-4" onSubmit={handleSubmit}>
      
      {/* Step 1: Work Email & Password */}
      {!preAuthToken ? (
        <>
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
                type={showPassword ? "text" : "password"}
                name="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
                placeholder="••••••••"
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
          </div>
        </>
      ) : (
        /* Step 2: MFA Code */
        <div className="space-y-4">
          <div className="flex items-center gap-2 mb-2">
            <button
              type="button"
              onClick={() => setPreAuthToken(null)}
              className="text-gray-500 hover:text-gray-800 transition-colors p-1 -ml-1 rounded-md"
              title="Go back"
            >
              <ArrowLeft className="w-4 h-4" />
            </button>
            <p className="text-[14px] font-medium text-gray-700">Enter your authenticator code</p>
          </div>
          
          <div className="relative">
            <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none">
              <ShieldCheck className="h-4 w-4 text-gray-400" />
            </div>
            <input
              type="text"
              name="totpCode"
              value={totpCode}
              onChange={(e) => setTotpCode(e.target.value.replace(/\D/g, ''))}
              required
              maxLength={6}
              placeholder="000000"
              className="block w-full pl-10 pr-3.5 py-2.5 border border-gray-200 rounded-lg text-[16px] tracking-[0.2em] font-mono text-center text-black placeholder:text-gray-300 focus:outline-none focus:ring-2 focus:ring-[#2a2468] focus:border-transparent transition-all bg-white"
            />
          </div>
        </div>
      )}

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
    </form>
  );
};
