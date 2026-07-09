"use client";

import { useEffect } from "react";
import { useAuthStore } from "@/store/authStore";
import { authRepository } from "@/repositories/authRepository";
import { getBaseDomainUrl, getTenantDomainUrl, isSubdomain } from "@/lib/auth";

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
        
        // If authenticated but on public domain, redirect to tenant domain
        if (!isSubdomain() && response.user?.domain) {
          let targetUrl = getTenantDomainUrl(response.user.domain);
          // Append the sso_token that we now get from the refresh call
          if (response.ssoToken) {
            targetUrl += `?sso_token=${response.ssoToken}`;
          }
          window.location.href = targetUrl;
          return; // Stop execution
        }
      } catch (error) {
        // Normal if they don't have a cookie or it's expired
        console.debug("Silent refresh failed or no cookie present.");
        
        // If NOT authenticated but on a subdomain, redirect to public login
        if (isSubdomain()) {
          window.location.href = getBaseDomainUrl("/login");
          return; // Stop execution
        }
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
