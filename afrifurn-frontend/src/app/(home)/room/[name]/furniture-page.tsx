'use client'
import { useState, useEffect } from 'react'
import { FaChevronDown } from 'react-icons/fa'
import { Filter, X } from 'lucide-react'

import { useFilterCollection } from '@/hooks/useFilterCollection'
import { Level2Category, Product, FilterParams } from '@/types'
import { Button } from '@/components/ui/button'
import { useDataContext } from '@/data/data.context'
import { ProductList } from '@/components/ProductList'
import { FilterSection } from '@/components/ui/FilterSection'

interface FurniturePageProps {
    shortName: string
    title: string
    categories: Array<Level2Category>
}

// FilterButton component
function FilterButton({ label, icon, children }: { label: string, icon?: React.ReactNode, children?: React.ReactNode }) {
    const [open, setOpen] = useState(false)

    return (
        <div className="relative">
            <button
                className="rounded-full bg-gray-100 px-5 py-2 font-semibold flex items-center gap-2 focus:outline-none focus:ring-2 focus:ring-blue-400"
                onClick={() => setOpen((v) => !v)}
                type="button"
            >
                {label}
                {icon ? icon : <FaChevronDown className="ml-1 text-xs" />}
            </button>
            {open && children && (
                <div className="absolute left-0 mt-2 z-40 bg-white rounded-xl shadow-lg p-4 min-w-[200px]">
                    {children}
                </div>
            )}
        </div>
    )
}

export default function FurniturePage({ shortName, title, categories }: FurniturePageProps) {
    const { data: products, loading, error, filterCollection } = useFilterCollection<Product>()
    const state = useDataContext();
    const colors = state?.colors || [];
    const materials = state?.materials || [];
    
    // Filters state (can be expanded as needed)
    const [filters, setFilters] = useState<Partial<FilterParams>>({});
    const [viewMode, setViewMode] = useState('grid');
    const [isFilterVisible, setIsFilterVisible] = useState(false)

    const toggleFilters = () => setIsFilterVisible(!isFilterVisible)
   if(!(categories.length>0)){
    return categories.length
   }
    // Fetch products when filters change
    useEffect(() => {
        filterCollection('products', filters as FilterParams);
    }, [filters, filterCollection]);

    const handleFilterChange = (newFilters: Partial<FilterParams>) => {
        setFilters((prev) => ({ ...prev, ...newFilters }));
    };
    const resetFilters = () => setFilters({});

    // Helper to get label for selected filters
    const getColorName = (code: string) => colors.find(c => c.color_code === code)?.name || code;
    const getMaterialName = (id: string) => materials.find(m => m._id === id)?.name || id;
    const getCategoryName = (shortName: string) => categories.find(c => c.short_name === shortName)?.name || shortName;

    // Remove a filter chip
    const removeFilter = (type: string, value?: string) => {
        setFilters(prev => {
            const updated = { ...prev };
            if (type === 'colors') updated.colors = [];
            if (type === 'materials') updated.materials = [];
            if (type === 'category_short_name') updated.category_short_name = '';
            if (type === 'sort_by') updated.sort_by = '';
            return updated;
        });
    };

    return (
        <main className="min-h-screen bg-white font-sans">
            <div className="container mx-auto px-6 py-8">
                <div className="mb-8">
                    <h1 className="text-3xl font-bold mb-4">{title}</h1>
                    
                    
                     {/* Filter Chips */}
                    <div className="flex flex-wrap gap-2 mb-4">
                        {filters.colors && filters.colors.length > 0 && filters.colors.map((code: string) => (
                            <span key={code} className="flex items-center bg-blue-100 text-blue-800 rounded-full px-3 py-1 text-sm font-semibold">
                                Color: {getColorName(code)}
                                <button className="ml-2" onClick={() => removeFilter('colors', code)}><X size={14} /></button>
                            </span>
                        ))}
                        {filters.materials && filters.materials.length > 0 && filters.materials.map((id: string) => (
                            <span key={id} className="flex items-center bg-green-100 text-green-800 rounded-full px-3 py-1 text-sm font-semibold">
                                Material: {getMaterialName(id)}
                                <button className="ml-2" onClick={() => removeFilter('materials', id)}><X size={14} /></button>
                            </span>
                        ))}
                        {filters.category_short_name && (
                            <span className="flex items-center bg-purple-100 text-purple-800 rounded-full px-3 py-1 text-sm font-semibold">
                                Category: {getCategoryName(filters.category_short_name as string)}
                                <button className="ml-2" onClick={() => removeFilter('category_short_name')}><X size={14} /></button>
                            </span>
                        )}
                        {filters.sort_by && (
                            <span className="flex items-center bg-yellow-100 text-yellow-800 rounded-full px-3 py-1 text-sm font-semibold">
                                Sort by: {filters.sort_by}
                                <button className="ml-2" onClick={() => removeFilter('sort_by')}><X size={14} /></button>
                            </span>
                        )}
                    </div>
                
                    <Button
                    variant="outline"
                    onClick={toggleFilters}
                    className="fixed left-2 top-1/2 z-10 transition-all duration-300 ease-in-out -translate-y-1/2"
                >
                    <Filter className="h-4 w-4" />
                </Button>
                    {/* Filter Section */}
                  
                    <FilterSection
                        isVisible={isFilterVisible}
                        isSticky={false}
                        filters={filters as any}
                        colors={colors}
                        categories={categories}
                        materials={materials}
                        onFilterChange={handleFilterChange}
                        onClearFilters={resetFilters}
                    />
                </div>
                {/* Product Grid/List */}
                <div>
                    <ProductList products={products || []} />
                </div>
            </div>
        </main>
    );
}
