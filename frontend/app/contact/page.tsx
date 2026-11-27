import Link from "next/link";
import { ArrowLeft, Mail, MapPin, Phone } from "lucide-react";

export default function ContactPage() {
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
          <h1 className="text-[32px] font-bold text-gray-900 mb-6 tracking-tight">Contact Us</h1>
          <p className="text-[15px] text-gray-500 mb-8 leading-relaxed">
            Have questions about WorkPilot AI? Our enterprise support team is here to help you get the most out of your workflow management.
          </p>
          
          <div className="space-y-8">
            <div className="flex items-start gap-4">
              <div className="w-10 h-10 bg-[#36307a]/10 rounded-xl flex items-center justify-center shrink-0">
                <Mail className="w-5 h-5 text-[#36307a]" />
              </div>
              <div>
                <h3 className="text-[16px] font-bold text-gray-900 mb-1">Email Support</h3>
                <p className="text-[14px] text-gray-500 mb-2">Our team typically responds within 2 hours during business days.</p>
                <a href="mailto:support@workpilotai.com" className="text-[14px] font-medium text-[#36307a] hover:underline">
                  support@workpilotai.com
                </a>
              </div>
            </div>

            <div className="flex items-start gap-4">
              <div className="w-10 h-10 bg-[#36307a]/10 rounded-xl flex items-center justify-center shrink-0">
                <Phone className="w-5 h-5 text-[#36307a]" />
              </div>
              <div>
                <h3 className="text-[16px] font-bold text-gray-900 mb-1">Sales Inquiries</h3>
                <p className="text-[14px] text-gray-500 mb-2">Looking for a custom enterprise plan? Give our sales team a call.</p>
                <a href="tel:+18005550199" className="text-[14px] font-medium text-[#36307a] hover:underline">
                  +1 (800) 555-0199
                </a>
              </div>
            </div>

            <div className="flex items-start gap-4">
              <div className="w-10 h-10 bg-[#36307a]/10 rounded-xl flex items-center justify-center shrink-0">
                <MapPin className="w-5 h-5 text-[#36307a]" />
              </div>
              <div>
                <h3 className="text-[16px] font-bold text-gray-900 mb-1">Headquarters</h3>
                <p className="text-[14px] text-gray-500">
                  123 Innovation Drive, Suite 500<br />
                  San Francisco, CA 94105<br />
                  United States
                </p>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}
