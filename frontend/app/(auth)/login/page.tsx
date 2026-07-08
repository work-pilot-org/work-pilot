import { LoginForm } from "@/components/auth/LoginForm";
import Link from "next/link";
import { Briefcase } from "lucide-react";

export const metadata = {
  title: "Login | WorkPilot AI",
  description: "Sign in to your WorkPilot AI account",
};

export default function LoginPage() {
  return (
    <div className="min-h-screen bg-gray-50 flex flex-col justify-center items-center p-4 font-sans">
      {/* Logo Section */}
      <div className="mb-6 text-center">
        <div className="w-12 h-12 bg-[#2a2468] rounded-xl flex items-center justify-center mx-auto mb-4">
          <Briefcase className="w-6 h-6 text-white" />
        </div>
        <h1 className="text-[28px] font-bold text-[#2a2468] tracking-tight">WorkPilot AI</h1>
        <p className="text-[13px] font-medium text-gray-500 mt-0.5">Enterprise SaaS Solutions</p>
      </div>

      {/* Main Card */}
      <div className="bg-white rounded-[20px] shadow-[0_2px_10px_rgba(0,0,0,0.02)] border border-gray-100 p-8 w-full max-w-[420px]">
        <div className="mb-8">
          <h2 className="text-[22px] font-bold text-gray-900 mb-1.5">Welcome back</h2>
          <p className="text-gray-500 text-[14px]">Sign in to your account.</p>
        </div>

        {/* The Form Component */}
        <LoginForm />

        <div className="mt-8 text-center text-[13px] text-gray-500 font-medium">
          Don't have an account?{" "}
          <Link href="/register" className="text-[#2a2468] font-bold hover:underline">
            Sign up
          </Link>
        </div>
      </div>

      {/* Footer Links */}
      <div className="mt-8 flex gap-8 text-[12px] font-medium text-gray-400">
        <Link href="/privacy" className="hover:text-gray-600 transition-colors">Privacy Policy</Link>
        <Link href="/terms" className="hover:text-gray-600 transition-colors">Terms of Service</Link>
        <Link href="/help" className="hover:text-gray-600 transition-colors">Help Center</Link>
      </div>
    </div>
  );
}
