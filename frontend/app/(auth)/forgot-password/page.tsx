import ForgotPasswordForm from "@/components/auth/ForgotPasswordForm";
import Link from "next/link";
import { Briefcase } from "lucide-react";

export default function ForgotPasswordPage() {
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
      <div className="bg-white rounded-[20px] shadow-[0_2px_10px_rgba(0,0,0,0.02)] border border-gray-100 p-8 w-full max-w-[520px]">
        <div className="mb-8">
          <h2 className="text-[22px] font-bold text-gray-900 mb-1.5">Reset your password</h2>
          <p className="text-gray-500 text-[14px]">Enter your work email address and we'll send you a recovery link.</p>
        </div>

        {/* The Form Component */}
        <ForgotPasswordForm />

        <div className="mt-8 text-center text-[13px] text-gray-500 font-medium">
          Remember your password?{" "}
          <Link href="/login" className="text-[#2a2468] font-bold hover:underline">
            Log in
          </Link>
        </div>
      </div>
    </div>
  );
}
