import React, { useState } from 'react';
import { Search } from 'lucide-react';

export const CustomSearchBar = () => {
  const [isFocused, setIsFocused] = useState(false);

  return (
    <div className={`relative flex items-center w-full max-w-screen-md mx-auto transition-all duration-300 ease-in-out ${isFocused ? 'bg-white shadow-lg' : 'bg-gray-100'} rounded-full`}>
      <Search className={`absolute left-3 w-5 h-5 transition-colors duration-300 ${isFocused ? 'text-blue-500' : 'text-gray-400'}`} />
      <input
        type="text"
        placeholder="Search..."
        className="w-full py-2 pl-10 pr-4 text-gray-700 bg-transparent rounded-full focus:outline-none"
        onFocus={() => setIsFocused(true)}
        onBlur={() => setIsFocused(false)}
      />
    </div>
  );
};

