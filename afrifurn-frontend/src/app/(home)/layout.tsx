'use client'
import { DataProvider } from '@/data/data.provider';
import { Inter, Madimi_One, Playfair_Display } from "next/font/google";
import React, { Suspense, useEffect } from 'react';
import { toast, Toaster } from 'sonner'; // or 'react-hot-toast'
import { usePathname } from 'next/navigation';

import '@/app/globals.css';
import Header from '@/components/ui/header/header';
import { CartProvider } from '@/context/cart/provider';
import { logoUrl } from '@/data/logo';
import { AuthProvider } from '@/ui/auth-provider';
import LoadingState from '../../components/ui/LoadingState';
import Footer from '@/components/ui/footer';
import Breadcrumbs from '@/components/ui/breadcrumbs';



export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  useEffect(() => {
    if (typeof window !== 'undefined') {
      if (localStorage.getItem('showRegisterSuccess')) {
        toast.success(localStorage.getItem('showRegisterSuccessMessage'));
        localStorage.removeItem('showRegisterSuccess');
        localStorage.removeItem('showRegisterSuccessMessage');

      }
    }
  }, []);

  return (
    <AuthProvider>
      <DataProvider>

        <CartProvider>



          <Header logoUrl={logoUrl} />
          <div className='bg-gray-50 px-6 text-sm md:text-base'>
            {usePathname() !== '/' && <Breadcrumbs />}
          </div>


          <main className={"mx-6"}>
            {children}
          </main>

          <Footer />
          <Toaster />
        </CartProvider>
      </DataProvider>
    </AuthProvider>



  );
}