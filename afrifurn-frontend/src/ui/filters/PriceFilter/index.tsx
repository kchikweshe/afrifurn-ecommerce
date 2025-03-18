import React, { useState, useEffect } from 'react';

const PriceFilter = ({ onFilterChange }: { onFilterChange: Function }) => {
  const [startPrice, setStartPrice] = useState<number | ''>(0);
  const [endPrice, setEndPrice] = useState<number | ''>(2000);

  useEffect(() => {
    const timer = setTimeout(() => {
      if (startPrice !== '' && endPrice !== '') {
        onFilterChange(startPrice, endPrice);
      }
    }, 500);

    return () => clearTimeout(timer);
  }, [startPrice, endPrice, onFilterChange]);

  const handlePriceChange = (setter: React.Dispatch<React.SetStateAction<number | ''>>) => (event: React.ChangeEvent<HTMLInputElement>) => {
    const value = event.target.value;
    setter(value === '' ? '' : Math.max(0, parseInt(value, 10)));
  };

  return (
    <div className="p-2 sm:p-4">
      <h2 className="text-lg sm:text-xl font-semibold mb-2 sm:mb-4">Filter By Price</h2>
      <div className="flex flex-col sm:flex-row space-y-2 sm:space-y-0 sm:space-x-4">
        <input
          type="number"
          value={startPrice}
          onChange={handlePriceChange(setStartPrice)}
          placeholder="Min Price"
          className="w-full px-3 py-2 text-sm border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
        <input
          type="number"
          value={endPrice}
          onChange={handlePriceChange(setEndPrice)}
          placeholder="Max Price"
          className="w-full px-3 py-2 text-sm border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
      </div>
    </div>
  );
};

export default PriceFilter;