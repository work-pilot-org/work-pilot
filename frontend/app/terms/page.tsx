import Link from "next/link";
import { ArrowLeft } from "lucide-react";

export default function TermsPage() {
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
          <h1 className="text-[32px] font-bold text-gray-900 mb-6 tracking-tight">Terms of Service</h1>
          <p className="text-sm text-gray-500 mb-8">Last updated: July 2026</p>
          
          <div className="space-y-6 text-[15px] text-gray-700 leading-relaxed">
            <section>
              <h2 className="text-[18px] font-bold text-gray-900 mb-3">1. Acceptance of Terms</h2>
              <p>By accessing or using the WorkPilot AI platform, you agree to be bound by these Terms of Service and all applicable laws and regulations. If you do not agree with any of these terms, you are prohibited from using or accessing this site.</p>
            </section>
            
            <section>
              <h2 className="text-[18px] font-bold text-gray-900 mb-3">2. Use License</h2>
              <p>Permission is granted to temporarily access the materials on WorkPilot AI's platform for personal, non-commercial transitory viewing only. This is the grant of a license, not a transfer of title.</p>
            </section>

            <section>
              <h2 className="text-[18px] font-bold text-gray-900 mb-3">3. Disclaimer</h2>
              <p>The materials on WorkPilot AI's platform are provided on an 'as is' basis. We make no warranties, expressed or implied, and hereby disclaim and negate all other warranties including, without limitation, implied warranties or conditions of merchantability, fitness for a particular purpose, or non-infringement of intellectual property or other violation of rights.</p>
            </section>

            <section>
              <h2 className="text-[18px] font-bold text-gray-900 mb-3">4. Limitations</h2>
              <p>In no event shall WorkPilot AI or its suppliers be liable for any damages (including, without limitation, damages for loss of data or profit, or due to business interruption) arising out of the use or inability to use the materials on WorkPilot AI's platform.</p>
            </section>
          </div>
        </div>
      </main>
    </div>
  );
}
