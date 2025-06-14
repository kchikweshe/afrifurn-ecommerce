/** @type {import('next').NextConfig} */
const nextConfig = {
  images: {
    domains: [
      'afri-furn.co.zw', // <-- add your image domain here (no protocol, no path)
      // add more domains as needed
    ],
    remotePatterns: [
      {
        protocol: 'http',
        hostname: process.env.NEXT_PUBLIC_URL || 'afri-furn.co.zw',
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
        hostname: 'localhost',
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