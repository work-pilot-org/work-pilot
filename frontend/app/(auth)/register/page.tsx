import RegisterForm from "@/components/auth/RegisterForm";
import Link from "next/link";
import { Briefcase } from "lucide-react";

export default function RegisterPage() {
  return (
    <div className="min-h-screen bg-gray-50 flex flex-col justify-center items-center p-4 font-sans">
      <div className="w-full max-w-[500px]">
        
        {/* Logo Section */}
        <div className="mb-6 text-center flex flex-col items-center">
          <div className="w-10 h-10 bg-gray-900 rounded flex items-center justify-center mb-3">
            <Briefcase className="w-5 h-5 text-white" />
          </div>
          <h1 className="text-xl font-semibold text-gray-900 tracking-tight">WorkPilot AI</h1>
        </div>

        {/* Main Card */}
        <div className="bg-white border border-gray-200 rounded-md shadow-sm p-6">
          <div className="mb-6">
            <h2 className="text-lg font-medium text-gray-900">Create an account</h2>
            <p className="text-sm text-gray-500 mt-1">Set up your workspace</p>
          </div>

          {/* The Form Component */}
          <RegisterForm />

          <div className="mt-6 text-sm text-gray-600">
            Already have an account?{" "}
            <Link href="/login" className="text-blue-600 hover:text-blue-700 hover:underline">
              Sign in
            </Link>
          </div>
        </div>

        {/* Footer Links */}
        <div className="mt-8 flex justify-center gap-6 text-xs text-gray-500">
          <Link href="/privacy" className="hover:text-gray-900 hover:underline">Privacy</Link>
          <Link href="/terms" className="hover:text-gray-900 hover:underline">Terms</Link>
          <Link href="/contact" className="hover:text-gray-900 hover:underline">Contact</Link>
        </div>
      </div>
    </div>
  );
}
