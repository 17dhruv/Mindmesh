/** @type {import('next').NextConfig} */
const nextConfig = {
  experimental: {
    optimizePackageImports: ['lucide-react', '@radix-ui/react-icons']
  },
  images: {
    remotePatterns: [
      {
        protocol: 'https',
        hostname: 'supabase.co',
      },
    ],
    formats: ['image/webp', 'image/avif']
  },
  compiler: {
    removeConsole: process.env.NODE_ENV === 'production'
  },
  poweredByHeader: false,
  compress: true
};

export default nextConfig;
