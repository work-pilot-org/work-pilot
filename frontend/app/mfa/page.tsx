"use client";

import { useEffect, useState } from "react";
import { useAuthStore } from "@/store/authStore";
import { useRouter } from "next/navigation";
import { Shield, ShieldAlert, Loader2, ArrowLeft, CheckCircle2 } from "lucide-react";
import { QRCodeSVG } from "qrcode.react";
import { executeSetupMfa, executeEnableMfa, executeDisableMfa } from "@/use-cases/auth/mfa";
import Link from "next/link";

export default function MFAPage() {
  const { user, isAuthenticated, isInitialized } = useAuthStore();
  const router = useRouter();

  const [isLoading, setIsLoading] = useState(false);
  const [setupData, setSetupData] = useState<{ secret: string; provisioning_uri: string } | null>(null);
  const [code, setCode] = useState("");
  const [password, setPassword] = useState(""); // Needed for disabling MFA
  const [error, setError] = useState<string | null>(null);
  const [successMsg, setSuccessMsg] = useState<string | null>(null);
  
  // We track local state for MFA enabled status, initialized from the backend user context
  const [isMfaEnabledLocal, setIsMfaEnabledLocal] = useState(user?.isMfaEnabled || false);

  useEffect(() => {
    if (user && isMfaEnabledLocal !== user.isMfaEnabled) {
      setIsMfaEnabledLocal(user.isMfaEnabled || false);
    }
  }, [user]);

  useEffect(() => {
    if (isInitialized && !isAuthenticated) {
      router.push("/login");
    }
  }, [isInitialized, isAuthenticated, router]);

  if (!isInitialized || !isAuthenticated) return null;

  const handleSetupMfa = async () => {
    try {
      setIsLoading(true);
      setError(null);
      const data = await executeSetupMfa();
      setSetupData(data);
    } catch (err: any) {
      setError(err.message || "Failed to setup MFA");
    } finally {
      setIsLoading(false);
    }
  };

  const handleEnableMfa = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      setIsLoading(true);
      setError(null);
      await executeEnableMfa({ code });
      setIsMfaEnabledLocal(true);
      setSetupData(null);
      setSuccessMsg("MFA successfully enabled!");
      setCode("");
    } catch (err: any) {
      setError(err.message || "Invalid MFA code");
    } finally {
      setIsLoading(false);
    }
  };

  const handleDisableMfa = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      setIsLoading(true);
      setError(null);
      await executeDisableMfa({ password, code });
      setIsMfaEnabledLocal(false);
      setSuccessMsg("MFA successfully disabled!");
      setPassword("");
      setCode("");
    } catch (err: any) {
      setError(err.message || "Failed to disable MFA. Check your password and code.");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col justify-center items-center p-4 font-sans">
      <div className="mb-5 text-center flex flex-col items-center">
        <div className="w-10 h-10 bg-[#2a2468] rounded-xl flex items-center justify-center mb-2 shadow-sm">
          <Shield className="w-5 h-5 text-white" />
        </div>
        <h1 className="text-[24px] font-bold text-[#2a2468] tracking-tight">Security Settings</h1>
      </div>

      <div className="bg-white rounded-[16px] shadow-sm border border-gray-100 p-6 w-full max-w-[450px]">
        <div className="mb-6 flex items-center gap-2">
          <Link href="/" className="text-gray-400 hover:text-gray-700 transition-colors p-1 -ml-1 rounded-md">
            <ArrowLeft className="w-4 h-4" />
          </Link>
          <h2 className="text-[18px] font-semibold text-gray-900">Multi-Factor Authentication</h2>
        </div>

        {error && (
          <div className="mb-4 p-3 bg-red-50 border border-red-100 rounded-lg flex gap-2 items-start text-red-700 text-[13px]">
            <ShieldAlert className="w-4 h-4 mt-0.5 shrink-0" />
            <p>{error}</p>
          </div>
        )}

        {successMsg && (
          <div className="mb-4 p-3 bg-green-50 border border-green-100 rounded-lg flex gap-2 items-start text-green-700 text-[13px]">
            <CheckCircle2 className="w-4 h-4 mt-0.5 shrink-0" />
            <p>{successMsg}</p>
          </div>
        )}

        {isMfaEnabledLocal ? (
          <div className="space-y-4">
            <div className="p-4 bg-green-50 border border-green-100 rounded-xl">
              <div className="flex items-center gap-2 text-green-700 font-medium mb-1">
                <CheckCircle2 className="w-5 h-5" />
                MFA is Active
              </div>
              <p className="text-[13px] text-green-600">
                Your account is protected by multi-factor authentication.
              </p>
            </div>
            
            <form onSubmit={handleDisableMfa} className="space-y-4 mt-6 border-t border-gray-100 pt-6">
              <h3 className="text-[14px] font-semibold text-gray-900">Disable MFA</h3>
              
              <div className="space-y-2">
                <label className="block text-[13px] font-medium text-gray-700">Current Password</label>
                <input
                  type="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  required
                  className="block w-full px-3.5 py-2.5 border border-gray-200 rounded-lg text-[14px] focus:ring-2 focus:ring-[#2a2468]"
                />
              </div>
              <div className="space-y-2">
                <label className="block text-[13px] font-medium text-gray-700">Authenticator Code</label>
                <input
                  type="text"
                  value={code}
                  onChange={(e) => setCode(e.target.value.replace(/\D/g, ''))}
                  required
                  maxLength={6}
                  className="block w-full px-3.5 py-2.5 border border-gray-200 rounded-lg text-[14px] font-mono tracking-widest text-center focus:ring-2 focus:ring-[#2a2468]"
                />
              </div>
              
              <button
                type="submit"
                disabled={isLoading}
                className="w-full bg-red-50 text-red-600 hover:bg-red-100 font-bold text-[14px] py-2.5 rounded-lg transition-colors flex items-center justify-center"
              >
                {isLoading ? <Loader2 className="w-4 h-4 animate-spin" /> : "Disable MFA"}
              </button>
            </form>
          </div>
        ) : !setupData ? (
          <div className="space-y-4">
            <p className="text-[14px] text-gray-600 leading-relaxed">
              Enhance your account security by enabling Multi-Factor Authentication. You will need an authenticator app like Google Authenticator or Authy.
            </p>
            <button
              onClick={handleSetupMfa}
              disabled={isLoading}
              className="w-full bg-[#36307a] hover:bg-[#2a2468] text-white font-bold text-[14px] py-3 rounded-xl transition-colors shadow-sm flex items-center justify-center"
            >
              {isLoading ? <Loader2 className="w-5 h-5 animate-spin" /> : "Setup MFA"}
            </button>
          </div>
        ) : (
          <div className="space-y-6">
            <div className="flex justify-center bg-gray-50 p-4 rounded-xl border border-gray-100">
              <QRCodeSVG value={setupData.provisioning_uri} size={160} />
            </div>
            
            <div className="text-center">
              <p className="text-[13px] text-gray-500 mb-1">Manual Setup Key</p>
              <code className="bg-gray-100 px-3 py-1.5 rounded-lg text-[13px] font-mono text-gray-800 break-all">
                {setupData.secret}
              </code>
            </div>

            <form onSubmit={handleEnableMfa} className="space-y-4">
              <div className="space-y-2">
                <label className="block text-[13px] font-medium text-gray-700">Enter the 6-digit code from your app</label>
                <input
                  type="text"
                  value={code}
                  onChange={(e) => setCode(e.target.value.replace(/\D/g, ''))}
                  required
                  maxLength={6}
                  placeholder="000000"
                  className="block w-full px-3.5 py-3 border border-gray-200 rounded-xl text-[18px] tracking-[0.2em] font-mono text-center focus:ring-2 focus:ring-[#2a2468]"
                />
              </div>
              <button
                type="submit"
                disabled={isLoading || code.length !== 6}
                className="w-full bg-[#36307a] hover:bg-[#2a2468] text-white font-bold text-[14px] py-3 rounded-xl transition-colors shadow-sm flex items-center justify-center disabled:opacity-70"
              >
                {isLoading ? <Loader2 className="w-5 h-5 animate-spin" /> : "Verify & Enable"}
              </button>
            </form>
          </div>
        )}
      </div>
    </div>
  );
}
