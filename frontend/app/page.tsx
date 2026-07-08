"use client";

import { useAuthStore } from "@/store/authStore";
import Link from "next/link";
import { LogOut, Home as HomeIcon } from "lucide-react";
import { useRouter } from "next/navigation";

export default function Home() {
  const { user, isAuthenticated, logout } = useAuthStore();
  const router = useRouter();

  const handleLogout = () => {
    logout();
    router.push("/login");
  };

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col items-center justify-center p-4 font-sans">
      <div className="bg-white rounded-[20px] shadow-[0_2px_10px_rgba(0,0,0,0.02)] border border-gray-100 p-10 w-full max-w-[520px] text-center">
        
        <div className="w-16 h-16 bg-[#2a2468]/10 rounded-2xl flex items-center justify-center mx-auto mb-6">
          <HomeIcon className="w-8 h-8 text-[#2a2468]" />
        </div>

        {isAuthenticated ? (
          <>
            <h1 className="text-[28px] font-bold text-gray-900 mb-2 tracking-tight">
              Welcome, {user?.name && user?.email || "User"}!
            </h1>
            <p className="text-[15px] text-gray-500 mb-8">
              You have successfully logged into WorkPilot AI.
            </p>

            <button
              onClick={handleLogout}
              className="inline-flex items-center justify-center gap-2 bg-red-50 hover:bg-red-100 text-red-600 font-bold text-[14px] py-3 px-6 rounded-xl transition-colors"
            >
              <LogOut className="w-4 h-4" />
              Sign Out
            </button>
          </>
        ) : (
          <>
            <h1 className="text-[28px] font-bold text-gray-900 mb-2 tracking-tight">
              WorkPilot AI
            </h1>
            <p className="text-[15px] text-gray-500 mb-8">
              Please sign in to access your dashboard.
            </p>

            <div className="flex flex-col sm:flex-row justify-center gap-4">
              <Link 
                href="/login"
                className="bg-[#36307a] hover:bg-[#2a2468] text-white font-bold text-[14px] py-3 px-8 rounded-xl shadow-sm transition-all text-center"
              >
                Log In
              </Link>
              <Link 
                href="/register"
                className="bg-white hover:bg-gray-50 text-gray-700 font-bold text-[14px] py-3 px-8 rounded-xl shadow-sm border border-gray-200 transition-all text-center"
              >
                Create Account
              </Link>
            </div>
          </>
        )}
      </div>
    </div>
  );
}
