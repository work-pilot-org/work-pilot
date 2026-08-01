"use client";

import { useState, useEffect } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import * as z from "zod";
import { Eye, EyeOff, ArrowLeft } from "lucide-react";
import { executeLogin } from "@/use-cases/auth/login";
import { executeMfaLogin } from "@/use-cases/auth/mfa";
import { useAuthStore } from "@/store/authStore";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { getTenantDomainUrl } from "@/lib/auth";
import { Button } from "@/components/ui/Button";
import { Input } from "@/components/ui/Input";
import { Label } from "@/components/ui/Label";

const loginSchema = z.object({
  email: z.string().email("Invalid email address").optional().or(z.literal("")),
  password: z.string().optional().or(z.literal("")),
  totpCode: z.string().optional().or(z.literal("")),
});

type LoginFormData = z.infer<typeof loginSchema>;

export const LoginForm = () => {
  const [showPassword, setShowPassword] = useState(false);
  const [preAuthToken, setPreAuthToken] = useState<string | null>(null);
  const router = useRouter();
  const { isLoading, error, isAuthenticated, isInitialized } = useAuthStore();

  useEffect(() => {
    if (isInitialized && isAuthenticated) {
      router.replace("/dashboard");
    }
  }, [isInitialized, isAuthenticated, router]);

  const {
    register,
    handleSubmit,
    setValue,
    formState: { errors },
  } = useForm<LoginFormData>({
    resolver: zodResolver(loginSchema),
    defaultValues: { email: "", password: "", totpCode: "" },
  });

  const onSubmit = async (data: LoginFormData) => {
    try {
      if (preAuthToken) {
        if (!data.totpCode) return;
        const result = await executeMfaLogin({ preauth_token: preAuthToken, code: data.totpCode });
        handleLoginSuccess(result);
      } else {
        if (!data.email || !data.password) return;
        const result = await executeLogin({ email: data.email, password: data.password });
        
        if ("mfa_required" in result && result.mfa_required) {
          setPreAuthToken(result.preauth_token);
          return;
        }
        
        handleLoginSuccess(result as any);
      }
    } catch (err) {
      console.error("Login failed", err);
    }
  };

  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const handleLoginSuccess = (result: any) => {
    if (result.user.domain) {
      let url = getTenantDomainUrl(result.user.domain, "/dashboard");
      if (result.ssoToken) {
        url += `?sso_token=${result.ssoToken}`;
      }
      window.location.assign(url);
    } else {
      router.push("/dashboard");
    }
  };

  return (
    <form className="space-y-4" onSubmit={handleSubmit(onSubmit)}>
      {!preAuthToken ? (
        <>
          <div className="space-y-2">
            <Label htmlFor="email">Work Email</Label>
            <Input
              id="email"
              type="email"
              placeholder="name@company.com"
              {...register("email")}
              error={!!errors.email}
              required
            />
            {errors.email && <p className="text-destructive text-xs">{errors.email.message}</p>}
          </div>

          <div className="space-y-2">
            <div className="flex items-center justify-between">
              <Label htmlFor="password">Password</Label>
              <Link href="/forgot-password" className="text-sm font-medium text-primary hover:underline">
                Forgot password?
              </Link>
            </div>
            <div className="relative">
              <Input
                id="password"
                type={showPassword ? "text" : "password"}
                {...register("password")}
                error={!!errors.password}
                className="pr-10"
                required
              />
              <button 
                type="button"
                onClick={() => setShowPassword(!showPassword)}
                className="absolute inset-y-0 right-0 pr-3 flex items-center text-muted-foreground hover:text-foreground"
              >
                {showPassword ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
              </button>
            </div>
          </div>
        </>
      ) : (
        <div className="space-y-4">
          <div className="flex items-center gap-2 mb-2">
            <button
              type="button"
              onClick={() => setPreAuthToken(null)}
              className="text-muted-foreground hover:text-foreground p-1 -ml-1 rounded"
              title="Go back"
            >
              <ArrowLeft className="w-4 h-4" />
            </button>
            <p className="text-sm font-medium">Enter your authenticator code</p>
          </div>
          
          <div className="space-y-2">
            <Input
              type="text"
              {...register("totpCode", {
                onChange: (e) => {
                  setValue("totpCode", e.target.value.replace(/\D/g, ''));
                }
              })}
              required
              maxLength={6}
              placeholder="000000"
              className="text-center tracking-[0.2em] font-mono text-lg"
            />
          </div>
        </div>
      )}

      {error && (
        <div className="text-destructive text-sm font-medium mt-2 bg-destructive/10 p-3 rounded-md border border-destructive/20">
          {error}
        </div>
      )}
      
      <Button type="submit" className="w-full mt-4" isLoading={isLoading}>
        Sign in
      </Button>
    </form>
  );
};
