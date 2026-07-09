import Link from "next/link";
import { ArrowLeft } from "lucide-react";

export default function PrivacyPage() {
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
          <h1 className="text-[32px] font-bold text-gray-900 mb-6 tracking-tight">Privacy Policy</h1>
          <p className="text-sm text-gray-500 mb-8">Last updated: July 2026</p>
          
          <div className="space-y-6 text-[15px] text-gray-700 leading-relaxed">
            <section>
              <h2 className="text-[18px] font-bold text-gray-900 mb-3">1. Information We Collect</h2>
              <p>We collect information you provide directly to us when you create an account, update your profile, use the interactive features of our services, or communicate with us. This may include your name, email address, company name, and any other information you choose to provide.</p>
            </section>
            
            <section>
              <h2 className="text-[18px] font-bold text-gray-900 mb-3">2. How We Use Information</h2>
              <p>We use the information we collect to provide, maintain, and improve our services, to develop new features, and to protect WorkPilot AI and our users. We may also use the information to send you technical notices, updates, and support messages.</p>
            </section>

            <section>
              <h2 className="text-[18px] font-bold text-gray-900 mb-3">3. Data Security</h2>
              <p>We take reasonable measures to help protect information about you from loss, theft, misuse, unauthorized access, disclosure, alteration, and destruction. Our multi-tenant architecture ensures strict data isolation between organizations.</p>
            </section>

            <section>
              <h2 className="text-[18px] font-bold text-gray-900 mb-3">4. Contact Us</h2>
              <p>If you have any questions about this Privacy Policy, please contact us via our Help Center or Contact page.</p>
            </section>
          </div>
        </div>
      </main>
    </div>
  );
}
