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
  async rewrites() {
    return [
      {
        source: '/api/analytics/:path*',
        destination: `${process.env.ANALYTICS_INTERNAL_URL || 'http://localhost:8007'}/analytics/:path*`
      }
    ];
  }
};

export default nextConfig;
