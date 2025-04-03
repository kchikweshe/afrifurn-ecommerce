'use client'
import React from 'react'

const LoadingState = () => (
  <div className="flex flex-col items-center justify-center h-[60vh] space-y-6">
    {/* Animated furniture icon */}
    <div className="relative w-24 h-24">
      <div className="absolute inset-0 animate-pulse">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          className="w-full h-full text-primary"
          strokeWidth="2"
        >
          <path d="M20 10V8a2 2 0 0 0-2-2H6a2 2 0 0 0-2 2v2m16 0v10H4V10m16 0h-6a2 2 0 0 0-2 2v2a2 2 0 0 0 2 2h6M4 10h6a2 2 0 0 1 2 2v2a2 2 0 0 1-2 2H4" />
        </svg>
      </div>
      <div className="absolute inset-0 animate-spin-slow">
        <div className="absolute inset-0 rounded-full border-4 border-primary border-t-transparent"></div>
      </div>
    </div>

    {/* Loading text with shimmer effect */}
    <div className="relative">
      <p className="text-2xl font-semibold text-gray-700">Loading ...</p>
      <div className="absolute inset-0 w-full animate-shimmer bg-gradient-to-r from-transparent via-primary/10 to-transparent"></div>
    </div>

    {/* Loading progress dots */}
    <div className="flex space-x-2">
      {[0, 1, 2].map((i) => (
        <div
          key={i}
          className="w-2 h-2 rounded-full bg-primary animate-bounce"
          style={{ animationDelay: `${i * 0.2}s` }}
        ></div>
      ))}
    </div>
  </div>
)

export default LoadingState