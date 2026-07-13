"use client";

import { useEffect, useState } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import * as z from "zod";
import { ShieldCheck, Loader2, Key } from "lucide-react";
import { mfaSetupUseCase } from "@/use-cases/auth/mfaSetup";
import { mfaVerifyUseCase } from "@/use-cases/auth/mfaVerify";
import { useRouter } from "next/navigation";
import { useAuthStore } from "@/store/authStore";

const mfaVerifySchema = z.object({
  code: z.string().length(6, "Code must be exactly 6 digits").regex(/^\d+$/, "Code must be numeric"),
});

type MFAVerifyFormData = z.infer<typeof mfaVerifySchema>;

export default function MFASetupForm() {
  const router = useRouter();
  const [qrCode, setQrCode] = useState<string | null>(null);
  const [otpauthUrl, setOtpauthUrl] = useState<string | null>(null);
  const [loadingSetup, setLoadingSetup] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [successMsg, setSuccessMsg] = useState<string | null>(null);

  const { isInitialized, isAuthenticated } = useAuthStore();

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<MFAVerifyFormData>({
    resolver: zodResolver(mfaVerifySchema),
    defaultValues: {
      code: "",
    },
  });

  useEffect(() => {
    if (!isInitialized) return;

    if (!isAuthenticated) {
      setError("Please log in to configure MFA.");
      setLoadingSetup(false);
      return;
    }

    const fetchSetup = async () => {
      setLoadingSetup(true);
      setError(null);
      const res = await mfaSetupUseCase();
      if (res.success && res.data) {
        setQrCode(res.data.qr_code);
        setOtpauthUrl(res.data.otpauth_url);
      } else {
        setError(res.error || "Failed to load MFA setup configuration.");
      }
      setLoadingSetup(false);
    };
    fetchSetup();
  }, [isInitialized, isAuthenticated]);

  const onSubmit = async (data: MFAVerifyFormData) => {
    if (submitting) return;
    setSubmitting(true);
    setError(null);
    setSuccessMsg(null);

    const res = await mfaVerifyUseCase(data.code);
    if (res.success) {
      setSuccessMsg("MFA enabled successfully! Redirecting...");
      setTimeout(() => {
        router.push("/");
      }, 2000);
    } else {
      setError(res.error || "Invalid code. Please try again.");
      setSubmitting(false);
    }
  };

  if (!isInitialized || loadingSetup) {
    return (
      <div className="flex flex-col items-center justify-center py-10 space-y-4">
        <Loader2 className="w-8 h-8 text-[#36307a] animate-spin" />
        <p className="text-sm text-gray-500 font-medium">Generating secure TOTP secret...</p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {error && (
        <div className="bg-red-50 text-red-700 p-4 rounded-xl text-sm font-medium border border-red-100">
          {error}
        </div>
      )}

      {successMsg && (
        <div className="bg-green-50 text-green-700 p-4 rounded-xl text-sm font-medium border border-green-100">
          {successMsg}
        </div>
      )}

      {!successMsg && qrCode && (
        <div className="flex flex-col items-center space-y-5">
          <div className="bg-white p-4 rounded-2xl shadow-sm border border-gray-100">
            <img
              src={`data:image/png;base64,${qrCode}`}
              alt="MFA QR Code"
              className="w-48 h-48"
            />
          </div>
          <div className="text-center max-w-[320px]">
            <p className="text-[13px] text-gray-500 font-medium">
              Scan this QR code with Google Authenticator or Authy to enroll.
            </p>
            {otpauthUrl && (
              <a
                href={otpauthUrl}
                className="text-[12px] text-[#36307a] hover:underline mt-2 inline-block break-all font-mono"
              >
                Or click to open Authenticator link
              </a>
            )}
          </div>

          <form onSubmit={handleSubmit(onSubmit)} className="w-full space-y-4">
            <div className="space-y-2">
              <label className="block text-[13px] font-medium text-gray-700">Verification Code</label>
              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none">
                  <Key className="h-4 w-4 text-gray-400" />
                </div>
                <input
                  type="text"
                  maxLength={6}
                  placeholder="000000"
                  {...register("code")}
                  className="block w-full pl-10 pr-3.5 py-2.5 border border-gray-200 rounded-lg text-[14px] text-black placeholder:text-gray-300 focus:outline-none focus:ring-2 focus:ring-[#2a2468] focus:border-transparent transition-all bg-white tracking-widest text-center font-bold"
                />
              </div>
              {errors.code && (
                <p className="text-red-500 text-xs font-medium mt-1">{errors.code.message}</p>
              )}
            </div>

            <button
              type="submit"
              disabled={submitting}
              className="w-full bg-[#36307a] hover:bg-[#2a2468] text-white text-[14px] font-bold py-3.5 rounded-xl shadow-sm transition-all disabled:opacity-70 flex items-center justify-center cursor-pointer"
            >
              {submitting ? <Loader2 className="w-5 h-5 animate-spin" /> : "Verify & Enable MFA"}
            </button>
          </form>
        </div>
      )}
    </div>
  );
}
