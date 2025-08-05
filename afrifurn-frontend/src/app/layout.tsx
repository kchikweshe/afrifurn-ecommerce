import React from 'react';
import { Metadata } from 'next';
import { Inter, Madimi_One, Playfair_Display } from "next/font/google"

import '@/app/globals.css'
import { Toaster } from '@/components/ui/toaster';

export const metadata: Metadata = {
  title: "Afri Furn | Premium Furniture in Zimbabwe",
  icons: [{
    url: './favicon.ico',
  }],
  description:
    "Handcrafted furniture for living room, bedroom, office and home office. Quality craftsmanship from Zimbabwe.",
}
const inter = Inter({
  subsets: ['latin'],

})

const playfair = Playfair_Display({
  subsets: ['latin'],
  weight:"400",

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
    <html lang="en" >


      <body className={`${inter.className}  bg-[#fffffff6]  text-gray-800  text-base`}>
        {children}
        <Toaster />
      </body>



    </html>
  );
}