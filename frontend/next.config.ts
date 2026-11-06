import type { NextConfig } from "next";

/** Hosts we are allowed to load optimised images from. */
const remoteImageHosts: string[] = [];

if (process.env.SUPABASE_PROJECT_REF) {
  remoteImageHosts.push(`${process.env.SUPABASE_PROJECT_REF}.supabase.co`);
}
if (process.env.NEXT_PUBLIC_API_URL) {
  try {
    remoteImageHosts.push(new URL(process.env.NEXT_PUBLIC_API_URL).hostname);
  } catch {
    /* ignore a malformed value and fall through to the defaults */
  }
}

const nextConfig: NextConfig = {
  cacheComponents: true,
  partialPrefetching: true,

  // Render serves behind a proxy; this keeps the response small and correct.
  poweredByHeader: false,
  compress: true,

  images: {
    remotePatterns: [
      ...remoteImageHosts.map((hostname) => ({
        protocol: "https" as const,
        hostname,
      })),
      // Supabase Storage for any project ref, so previews work too.
      { protocol: "https" as const, hostname: "*.supabase.co" },
      // Local Django during development.
      { protocol: "http" as const, hostname: "127.0.0.1", port: "8000" },
      { protocol: "http" as const, hostname: "localhost", port: "8000" },
    ],
    formats: ["image/avif", "image/webp"],
    deviceSizes: [360, 420, 640, 768, 1024, 1280, 1536, 1920],
  },

  turbopack: {
    rules: {
      "*.css": {
        loaders: ["@tailwindcss/turbopack"],
        as: "*.css",
      },
    },
  },

  async headers() {
    return [
      {
        source: "/:path*",
        headers: [
          { key: "X-Content-Type-Options", value: "nosniff" },
          { key: "X-Frame-Options", value: "SAMEORIGIN" },
          {
            key: "Referrer-Policy",
            value: "strict-origin-when-cross-origin",
          },
          {
            key: "Permissions-Policy",
            value: "camera=(), microphone=(), geolocation=()",
          },
        ],
      },
    ];
  },
};

export default nextConfig;
