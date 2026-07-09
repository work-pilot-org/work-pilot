import RegisterForm from "@/components/auth/RegisterForm";
import Link from "next/link";
import { Briefcase } from "lucide-react";

export default function RegisterPage() {
  return (
    <div className="min-h-screen bg-gray-50 flex flex-col justify-center items-center p-4 font-sans">
      {/* Logo Section */}
      <div className="mb-4 text-center flex flex-col items-center">
        <div className="w-10 h-10 bg-[#2a2468] rounded-xl flex items-center justify-center mb-2 shadow-sm">
          <Briefcase className="w-5 h-5 text-white" />
        </div>
        <h1 className="text-[24px] font-bold text-[#2a2468] tracking-tight">WorkPilot AI</h1>
      </div>

      {/* Main Card */}
      <div className="bg-white rounded-[16px] shadow-sm border border-gray-100 p-6 w-full max-w-[500px]">
        <div className="mb-5 text-center">
          <h2 className="text-[20px] font-semibold text-gray-900 mb-1">Create your account</h2>
          <p className="text-gray-500 text-[13px]">Join the next generation of AI workflow</p>
        </div>

        {/* The Form Component */}
        <RegisterForm />

        <div className="mt-6 text-center text-[13px] text-gray-500 font-medium">
          Already have an account?{" "}
          <Link href="/login" className="text-[#2a2468] font-bold hover:underline">
            Log in
          </Link>
        </div>
      </div>

      {/* Footer Links */}
      <div className="mt-6 flex gap-6 text-[12px] font-medium text-gray-400">
        <Link href="/privacy" className="hover:text-gray-600 transition-colors">Privacy</Link>
        <Link href="/terms" className="hover:text-gray-600 transition-colors">Terms</Link>
        <Link href="/contact" className="hover:text-gray-600 transition-colors">Contact</Link>
        <Link href="/help" className="hover:text-gray-600 transition-colors">Help</Link>
      </div>
    </div>
  );
}
