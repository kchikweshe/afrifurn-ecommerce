'use client';

import ColorFilter from "@/ui/filters/ColorFilter";
import PriceFilter from "@/ui/filters/PriceFilter";
import WidthFilter from "@/ui/filters/WidthFilter";

import { useDataContext } from "@/data/data.context";
import { useCallback, useEffect, useState } from "react";
import { Button } from "@/components/ui/button"
import { Grid, List } from "lucide-react"
import ProductList from './product-list'
export function useFilters(initialFilters) {
  const [filters, setFilters] = useState(initialFilters);
  const [debouncedFilters, setDebouncedFilters] = useState(initialFilters);

  useEffect(() => {
    const timer = setTimeout(() => {
      setDebouncedFilters(filters);
    }, 300);

    return () => clearTimeout(timer);
  }, [filters]);

  const updateFilters = useCallback((newFilters) => {
    setFilters((prev) => ({ ...prev, ...newFilters }));
    // Update URL
    // router.push({
    //   pathname: router.pathname,
    //   query: { ...router.query, ...newFilters },
    // }, undefined, { shallow: true });
  }, []);

  const resetFilters = useCallback(() => {
    setFilters(initialFilters);
    setDebouncedFilters(initialFilters);
    // router.push(router.pathname, undefined, { shallow: true });
  }, [initialFilters]);

  return { filters: debouncedFilters, updateFilters, resetFilters };
}
export const primaryImage = process.env.NEXT_PUBLIC_PRIMARY_IMAGE 

const handleFilterButtonClick = () => {
  setIsFilterOpen(!isFilterOpen);
};

const ShopPage = ({ initialFilters, data }) => {
  const [isFilterOpen, setIsFilterOpen] = useState(false);
  const { filters, updateFilters, resetFilters } = useFilters(initialFilters);
  const state = useDataContext();
  const [priceRange, setPriceRange] = useState([0, 200])
  const [viewMode, setViewMode] = useState('grid')


  const { colors } = state;

  const handleFilterChange = (newFilters) => {
    updateFilters(newFilters);
  };

  return (
    <main className="flex-grow container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-8">Product Category</h1>

      <div className="mt-4 sm:mt-6 px-4 sm:px-6 lg:px-8">
        <button
          className="lg:hidden w-full py-2 bg-gray-200 text-gray-800 rounded-lg mb-4"
          onClick={handleFilterButtonClick}
          aria-expanded={isFilterOpen}
          aria-controls="filter-menu"
        >
          {isFilterOpen ? 'Hide Filters' : 'Show Filters'}
        </button>

        <div className="flex flex-col md:flex-row gap-8">
          <aside className="w-full md:w-64 space-y-6">
            <PriceFilter
              onFilterChange={(start_price, end_price) => handleFilterChange({ start_price, end_price })}
            />
            <ColorFilter
              colors={colors}
              onFilterChange={(color) => handleFilterChange({ color })}
            />
            <WidthFilter
              onFilterChange={(length) => length && handleFilterChange({ length })}
            />
            <button
              onClick={resetFilters}
              className="mt-4 w-full py-2 bg-red-500 text-white rounded-lg"
            >
              Reset Filters
            </button>
          </aside>

          {/* <div className="flex-1 bg-white shadow-md rounded-lg p-4">

            <ProductGrid filters={filters} initialProducts={data} />
          </div> */}

          <div className="flex-grow">
            <div className="flex justify-between items-center mb-4">
              <p className="text-sm text-gray-600">{data.length} products found</p>
              <div className="flex gap-2">
                <Button
                  variant={viewMode === 'grid' ? 'default' : 'outline'}
                  size="icon"
                  onClick={() => setViewMode('grid')}
                >
                  <Grid className="h-4 w-4" />
                  <span className="sr-only">Grid view</span>
                </Button>
                <Button
                  variant={viewMode === 'list' ? 'default' : 'outline'}
                  size="icon"
                  onClick={() => setViewMode('list')}
                >
                  <List className="h-4 w-4" />
                  <span className="sr-only">List view</span>
                </Button>
              </div>
            </div>
            <ProductList filters={filters} products={data} viewMode={viewMode} />
          </div>
        </div>
      </div>
    </main>
  );
};

export default ShopPage;