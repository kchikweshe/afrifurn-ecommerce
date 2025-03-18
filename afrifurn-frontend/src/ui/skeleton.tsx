// src/app/components/ProductGridSkeleton.js
import React from 'react';

const ProductGridSkeleton = () => {
  return (
    <div className="grid grid-cols-2 lg:grid-cols-3 gap-8">
      {[...Array(6)].map((_, index) => (
        <div key={index} className="animate-pulse p-4 bg-gray-300 rounded-lg">
          <div className="h-40 bg-gray-400 mb-4"></div>
          <div className="h-6 bg-gray-400 mb-2"></div>
          <div className="h-6 bg-gray-400"></div>
        </div>
      ))}
    </div>
  );
};

export default ProductGridSkeleton;
