import React from 'react';
import { Metadata } from 'next';
import { Inter, Playfair_Display } from "next/font/google"

import '@/app/globals.css'
import { Toaster } from '@/components/ui/toaster';

export const metadata: Metadata = {
  title: "Afri Furn | Premium Furniture in Zimbabwe",
  description:
    "Handcrafted furniture for living room, bedroom, office and home office. Quality craftsmanship from Zimbabwe.",
}
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

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" className={`${inter.variable} ${playfair.variable}`}>


      <body>
        <main>   {children}</main>
     <Toaster />
      </body>
    


    </html>
  );
}