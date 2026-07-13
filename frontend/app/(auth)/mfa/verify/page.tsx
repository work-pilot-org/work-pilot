import MFAVerificationForm from "@/components/auth/MFAVerificationForm";
import Link from "next/link";
import { Briefcase } from "lucide-react";

export const metadata = {
  title: "Verify MFA | WorkPilot AI",
  description: "Verify your identity using Multi-Factor Authentication",
};

export default async function MFAVerifyPage({
  searchParams,
}: {
  searchParams: Promise<{ [key: string]: string | string[] | undefined }>;
}) {
  const resolvedParams = await searchParams;
  const token = typeof resolvedParams.token === "string" ? resolvedParams.token : "";

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
      <div className="bg-white rounded-[16px] shadow-sm border border-gray-100 p-6 w-full max-w-[400px]">
        <div className="mb-6 text-center">
          <h2 className="text-[20px] font-semibold text-gray-900 mb-1">Two-Factor Verification</h2>
          <p className="text-gray-500 text-[13px]">Enter the code from your authenticator app</p>
        </div>

        {/* The Form Component */}
        <MFAVerificationForm mfaToken={token} />

        <div className="mt-6 text-center text-[13px] text-gray-500 font-medium">
          <Link href="/login" className="text-[#2a2468] font-bold hover:underline">
            Back to Login
          </Link>
        </div>
      </div>
    </div>
  );
}
