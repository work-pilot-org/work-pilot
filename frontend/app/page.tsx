"use client";

import { useAuthStore } from "@/store/authStore";
import Link from "next/link";
import { LayoutDashboard, Shield, Users, Zap, ArrowRight } from "lucide-react";
import { useRouter } from "next/navigation";
import { useEffect } from "react";
import { getBaseDomainUrl } from "@/lib/auth";

export default function Home() {
  const { isAuthenticated, isInitialized } = useAuthStore();
  const router = useRouter();

  useEffect(() => {
    if (isInitialized && isAuthenticated) {
      router.replace("/dashboard");
    }
  }, [isInitialized, isAuthenticated, router]);

  if (!isInitialized || isAuthenticated) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center p-4">
        <div className="animate-pulse bg-white rounded-2xl shadow-sm border border-gray-100 p-10 w-full max-w-4xl h-[400px]">
          <div className="flex flex-col items-center justify-center h-full gap-4">
            <div className="w-16 h-16 bg-gray-200 rounded-xl"></div>
            <div className="w-48 h-6 bg-gray-200 rounded-full"></div>
            <div className="w-32 h-4 bg-gray-200 rounded-full mt-4"></div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 font-sans flex flex-col">
      {/* Header */}
      <header className="border-b border-gray-200 bg-white sticky top-0 z-10">
        <div className="max-w-7xl mx-auto px-6 h-16 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 bg-[#2a2468] rounded-lg flex items-center justify-center">
              <LayoutDashboard className="w-4 h-4 text-white" />
            </div>
            <span className="font-bold text-[18px] text-[#2a2468] tracking-tight">WorkPilot AI</span>
          </div>
          <div className="flex items-center gap-4">
            <a href={getBaseDomainUrl("/login")} className="text-[14px] font-medium text-gray-600 hover:text-gray-900 transition-colors">
              Log in
            </a>
            <a href={getBaseDomainUrl("/register")} className="bg-[#36307a] hover:bg-[#2a2468] text-white text-[14px] font-medium px-4 py-2 rounded-lg transition-colors shadow-sm">
              Get Started
            </a>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="flex-1 flex flex-col">
        <div className="flex-1 flex flex-col">
          {/* Hero Section */}
          <section className="py-20 px-6 text-center max-w-4xl mx-auto">
            <h1 className="text-[44px] md:text-[56px] font-extrabold text-gray-900 tracking-tight leading-tight mb-6">
              Next-generation <span className="text-transparent bg-clip-text bg-gradient-to-r from-[#2a2468] to-[#5c54b4]">AI Workflow Management</span>
            </h1>
            <p className="text-[18px] text-gray-500 mb-10 max-w-2xl mx-auto leading-relaxed">
              Empower your enterprise with seamless multi-tenant architecture, robust security, and intelligent automation built for modern teams.
            </p>
            <div className="flex flex-col sm:flex-row justify-center gap-4">
              <a href={getBaseDomainUrl("/register")} className="bg-[#36307a] hover:bg-[#2a2468] text-white font-medium text-[15px] py-3 px-8 rounded-xl shadow-sm transition-all flex items-center justify-center gap-2">
                Start Free Trial <ArrowRight className="w-4 h-4" />
              </a>
              <a href={getBaseDomainUrl("/login")} className="bg-white hover:bg-gray-50 text-gray-700 font-medium text-[15px] py-3 px-8 rounded-xl shadow-sm border border-gray-200 transition-all flex items-center justify-center">
                Sign In to Workspace
              </a>
            </div>
          </section>

          {/* Features Section */}
          <section className="bg-white border-t border-gray-100 py-20 px-6 flex-1">
            <div className="max-w-6xl mx-auto">
              <div className="text-center mb-16">
                <h2 className="text-[28px] font-bold text-gray-900 tracking-tight">Enterprise-grade Infrastructure</h2>
              </div>
              <div className="grid md:grid-cols-3 gap-8">
                <div className="p-6 rounded-2xl bg-gray-50 border border-gray-100 hover:border-gray-200 transition-colors">
                  <div className="w-12 h-12 bg-white rounded-xl flex items-center justify-center mb-4 shadow-sm text-[#2a2468]">
                    <Users className="w-6 h-6" />
                  </div>
                  <h3 className="text-[18px] font-bold text-gray-900 mb-2">Multi-tenant Architecture</h3>
                  <p className="text-[14px] text-gray-500 leading-relaxed">
                    True data isolation with separate database schemas for each organization, ensuring complete privacy and compliance.
                  </p>
                </div>
                <div className="p-6 rounded-2xl bg-gray-50 border border-gray-100 hover:border-gray-200 transition-colors">
                  <div className="w-12 h-12 bg-white rounded-xl flex items-center justify-center mb-4 shadow-sm text-[#2a2468]">
                    <Shield className="w-6 h-6" />
                  </div>
                  <h3 className="text-[18px] font-bold text-gray-900 mb-2">Advanced Security</h3>
                  <p className="text-[14px] text-gray-500 leading-relaxed">
                    Bank-grade encryption, secure JWT sessions, and rigorous cross-origin protection built into the core.
                  </p>
                </div>
                <div className="p-6 rounded-2xl bg-gray-50 border border-gray-100 hover:border-gray-200 transition-colors">
                  <div className="w-12 h-12 bg-white rounded-xl flex items-center justify-center mb-4 shadow-sm text-[#2a2468]">
                    <Zap className="w-6 h-6" />
                  </div>
                  <h3 className="text-[18px] font-bold text-gray-900 mb-2">Lightning Fast</h3>
                  <p className="text-[14px] text-gray-500 leading-relaxed">
                    Powered by Next.js and FastAPI for sub-millisecond response times and an ultra-smooth user experience.
                  </p>
                </div>
              </div>
            </div>
          </section>
        </div>
      </main>

      {/* Footer */}
      <footer className="bg-white border-t border-gray-100 py-8 px-6 mt-auto">
        <div className="max-w-7xl mx-auto flex flex-col md:flex-row items-center justify-between gap-4">
          <div className="text-[13px] text-gray-500">
            &copy; {new Date().getFullYear()} WorkPilot AI. All rights reserved.
          </div>
          <div className="flex gap-6 text-[13px] font-medium text-gray-500">
            <Link href="/privacy" className="hover:text-gray-900 transition-colors">Privacy</Link>
            <Link href="/terms" className="hover:text-gray-900 transition-colors">Terms</Link>
            <Link href="/contact" className="hover:text-gray-900 transition-colors">Contact</Link>
            <Link href="/help" className="hover:text-gray-900 transition-colors">Help</Link>
          </div>
        </div>
      </footer>
    </div>
  );
}
