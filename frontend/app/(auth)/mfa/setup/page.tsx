import MFASetupForm from "@/components/auth/MFASetupForm";
import Link from "next/link";
import { Briefcase } from "lucide-react";

export const metadata = {
  title: "Setup MFA | WorkPilot AI",
  description: "Setup Multi-Factor Authentication for your WorkPilot AI account",
};

export default function MFASetupPage() {
  return (
    <div className="min-h-screen bg-gray-50 flex flex-col justify-center items-center p-4 font-sans">
      {/* Logo Section */}
      <div className="mb-6 text-center flex flex-col items-center">
        <div className="w-10 h-10 bg-[#2a2468] rounded-xl flex items-center justify-center mb-2 shadow-sm">
          <Briefcase className="w-5 h-5 text-white" />
        </div>
        <h1 className="text-[24px] font-bold text-[#2a2468] tracking-tight">WorkPilot AI</h1>
      </div>

      {/* Main Card */}
      <div className="bg-white rounded-[16px] shadow-sm border border-gray-100 p-6 w-full max-w-[440px]">
        <div className="mb-6 text-center">
          <h2 className="text-[20px] font-semibold text-gray-900 mb-1">Configure MFA</h2>
          <p className="text-gray-500 text-[13px]">Protect your account with two-factor security</p>
        </div>

        {/* The Form Component */}
        <MFASetupForm />

        <div className="mt-6 text-center text-[13px] text-gray-500 font-medium">
          <Link href="/" className="text-[#2a2468] font-bold hover:underline">
            Back to Dashboard
          </Link>
        </div>
      </div>
    </div>
  );
}
