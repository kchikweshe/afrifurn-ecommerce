// File: components/AuthLayout.tsx
import React from 'react';
import Image from 'next/image';

interface AuthLayoutProps {
  children: React.ReactNode;
}

const AuthLayout: React.FC<AuthLayoutProps> = ({ children }) => {
  return (
    <div className="flex min-h-screen relative overflow-hidden">
      {/* Background Image */}
      <div className="absolute inset-0 z-0">
        <Image
          src="/living.jpg" // Update this path to your actual image
          alt="Background"
          layout="fill"
          objectFit="cover"
          priority
        />
        {/* Optional overlay for better readability */}
        <div className="absolute inset-0 bg-black bg-opacity-40"></div>
      </div>

      {/* Right side - Form */}
      <div className="w-full flex items-center justify-center rounded-sm relative z-10">
        <div className="bg-slate-500 w-auto h-auto">
          {children}
        </div>
      </div>
    </div>
  );
};

export default AuthLayout;