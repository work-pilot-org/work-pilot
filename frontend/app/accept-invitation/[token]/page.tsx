"use client";

import { useEffect, useState } from "react";
import { useParams, useRouter } from "next/navigation";
import { invitationRepository } from "@/repositories/invitationRepository";
import { InvitationValidateResponse } from "@/types/invitation";
import { useAuthStore } from "@/store/authStore";
import { Button } from "@/components/ui/Button";
import { Input } from "@/components/ui/Input";
import { Label } from "@/components/ui/Label";
import { LoadingState } from "@/components/common/LoadingState";
import toast from "react-hot-toast";

export default function AcceptInvitationPage() {
  const { token } = useParams<{ token: string }>();
  const router = useRouter();
  const { isAuthenticated, user, logout, isInitialized } = useAuthStore();

  const [validation, setValidation] = useState<InvitationValidateResponse | null>(null);
  const [isValidating, setIsValidating] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Form State
  const [fullName, setFullName] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);

  useEffect(() => {
    // Wait for auth initialization before validating to avoid redirect races
    if (!isInitialized) return;

    const validateToken = async () => {
      try {
        setIsValidating(true);
        const data = await invitationRepository.validateInvitation(token);
        setValidation(data);

        if (!data.valid) {
          setError(data.revoked ? "This invitation has been revoked." : "This invitation is invalid or has expired.");
          return;
        }

        // Logic for existing user
        if (data.user_exists) {
          if (!isAuthenticated) {
            toast("Please log in to accept this invitation.");
            router.push(`/login?returnUrl=/accept-invitation/${token}`);
          }
        }
      } catch (err: any) {
        setError(err.message || "Failed to validate invitation token.");
      } finally {
        setIsValidating(false);
      }
    };

    validateToken();
  }, [token, isAuthenticated, router, isInitialized]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!validation) return;

    if (!validation.user_exists) {
      if (password !== confirmPassword) {
        toast.error("Passwords do not match.");
        return;
      }
      if (password.length < 8) {
        toast.error("Password must be at least 8 characters.");
        return;
      }
    }

    try {
      setIsSubmitting(true);
      await invitationRepository.acceptInvitation({
        token,
        full_name: fullName,
        password: !validation.user_exists ? password : undefined,
        confirm_password: !validation.user_exists ? confirmPassword : undefined,
      });

      toast.success("Invitation accepted successfully!");
      if (validation.user_exists && isAuthenticated) {
        // Force refresh or redirect to dashboard
        router.push("/dashboard");
      } else {
        router.push("/login?message=Account created. Please log in.");
      }
    } catch (err: any) {
      toast.error(err.message || "Failed to accept invitation.");
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleLogout = async () => {
    await logout();
    window.location.reload();
  };

  if (!isInitialized || isValidating) {
    return <LoadingState message="Validating invitation..." className="min-h-screen flex items-center justify-center" />;
  }

  if (error || !validation || !validation.valid) {
    return (
      <div className="min-h-screen flex flex-col items-center justify-center bg-gray-50 py-12 sm:px-6 lg:px-8">
        <div className="sm:mx-auto sm:w-full sm:max-w-md">
          <div className="bg-white py-8 px-4 shadow sm:rounded-lg sm:px-10 text-center space-y-4">
            <h2 className="text-2xl font-bold text-red-600">Invalid Invitation</h2>
            <p className="text-gray-600">{error || "This invitation is invalid or has expired."}</p>
            <Button onClick={() => router.push("/")} className="w-full">
              Return to Home
            </Button>
          </div>
        </div>
      </div>
    );
  }

  // Handle Mismatched Authenticated User
  if (validation.user_exists && isAuthenticated && user?.email !== validation.email) {
    return (
      <div className="min-h-screen flex flex-col items-center justify-center bg-gray-50 py-12 sm:px-6 lg:px-8">
        <div className="sm:mx-auto sm:w-full sm:max-w-md">
          <div className="bg-white py-8 px-4 shadow sm:rounded-lg sm:px-10 text-center space-y-4">
            <h2 className="text-2xl font-bold text-gray-900">Account Mismatch</h2>
            <p className="text-gray-600">
              You are currently logged in as <strong>{user?.email}</strong>, but this invitation is for <strong>{validation.email}</strong>.
            </p>
            <p className="text-sm text-gray-500">Please sign out and sign back in with the invited account.</p>
            <Button onClick={handleLogout} className="w-full" variant="outline">
              Sign Out
            </Button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gray-50 py-12 sm:px-6 lg:px-8">
      <div className="sm:mx-auto sm:w-full sm:max-w-md text-center mb-6">
        <h2 className="text-3xl font-bold tracking-tight text-gray-900">
          Join {validation.company_name || "the Team"}
        </h2>
        <p className="mt-2 text-sm text-gray-600">
          You have been invited as a {validation.role?.replace("_", " ")}.
        </p>
      </div>

      <div className="sm:mx-auto sm:w-full sm:max-w-md">
        <div className="bg-white py-8 px-4 shadow sm:rounded-lg sm:px-10">
          <form onSubmit={handleSubmit} className="space-y-6">
            <div>
              <Label htmlFor="email">Email</Label>
              <Input
                id="email"
                type="email"
                value={validation.email || ""}
                disabled
                className="bg-gray-50"
              />
            </div>

            {!validation.user_exists ? (
              <>
                <div>
                  <Label htmlFor="fullName">Full Name</Label>
                  <Input
                    id="fullName"
                    type="text"
                    required
                    value={fullName}
                    onChange={(e) => setFullName(e.target.value)}
                    placeholder="John Doe"
                  />
                </div>

                <div>
                  <Label htmlFor="password">Password</Label>
                  <Input
                    id="password"
                    type="password"
                    required
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                  />
                </div>

                <div>
                  <Label htmlFor="confirmPassword">Confirm Password</Label>
                  <Input
                    id="confirmPassword"
                    type="password"
                    required
                    value={confirmPassword}
                    onChange={(e) => setConfirmPassword(e.target.value)}
                  />
                </div>
              </>
            ) : (
              <div className="rounded-md bg-blue-50 p-4 mb-4">
                <div className="flex">
                  <div className="ml-3">
                    <h3 className="text-sm font-medium text-blue-800">Account already exists</h3>
                    <div className="mt-2 text-sm text-blue-700">
                      <p>You can accept this invitation immediately since you are logged in.</p>
                    </div>
                  </div>
                </div>
              </div>
            )}

            <Button type="submit" className="w-full" disabled={isSubmitting}>
              {isSubmitting ? "Accepting..." : "Accept Invitation"}
            </Button>
          </form>
        </div>
      </div>
    </div>
  );
}
