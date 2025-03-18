/** @type {import('next').NextConfig} */
const nextConfig = {
  images: {
    remotePatterns: [
      {
        protocol: 'http',
        hostname: process.env.NEXT_HOST_IP || 'api-gateway',
        port: '8090',
        pathname: '/static/**',
      },
      {
        protocol: 'http',
        hostname: process.env.NEXT_HOST_IP,
        port: '8000',
        pathname: '/**',
      },
      {
        protocol: 'http',
        hostname: process.env.NEXT_HOST_IP || 'api-gateway',
        port: '3000',
        pathname: '/**',
      },
      {
        protocol: 'http',
        hostname: process.env.NEXT_HOST_IP || 'localhost',
        port: '3000',
        pathname: '/**',
      },
    ],
  },
  output: "standalone",

};

module.exports = nextConfig;