import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";

export function middleware(request: NextRequest) {
  const url = request.nextUrl;
  
  // Get host header (may include port), e.g. apple.localhost:3000
  const host = request.headers.get("host") || "";
  const [hostnameRaw, ...portParts] = host.split(":");
  const hostname = (hostnameRaw || "").toLowerCase();
  const port = portParts.length > 0 ? `:${portParts.join(":")}` : "";
  
  // Extract the subdomain and base domain
  let subdomain = "";
  let baseDomain = host;
  
  if (hostname === "localhost" || hostname.endsWith(".localhost")) {
    if (hostname !== "localhost") {
      subdomain = hostname.slice(0, -".".concat("localhost").length);
    }
    baseDomain = `localhost${port}`; // e.g. localhost:3000
  } else if (hostname === "workpilot.com" || hostname.endsWith(".workpilot.com")) {
    if (hostname !== "workpilot.com") {
      subdomain = hostname.slice(0, -".".concat("workpilot.com").length);
    }
    baseDomain = `workpilot.com${port}`;
  }

  const isLogout = url.searchParams.get("logout") === "true";
  if (isLogout) {
    // Keep the logout param and redirect to login URL so AuthProvider skips silent refresh
    const cleanUrl = new URL("/login?logout=true", request.url);
    const response = NextResponse.redirect(cleanUrl);
    // Must match exact attributes used when setting the cookie:
    // secure=true, samesite="none", httpOnly=true, path="/"
    response.cookies.set("refresh_token", "", {
      maxAge: 0,
      path: "/",
      httpOnly: true,
      secure: true,
      sameSite: "none",
    });
    return response;
  }

  const isAuthPage = url.pathname === '/login' || url.pathname === '/register';

  // Force auth pages to the root domain
  if (isAuthPage && subdomain && subdomain !== "www") {
    const proto = request.headers.get("x-forwarded-proto") || (host.includes("localhost") ? "http" : "https");
    const targetUrl = new URL(url.pathname + url.search, `${proto}://${baseDomain}`);
    return new NextResponse(
      `<html><head><meta http-equiv="refresh" content="0;url=${targetUrl.toString()}" /></head><body></body></html>`,
      { headers: { "content-type": "text/html" } }
    );
  }

  const hasRefreshToken = request.cookies.has("refresh_token");
  const hasSsoToken = url.searchParams.has("sso_token");
  const isProtectedRoute = url.pathname.startsWith('/dashboard') || url.pathname.startsWith('/mfa');

  if (isProtectedRoute && !hasRefreshToken && !hasSsoToken) {
    const proto = request.headers.get("x-forwarded-proto") || (host.includes("localhost") ? "http" : "https");
    const targetUrl = new URL('/login', `${proto}://${baseDomain}`);
    return new NextResponse(
      `<html><head><meta http-equiv="refresh" content="0;url=${targetUrl.toString()}" /></head><body></body></html>`,
      { headers: { "content-type": "text/html" } }
    );
  }

  // If visiting the root on a tenant subdomain without auth, redirect to login
  if (subdomain && subdomain !== "www" && url.pathname === "/" && !hasRefreshToken && !hasSsoToken) {
    const proto = request.headers.get("x-forwarded-proto") || (host.includes("localhost") ? "http" : "https");
    const targetUrl = new URL('/login', `${proto}://${baseDomain}`);
    return new NextResponse(
      `<html><head><meta http-equiv="refresh" content="0;url=${targetUrl.toString()}" /></head><body></body></html>`,
      { headers: { "content-type": "text/html" } }
    );
  }

  // Rewrite logic was removed because Next.js app router handles routes globally 
  // and we use page-level logic (and useAuthStore) for tenant context.

  return NextResponse.next();
}

export const config = {
  matcher: [
    '/((?!api|_next/static|_next/image|favicon.ico).*)',
  ],
};
