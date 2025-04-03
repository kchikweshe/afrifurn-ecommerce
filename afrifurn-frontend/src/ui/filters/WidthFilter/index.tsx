import React, { useState, useEffect } from 'react';

const TvSizeFilter = ({ onFilterChange }: { onFilterChange: Function }) => {
  const [inputSize, setInputSize] = useState<number | ''>('');

  useEffect(() => {
    const timer = setTimeout(() => {
      if (inputSize !== '') {
        const standSize = mapSizeToStand(inputSize);
        onFilterChange(standSize);
      } else {
        onFilterChange(null);
      }
    }, 500);

    return () => clearTimeout(timer);
  }, [inputSize, onFilterChange]);

  const handleSizeChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const value = event.target.value;
    setInputSize(value === '' ? '' : Math.max(0, parseInt(value, 10)));
  };

  const mapSizeToStand = (inches: number): number => {
    if (inches <= 47) return 120;
    if (inches <= 63) return 160;
    return 200;
  };

  return (
    <div className="p-2 sm:p-4">
      <h2 className="text-lg sm:text-xl font-semibold mb-2 sm:mb-4">Enter TV Size (inches)</h2>
      <input
        type="number"
        value={inputSize}
        onChange={handleSizeChange}
        className="w-full py-2 px-3 rounded-lg bg-gray-100 text-gray-700 border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500 transition duration-200"
        placeholder="Enter TV size in inches"
        min="0"
      />
      {inputSize && (
        <p className="mt-2 text-sm text-gray-600">
          Recommended stand width: {mapSizeToStand(inputSize as number)} cm
        </p>
      )}
    </div>
  );
};

export default TvSizeFilter;