'use client'
import { DataProvider } from '@/data/data.provider';
import { Inter, Madimi_One, Playfair_Display } from "next/font/google";
import React, { Suspense, useEffect } from 'react';
import { toast, Toaster } from 'sonner'; // or 'react-hot-toast'

import '@/app/globals.css';
import Header from '@/components/ui/header/header';
import { CartProvider } from '@/context/cart/provider';
import { logoUrl } from '@/data/logo';
import { AuthProvider } from '@/ui/auth-provider';
import LoadingState from './room/[name]/LoadingState';
import Footer from '@/components/ui/footer';
import Breadcrumbs from '@/components/ui/breadcrumbs';

const inter = Inter({
  subsets: ['latin'],
  display: 'swap',
  variable: '--font-sans',
})

const playfair = Playfair_Display({
  subsets: ['latin'],
  display: 'swap',
  variable: '--font-heading',
})

const madimi = Madimi_One({
  weight: '400',
  subsets: ['latin'],
  variable: '--font-madimi',
})

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
          <Breadcrumbs />


          <main className='bg-slate-50'>
            {children}
          </main>

          <Footer />
          <Toaster />
        </CartProvider>
      </DataProvider>
    </AuthProvider>



  );
}