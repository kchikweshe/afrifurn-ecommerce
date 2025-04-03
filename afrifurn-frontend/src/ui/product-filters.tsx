import { useState, useContext } from 'react';
import { Color } from '@/types';
import { DataContext } from '@/data/data.context';

interface ProductFiltersProps {
  filters: {
    colors: string[];
    priceRange: [number, number];
    inStock: boolean;
  };
  onFilterChange: (filters: any) => void;
}

export default function ProductFilters({ filters, onFilterChange }: ProductFiltersProps) {
  const [expanded, setExpanded] = useState({
    colors: true,
    price: true,
    availability: true,
  });

  const state = useContext(DataContext);
  if (!state) return null;
  const { colors } = state;
  const toggleSection = (section: keyof typeof expanded) => {
    setExpanded({ ...expanded, [section]: !expanded[section] });
  };

  return (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200">
      <h2 className="text-xl font-medium px-6 py-4 border-b border-gray-200">Filters</h2>

      <div className="p-6 space-y-6">
        <div>
          <button
            className="flex justify-between items-center w-full text-left text-lg font-medium text-gray-700 focus:outline-none"
            onClick={() => toggleSection('colors')}
          >
            Colors
            <span className="material-icons">
              {expanded.colors ? 'expand_less' : 'expand_more'}
            </span>
          </button>
          {expanded.colors && (
            <div className="mt-4 space-y-2">
              {colors?.map((color:Color) => (
                <label key={color._id} className="flex items-center group cursor-pointer">
                  <input
                    type="checkbox"
                    checked={filters.colors.includes(color.color_code)}
                    onChange={() => {
                      const newColors = filters.colors.includes(color.color_code)
                        ? filters.colors.filter((c) => c !== color.color_code)
                        : [...filters.colors, color.color_code];
                      onFilterChange({ colors: newColors });
                    }}
                    className="form-checkbox h-5 w-5 text-blue-600 transition duration-150 ease-in-out"
                  />
                  <span
                    className="w-6 h-6 inline-block ml-3 rounded-full border-2 border-gray-200 group-hover:border-gray-300"
                    style={{ backgroundColor: color.color_code }}
                  ></span>
                  <span className="ml-3 text-gray-700 group-hover:text-gray-900">{color.name}</span>
                </label>
              ))}
            </div>
          )}
        </div>

        <div>
          <button
            className="flex justify-between items-center w-full text-left text-lg font-medium text-gray-700 focus:outline-none"
            onClick={() => toggleSection('price')}
          >
            Price Range
            <span className="material-icons">
              {expanded.price ? 'expand_less' : 'expand_more'}
            </span>
          </button>
          {expanded.price && (
            <div className="mt-4">
              <input
                type="range"
                min="0"
                max="1000"
                step="10"
                value={filters.priceRange[1]}
                onChange={(e) => onFilterChange({ priceRange: [0, Number(e.target.value)] })}
                className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer"
              />
              <div className="flex justify-between mt-2 text-sm text-gray-600">
                <span>$0</span>
                <span>${filters.priceRange[1]}</span>
              </div>
            </div>
          )}
        </div>

        <div>
          <button
            className="flex justify-between items-center w-full text-left text-lg font-medium text-gray-700 focus:outline-none"
            onClick={() => toggleSection('availability')}
          >
            Availability
            <span className="material-icons">
              {expanded.availability ? 'expand_less' : 'expand_more'}
            </span>
          </button>
          {expanded.availability && (
            <div className="mt-4">
              <label className="inline-flex items-center cursor-pointer">
                <input
                  type="checkbox"
                  checked={filters.inStock}
                  onChange={(e) => onFilterChange({ inStock: e.target.checked })}
                  className="form-checkbox h-5 w-5 text-blue-600 transition duration-150 ease-in-out"
                />
                <span className="ml-3 text-gray-700">In Stock Only</span>
              </label>
            </div>
          )}
        </div>
      </div>

      <div className="px-6 py-4 bg-gray-50 border-t border-gray-200">
        <button
          onClick={() => onFilterChange({ colors: [], priceRange: [0, 1000], inStock: false })}
          className="w-full px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md shadow-sm hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
        >
          Clear All Filters
        </button>
      </div>
    </div>
  );
}