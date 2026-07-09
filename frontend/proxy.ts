import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";

export function proxy(request: NextRequest) {
  const url = request.nextUrl;
  
  // Get hostname of request (e.g. apple.localhost:3000 -> apple.localhost)
  const hostname = request.headers.get("host") || "";
  
  // Extract the subdomain (e.g. apple)
  let subdomain = "";
  if (hostname.includes(".localhost")) {
    subdomain = hostname.split(".localhost")[0];
  } else if (hostname.includes(".workpilot.com")) {
    subdomain = hostname.split(".workpilot.com")[0];
  }

  // Check if the user is logged in (has the refresh token cookie)
  const hasToken = request.cookies.has("refresh_token");

  // If user is already logged in and tries to access login/register, redirect them to home
  if (hasToken && (url.pathname === '/login' || url.pathname === '/register')) {
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
