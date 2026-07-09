import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";

export function proxy(request: NextRequest) {
  const url = request.nextUrl;
  
  // Get hostname of request (e.g. apple.localhost:3000 -> apple.localhost:3000)
  const host = request.headers.get("host") || "";
  
  // Extract the subdomain and base domain
  let subdomain = "";
  let baseDomain = host;
  
  if (host.includes(".localhost")) {
    const parts = host.split(".localhost");
    subdomain = parts[0];
    baseDomain = `localhost${parts[1]}`; // e.g. localhost:3000
  } else if (host.includes(".workpilot.com")) {
    const parts = host.split(".workpilot.com");
    subdomain = parts[0];
    baseDomain = `workpilot.com${parts[1] || ""}`;
  }

  const isLogout = url.searchParams.get("logout") === "true";
  if (isLogout) {
    const redirectUrl = new URL(url.pathname, request.url);
    const response = NextResponse.redirect(redirectUrl);
    response.cookies.delete("refresh_token");
    return response;
  }

  const isAuthPage = url.pathname === '/login' || url.pathname === '/register';

  // Force auth pages to the root domain
  if (isAuthPage && subdomain && subdomain !== "www") {
    const proto = request.headers.get("x-forwarded-proto") || (host.includes("localhost") ? "http" : "https");
    return NextResponse.redirect(`${proto}://${baseDomain}${url.pathname}${url.search}`);
  }

  // Check if the user is logged in (has the refresh token cookie)
  const hasToken = request.cookies.has("refresh_token");

  // If user is already logged in and tries to access login/register on the main domain, redirect them to home
  if (hasToken && isAuthPage) {
    return NextResponse.redirect(new URL('/', request.url));
  }

  // If it's a specific subdomain (not the main domain), you can rewrite the URL 
  // to a specific Next.js app directory like /app/tenant/[domain]/...
  // if (subdomain && subdomain !== "www") {
  //   return NextResponse.rewrite(new URL(`/tenant/${subdomain}${url.pathname}`, request.url));
  // }

  return NextResponse.next();
}

export const config = {
  matcher: [
    '/((?!api|_next/static|_next/image|favicon.ico).*)',
  ],
};
