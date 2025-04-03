'use client'
import React, { useState } from 'react';

const NameSearchBar = ({ onSearch }) => {
  const [searchTerm, setSearchTerm] = useState('');

  const handleInputChange = (event) => {
    const value = event.target.value;
    setSearchTerm(value);
    onSearch(value); // Trigger the search action
  };

  return (
    <div className="p-4">
      <label htmlFor="search-bar" className="block text-sm font-medium text-gray-700">Search by Name</label>
      <div className="mt-1">
        <input
          type="text"
          name="search-bar"
          id="search-bar"
          value={searchTerm}
          onChange={handleInputChange}
          placeholder="Type a name to search..."
          className="shadow-sm focus:ring-indigo-500 focus:border-indigo-500 block w-full sm:text-sm border-gray-300 rounded-md"
        />
      </div>
    </div>
  );
};

export default NameSearchBar;
