import Link from "next/link";
import { ArrowLeft, BookOpen, MessageCircle, HelpCircle } from "lucide-react";

export default function HelpPage() {
  return (
    <div className="min-h-screen bg-gray-50 font-sans">
      <header className="bg-white border-b border-gray-200 sticky top-0 z-10">
        <div className="max-w-3xl mx-auto px-6 h-16 flex items-center">
          <Link href="/" className="text-gray-500 hover:text-gray-900 flex items-center gap-2 text-[14px] font-medium transition-colors">
            <ArrowLeft className="w-4 h-4" /> Back to Home
          </Link>
        </div>
      </header>
      
      <main className="max-w-3xl mx-auto px-6 py-12">
        <div className="bg-white rounded-2xl shadow-sm border border-gray-100 p-8 md:p-12">
          <h1 className="text-[32px] font-bold text-gray-900 mb-6 tracking-tight">Help Center</h1>
          <p className="text-[15px] text-gray-500 mb-8 leading-relaxed">
            Welcome to the WorkPilot AI Help Center. Browse our resources below or reach out to our team if you need personalized assistance.
          </p>
          
          <div className="grid sm:grid-cols-2 gap-6">
            <div className="p-6 rounded-2xl bg-gray-50 border border-gray-100 hover:border-gray-200 transition-colors cursor-pointer">
              <div className="w-10 h-10 bg-[#36307a]/10 rounded-xl flex items-center justify-center mb-4 text-[#36307a]">
                <BookOpen className="w-5 h-5" />
              </div>
              <h3 className="text-[16px] font-bold text-gray-900 mb-2">Documentation</h3>
              <p className="text-[13px] text-gray-500 leading-relaxed">
                Read comprehensive guides, API references, and tutorials on how to set up and manage your workspace.
              </p>
            </div>

            <div className="p-6 rounded-2xl bg-gray-50 border border-gray-100 hover:border-gray-200 transition-colors cursor-pointer">
              <div className="w-10 h-10 bg-[#36307a]/10 rounded-xl flex items-center justify-center mb-4 text-[#36307a]">
                <HelpCircle className="w-5 h-5" />
              </div>
              <h3 className="text-[16px] font-bold text-gray-900 mb-2">FAQs</h3>
              <p className="text-[13px] text-gray-500 leading-relaxed">
                Find quick answers to common questions about billing, multi-tenant setup, and user management.
              </p>
            </div>

            <div className="p-6 rounded-2xl bg-gray-50 border border-gray-100 hover:border-gray-200 transition-colors cursor-pointer">
              <div className="w-10 h-10 bg-[#36307a]/10 rounded-xl flex items-center justify-center mb-4 text-[#36307a]">
                <MessageCircle className="w-5 h-5" />
              </div>
              <h3 className="text-[16px] font-bold text-gray-900 mb-2">Community Forum</h3>
              <p className="text-[13px] text-gray-500 leading-relaxed">
                Join the discussion. Share tips, feature requests, and connect with other WorkPilot AI users.
              </p>
            </div>
            
            <Link href="/contact" className="p-6 rounded-2xl bg-gray-50 border border-gray-100 hover:border-[#36307a]/30 hover:bg-[#36307a]/5 transition-colors block">
              <div className="w-10 h-10 bg-white rounded-xl flex items-center justify-center mb-4 text-[#36307a] shadow-sm">
                <ArrowLeft className="w-5 h-5 rotate-135" /> 
              </div>
              <h3 className="text-[16px] font-bold text-gray-900 mb-2">Still need help?</h3>
              <p className="text-[13px] text-gray-500 leading-relaxed">
                Can't find what you're looking for? Contact our support team directly.
              </p>
            </Link>
          </div>
        </div>
      </main>
    </div>
  );
}
