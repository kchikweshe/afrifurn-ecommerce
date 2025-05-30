'use client'
import { useState, useEffect } from 'react'
import { FaChevronDown, FaFilter } from 'react-icons/fa'
import { X } from 'lucide-react'

import { useFilterCollection } from '@/hooks/useFilterCollection'
import { Level2Category, Product, FilterParams } from '@/types'
import { Button } from '@/components/ui/button'
import { useDataContext } from '@/data/data.context'
import ColorFilter from '@/ui/filters/ColorFilter'
import PriceFilter from '@/ui/filters/PriceFilter'
import { ProductList } from '@/components/ProductList'
import MaterialFilter from '@/ui/filters/MaterialFilter'
import { FilterSection } from '@/app/(home)/room/[name]/FilterSection'

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
                    {/* Filter Section */}
                    <FilterSection
                        isVisible={true}
                        isSticky={false}
                        filters={filters as any}
                        colors={colors}
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
