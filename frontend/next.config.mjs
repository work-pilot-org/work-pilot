/** @type {import('next').NextConfig} */
const nextConfig = {
  allowedDevOrigins: [
    "localhost",
    "*.localhost",
    "*.workpilot.com.localhost",
    "gmail.workpilot.com.localhost",
    "apple.localhost",
    "account.localhost",
    "next.localhost"
  ],
  output: "standalone",
};

export default nextConfig;
