'use client';
import Image from "next/image";

export const HeroSection = ({ primaryImage }) => (
  <div className="relative w-full">
    <Image
      className="h-[100vh] sm:h-[25vh] lg:h-[30vh] w-full object-cover"
      width={800}
      height={800}
      src={primaryImage}
      alt="Best Room Decor Items"
      loading="lazy" />
    <div className="absolute inset-0 bg-gradient-to-r from-black/50 to-transparent"></div>
    <div className="absolute left-[5%] right-[5%] lg:right-auto lg:w-[50%] lg:w-[36%] bottom-0 top-0 my-auto flex h-max flex-col items-start justify-center">
      <h1 className="tracking-[-0.50px] text-sm sm:text-base font-semibold text-yellow-100">Best Room Decor Items</h1>
      <h2 className="text-lg sm:text-2xl lg:text-[28px] leading-tight sm:leading-snug lg:leading-normal tracking-[-0.50px] font-raleway font-bold text-white mt-2">
        Our goods have the best quality and materials in the world
      </h2>
      <button className="mt-4 min-w-[120px] sm:min-w-[150px] tracking-[-0.50px] font-poppins font-bold px-4 sm:px-6 flex items-center justify-center text-center cursor-pointer rounded h-[40px] sm:h-[50px] text-base sm:text-lg bg-yellow-100 text-blue-gray-900 transform hover:scale-105 transition-transform duration-200">
        Shop Now
      </button>
    </div>
  </div>
);
