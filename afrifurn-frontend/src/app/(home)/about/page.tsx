import React from 'react';
import Image from 'next/image';
import Link from 'next/link';

export default function AboutPage() {
  return (
    <div className="container mx-auto px-4 py-12">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-4xl font-bold text-center mb-8">About Afri Furn</h1>
        
        <div className="mb-12 relative h-80 rounded-xl overflow-hidden">
          <Image 
            src="/about-hero.jpg" 
            alt="Afri Furn Team" 
            fill
            className="object-cover"
          />
        </div>
        
        <div className="prose prose-lg max-w-none">
          <h2 className="text-2xl font-semibold mb-4">Our Story</h2>
          <p className="mb-6">
            Founded in 2020, Afri Furn was born from a passion for bringing authentic African-inspired furniture and home décor to homes around the world. What started as a small workshop in Harare has grown into a global brand that celebrates African craftsmanship and design.
          </p>
          
          <h2 className="text-2xl font-semibold mb-4">Our Mission</h2>
          <p className="mb-6">
            At Afri Furn, our mission is to showcase the rich heritage of African design while supporting local artisans and sustainable practices. We believe that beautiful furniture should tell a story, connect cultures, and be created with respect for both people and the planet.
          </p>
          
          <h2 className="text-2xl font-semibold mb-4">Our Artisans</h2>
          <p className="mb-6">
            Every piece in our collection is handcrafted by skilled artisans who bring generations of expertise to their work. We partner directly with craftspeople across Africa, ensuring fair wages and preserving traditional techniques while embracing contemporary design.
          </p>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 my-12">
            <div className="text-center">
              <div className="bg-blue-100 rounded-full w-20 h-20 flex items-center justify-center mx-auto mb-4">
                <svg xmlns="http://www.w3.org/2000/svg" className="h-10 w-10 text-blue-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 12a9 9 0 01-9 9m9-9a9 9 0 00-9-9m9 9H3m9 9a9 9 0 01-9-9m9 9c1.657 0 3-4.03 3-9s-1.343-9-3-9m0 18c-1.657 0-3-4.03-3-9s1.343-9 3-9m-9 9a9 9 0 019-9" />
                </svg>
              </div>
              <h3 className="font-semibold text-xl mb-2">Global Reach</h3>
              <p className="text-gray-600">Shipping to over 50 countries worldwide</p>
            </div>
            
            <div className="text-center">
              <div className="bg-green-100 rounded-full w-20 h-20 flex items-center justify-center mx-auto mb-4">
                <svg xmlns="http://www.w3.org/2000/svg" className="h-10 w-10 text-green-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 12l3-3 3 3 4-4M8 21l4-4 4 4M3 4h18M4 4h16v12a1 1 0 01-1 1H5a1 1 0 01-1-1V4z" />
                </svg>
              </div>
              <h3 className="font-semibold text-xl mb-2">Sustainable</h3>
              <p className="text-gray-600">Eco-friendly materials and practices</p>
            </div>
            
            <div className="text-center">
              <div className="bg-amber-100 rounded-full w-20 h-20 flex items-center justify-center mx-auto mb-4">
                <svg xmlns="http://www.w3.org/2000/svg" className="h-10 w-10 text-amber-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
                </svg>
              </div>
              <h3 className="font-semibold text-xl mb-2">Community</h3>
              <p className="text-gray-600">Supporting over 200 artisans and their families</p>
            </div>
          </div>
          
          <h2 className="text-2xl font-semibold mb-4">Our Commitment to Quality</h2>
          <p className="mb-6">
            Every Afri Furn piece undergoes rigorous quality control to ensure it meets our exacting standards. We use only the finest materials, from sustainably sourced hardwoods to premium textiles, creating furniture that's not just beautiful but built to last.
          </p>
          
          <div className="bg-blue-50 p-8 rounded-xl my-12">
            <h2 className="text-2xl font-semibold mb-4 text-center">Get in Touch</h2>
            <p className="text-center mb-6">
              Have questions or want to learn more about our products and process? We'd love to hear from you!
            </p>
            <div className="text-center">
              <Link href="/contact" className="inline-block bg-blue-600 text-white px-6 py-3 rounded-lg font-medium hover:bg-blue-700 transition-colors">
                Contact Us
              </Link>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
} 