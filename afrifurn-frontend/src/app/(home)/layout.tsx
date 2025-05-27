'use client'
import { DataProvider } from '@/data/data.provider';
import { Inter, Madimi_One, Playfair_Display } from "next/font/google";
import React, { Suspense } from 'react';

import '@/app/globals.css';
import Header from '@/components/ui/header/header';
import { Toaster } from '@/components/ui/toaster';
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
  return (
    <AuthProvider>
       <DataProvider>
      
      <CartProvider>
        <Header logoUrl={logoUrl} />
        <Breadcrumbs />
  
  <main >
    {children}
  </main>
  <Footer/>
  
      </CartProvider>
    </DataProvider>
    </AuthProvider>
   
  );
}