"use client";

import { useState } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import * as z from "zod";
import { ShieldCheck, Loader2, Key } from "lucide-react";
import { mfaVerifyUseCase } from "@/use-cases/auth/mfaVerify";
import { useRouter } from "next/navigation";
import { getTenantDomainUrl } from "@/lib/auth";

const mfaVerifySchema = z.object({
  code: z.string().length(6, "Code must be exactly 6 digits").regex(/^\d+$/, "Code must be numeric"),
});

type MFAVerifyFormData = z.infer<typeof mfaVerifySchema>;

interface MFAVerificationFormProps {
  mfaToken: string;
}

export default function MFAVerificationForm({ mfaToken }: MFAVerificationFormProps) {
  const router = useRouter();
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [successMsg, setSuccessMsg] = useState<string | null>(null);

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

  const onSubmit = async (data: MFAVerifyFormData) => {
    if (submitting) return;
    if (!mfaToken) {
      setError("MFA session token is missing. Please restart the login process.");
      return;
    }

    setSubmitting(true);
    setError(null);
    setSuccessMsg(null);

    const res = await mfaVerifyUseCase(data.code, mfaToken);
    if (res.success && res.data) {
      setSuccessMsg("Verification successful! Logging you in...");
      const result = res.data;
      
      setTimeout(() => {
        if (result.user && result.user.domain) {
          let url = getTenantDomainUrl(result.user.domain, "/");
          if (result.ssoToken) {
            url += `?sso_token=${result.ssoToken}`;
          }
          window.location.href = url;
        } else {
          router.push("/");
        }
      }, 1500);
    } else {
      setError(res.error || "Invalid code. Please try again.");
      setSubmitting(false);
    }
  };

  if (!mfaToken) {
    return (
      <div className="bg-red-50 text-red-700 p-4 rounded-xl text-sm font-medium text-center border border-red-100">
        MFA session token is missing. Please return to the login page and try again.
      </div>
    );
  }

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-5">
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

      {!successMsg && (
        <>
          <div className="space-y-2">
            <label className="block text-[13px] font-medium text-gray-700">6-Digit Verification Code</label>
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
            {submitting ? <Loader2 className="w-5 h-5 animate-spin" /> : "Verify & Continue"}
          </button>
        </>
      )}
    </form>
  );
}
