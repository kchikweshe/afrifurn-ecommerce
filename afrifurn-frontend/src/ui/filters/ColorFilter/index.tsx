'use client'
import { Color } from '@/types';
import { useState } from 'react';
import Image from 'next/image';
import { PRODUCT_IMAGE_URLS } from '@/data/urls';
const ColorFilter = ({ colors, onFilterChange }: { colors: Color[], onFilterChange: Function }) => {
  const [selectedColor, setSelectedColor] = useState<string | null>(null);

  const handleChange = (newColor:string) => {
    setSelectedColor(newColor === selectedColor ? null : newColor);
    onFilterChange(newColor === selectedColor ? null : newColor);
  }

  return (
    <div className="p-2 sm:p-4">
      <h3 className="text-md font-medium mb-2">Colors</h3>
      <div className="flex flex-wrap gap-2">
        {colors.map((color, index) => (
          <button
            key={index}
            className={`w-8 h-8 rounded-full border-2 ${selectedColor == color.color_code ? 'border-black' : 'border-blue-400'
              }`}
            style={{ backgroundColor: color.color_code }}
            onClick={() => handleChange(color.color_code)}
            aria-label={`Filter by ${color}`}
          />
        ))}
      </div>
    </div>
  );
};

export default ColorFilter;