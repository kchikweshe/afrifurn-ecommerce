/** @type {import('next').NextConfig} */
const nextConfig = {
  images: {
    remotePatterns: [
      {
        protocol: 'http',
        hostname: process.env.NEXT_PUBLIC_URL || 'api-gateway',
        port: '8000',
        pathname: '/static/**',
      },
      {
        protocol: 'http',
        hostname: process.env.NEXT_PUBLIC_URL,
        port: '8000',
        pathname: '/**',
      },
      {
        protocol: 'http',
        hostname: process.env.NEXT_PUBLIC_URL || 'api-gateway',
        port: '3000',
        pathname: '/**',
      },
      {
        protocol: 'http',
        hostname: process.env.NEXT_PUBLIC_URL || 'localhost',
        port: '3000',
        pathname: '/**',
      },
    ],
  },
  output: "standalone",

};

module.exports = nextConfig;