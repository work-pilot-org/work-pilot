"use client";

import { useEffect } from "react";
import { useAuthStore } from "@/store/authStore";
import { authRepository } from "@/repositories/authRepository";

export default function AuthProvider({ children }: { children: React.ReactNode }) {
  const { setInitialized, setUser, isInitialized } = useAuthStore();

  useEffect(() => {
    const initializeAuth = async () => {
      try {
        const url = new URL(window.location.href);
        const ssoToken = url.searchParams.get("sso_token");
        
        if (ssoToken) {
          // Exchange the SSO token for a secure HttpOnly cookie on this domain
          await authRepository.exchangeSsoToken(ssoToken);
          // Clean the URL
          url.searchParams.delete("sso_token");
          window.history.replaceState({}, document.title, url.pathname + url.search);
        }

        // Silently attempt to refresh the token using the HttpOnly cookie
        const response = await authRepository.refreshToken();
        setUser(response.user, response.token);
      } catch (error) {
        // Normal if they don't have a cookie or it's expired
        console.debug("Silent refresh failed or no cookie present.");
      } finally {
        setInitialized(true);
      }
    };

    initializeAuth();
  }, [setInitialized, setUser]);

  // Optionally, you can return a loading spinner here while `!isInitialized`,
  // but to prevent layout shift or blocking public routes, we just render children.
  // The pages themselves can check `isInitialized` if they need to block rendering.
  return <>{children}</>;
}
