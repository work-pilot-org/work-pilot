import { NextRequest, NextResponse } from "next/server";

// We must use the internal Docker network URL, not localhost, because this runs on the Next.js server inside a container.
let AUTH_SERVICE_URL = process.env.INTERNAL_AUTH_SERVICE_URL || process.env.NEXT_PUBLIC_AUTH_SERVICE_URL || "http://auth-service:8000";

// If running in Docker, NEXT_PUBLIC_AUTH_SERVICE_URL might be http://localhost:8001 for the browser,
// but the server needs to hit the container name.
if (AUTH_SERVICE_URL.includes("localhost:8001")) {
  AUTH_SERVICE_URL = AUTH_SERVICE_URL.replace("localhost:8001", "auth-service:8000");
} else if (AUTH_SERVICE_URL.includes("localhost:8000")) {
  // Just in case it's set to localhost:8000
  AUTH_SERVICE_URL = AUTH_SERVICE_URL.replace("localhost:8000", "auth-service:8000");
}

async function handleRequest(request: NextRequest) {
  try {
    // Extract the path after /api/auth/
    const pathName = request.nextUrl.pathname;
    const path = pathName.replace(/^\/api\/auth\/?/, "");
    
    const targetUrl = `${AUTH_SERVICE_URL}/auth/${path}${request.nextUrl.search}`;

    const headers = new Headers(request.headers);
    headers.delete("host");

    const response = await fetch(targetUrl, {
      method: request.method,
      headers,
      body: request.method !== "GET" && request.method !== "HEAD" ? await request.arrayBuffer() : undefined,
      redirect: "manual",
    });

    const responseHeaders = new Headers(response.headers);
    
    // Some headers like content-encoding might cause issues if passed directly through Next.js
    responseHeaders.delete("content-encoding");

    return new NextResponse(response.body, {
      status: response.status,
      headers: responseHeaders,
    });
  } catch (error) {
    console.error("Auth proxy error:", error);
    return new NextResponse(JSON.stringify({ detail: "Internal Proxy Error" }), { 
      status: 500,
      headers: { "Content-Type": "application/json" }
    });
  }
}

export const GET = handleRequest;
export const POST = handleRequest;
export const PUT = handleRequest;
export const PATCH = handleRequest;
export const DELETE = handleRequest;
export const OPTIONS = handleRequest;
