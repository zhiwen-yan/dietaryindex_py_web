import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  output: "standalone",
  reactStrictMode: true,
  poweredByHeader: false,
  allowedDevOrigins: ["192.168.1.10", "100.115.176.48", "192.168.1.*"],
};

export default nextConfig;
