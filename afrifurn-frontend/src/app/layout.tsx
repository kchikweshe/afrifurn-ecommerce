import React from 'react';
import { DataProvider } from '@/data/data.provider';
import { Metadata } from 'next';
import { Inter, Playfair_Display } from "next/font/google"

import '@/app/globals.css'

export const metadata: Metadata = {
  title: 'Afri Furn',
  description: 'Web site created with Next.js for African furniture.',
};
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
      <body className="min-h-screen bg-background font-sans antialiased">
        <DataProvider>
          {children}
        </DataProvider>
      </body>
    </html>
  );
}