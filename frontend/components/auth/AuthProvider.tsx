"use client";

import { useEffect, useRef } from "react";
import { useRouter } from "next/navigation";
import { useAuthStore } from "@/store/authStore";
import { authRepository } from "@/repositories/authRepository";
import { getBaseDomainUrl, getTenantDomainUrl, isSubdomain } from "@/lib/auth";

/**
 * Routes where session restoration must NOT be attempted automatically.
 *
 * On these paths the user is intentionally unauthenticated (just logged out,
 * registering, or resetting a password). Calling /auth/refresh here would
 * re-authenticate a user who explicitly logged out.
 *
 * On every other route (including "/") the normal refresh flow runs so that
 * already-authenticated users are seamlessly redirected to their tenant dashboard.
 */
const NO_REFRESH_PATHS = new Set([
  "/login",
  "/register",
  "/forgot-password",
  "/reset-password",
]);

export default function AuthProvider({ children }: { children: React.ReactNode }) {
  const { setInitialized, setUser } = useAuthStore();
  const router = useRouter();
  // Prevents the effect from running twice in React 18 Strict Mode dev double-invoke.
  const hasRun = useRef(false);

  useEffect(() => {
    if (hasRun.current) return;
    hasRun.current = true;

    const initializeAuth = async () => {
      const url = new URL(window.location.href);
      const pathname = url.pathname;
      const ssoToken = url.searchParams.get("sso_token");

      // ── PUBLIC ROUTE GATE ────────────────────────────────────────────────────
      // Do NOT call /auth/refresh on auth pages when there is no SSO token.
      // These are pages the user reaches intentionally (after logout, signup, etc.).
      // If there is an SSO token present even on a public path we still need to
      // exchange it (edge case: should not normally occur, but handle gracefully).
      const isNoRefreshPath = NO_REFRESH_PATHS.has(pathname) ||
        Array.from(NO_REFRESH_PATHS).some(p => pathname.startsWith(p + "/"));

      if (isNoRefreshPath && !ssoToken) {
        console.log("[AUTH] Session restore skipped — public route with no SSO token");
        setInitialized(true);
        return;
      }
      // ─────────────────────────────────────────────────────────────────────────

      try {
        if (ssoToken) {
          console.log("[AUTH] SSO exchange");
          try {
            await authRepository.exchangeSsoToken(ssoToken);
            console.log("[AUTH] SSO exchange complete — refresh cookie set");
          } catch (e) {
            // Token was already used (revoked) or has expired.
            // Fall through to /auth/refresh: if the cookie already exists from a
            // prior exchange, the session can still be restored.
            console.warn("[AUTH] SSO exchange rejected (token already used or expired)", e);
          }

          // Remove the SSO token from the URL *after* the async exchange.
          // This ensures the token is cleaned up without triggering a Next.js 
          // App Router navigation (RSC fetch) before the cookie is successfully set.
          const cleanSearch = url.search
            .replace(/[?&]sso_token=[^&]*/g, "")
            .replace(/^&/, "?");
          const cleanPath = pathname + cleanSearch;
          window.history.replaceState(null, "", cleanPath);
          console.log("[AUTH] SSO token removed from URL");
        }

        // Attempt session restoration via the HttpOnly refresh cookie.
        // The backend validates the token, checks the revocation list, rotates
        // it (issues a new cookie), and returns a fresh access token.
        console.log("[AUTH] Refresh requested");
        const response = await authRepository.refreshToken();
        setUser(response.user, response.token);
        console.log("[AUTH] Refresh success — user authenticated as", response.user?.email);

        // If authenticated on the root (public) domain, redirect to the tenant subdomain.
        // The refresh response includes an SSO token for the cross-domain cookie handoff.
        if (!isSubdomain() && response.user?.domain) {
          let targetUrl = getTenantDomainUrl(response.user.domain);
          if (response.ssoToken) {
            targetUrl += `?sso_token=${response.ssoToken}`;
          }
          window.location.href = targetUrl;
          return;
        }
      } catch (error) {
        // /auth/refresh returned 401: no cookie, expired, or token revoked.
        // This is the normal unauthenticated state.
        console.debug("[AUTH] Refresh skipped — no valid session:", error);

        if (isSubdomain()) {
          // On a tenant subdomain with no valid session → send to root login.
          console.log("[AUTH] Redirecting unauthenticated user from subdomain to login");
          window.location.href = getBaseDomainUrl("/login");
          return;
        }
      } finally {
        setInitialized(true);
      }
    };

    initializeAuth();

    // Listen for logout events from other tabs (BroadcastChannel multi-tab sync).
    const channel = new BroadcastChannel("auth_channel");
    channel.onmessage = (event) => {
      if (event.data === "logout") {
        console.log("[AUTH] Logout broadcast received — clearing state");
        useAuthStore.setState({ user: null, token: null, isAuthenticated: false });
        window.location.href = getBaseDomainUrl("/login");
      }
    };

    return () => channel.close();
  }, []); // eslint-disable-line react-hooks/exhaustive-deps
  // Intentionally empty: runs once on mount. Navigation guards are handled by
  // middleware (server-side) and DashboardLayout (client-side isAuthenticated check).

  return <>{children}</>;
}
