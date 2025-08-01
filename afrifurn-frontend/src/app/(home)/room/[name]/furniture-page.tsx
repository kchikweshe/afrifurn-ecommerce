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
    const state = useDataContext();
    const colors = state?.colors || [];
    const materials = state?.materials || [];
    // Filters state (can be expanded as needed)
    const [filters, setFilters] = useState<Partial<FilterParams>>({ level1_category_name: title });
    const [isFilterVisible, setIsFilterVisible] = useState(true)
    const [isMobileFilterOpen, setIsMobileFilterOpen] = useState(false)
    const { data: products, loading, error, filterCollection } = useFilterCollection<Product>()

    const toggleFilters = () => setIsFilterVisible(!isFilterVisible)
    const toggleMobileFilters = () => setIsMobileFilterOpen(!isMobileFilterOpen)
    // Fetch products when filters change

    useEffect(() => {
        filterCollection('products', filters as FilterParams);
    }, [filters, filterCollection]);

    const handleFilterChange = (newFilters: Partial<FilterParams>) => {
        setFilters((prev) => ({ ...prev, ...newFilters }));
    };
    const resetFilters = () => setFilters({ level1_category_name: title });

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
        <main className="min-h-screen bg-white font-sans rounded-lg">
            <div className="container mx-auto px-6 py-8">
                <section>
                    <div className="mb-8">
                        <h1 className="text-2xl text-center lg:text-left  md:text-3xl font-bold mb-4">{title}</h1>
                        <div>
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
                                        {getCategoryName(filters.category_short_name as string)}
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
                            
                            {/* Desktop Filter Button */}
                            <div className="hidden lg:block mb-4">
                                <Button
                                    variant="outline"
                                    onClick={toggleFilters}
                                    className="flex items-center gap-2"
                                >
                                    <Filter className="h-4 w-4" />
                                    {isFilterVisible ? 'Hide Filters' : 'Show Filters'}
                                </Button>
                            </div>
                            <div className='hidden lg:block'>
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
                     
                        </div>

                        {/* Filter Section */}

                    </div>
                </section>

                {/* Product Grid/List */}
                <div >
                    <ProductList products={products || []} />
                </div>
            </div>

            {/* Mobile Filter Modal */}
            {isMobileFilterOpen && (
                <div className="fixed inset-0 z-50 flex items-center justify-center">
                    {/* Backdrop with blur */}
                    <div 
                        className="absolute inset-0 bg-black/20 backdrop-blur-sm"
                        onClick={toggleMobileFilters}
                    />
                    
                    {/* Filter Modal */}
                    <div className="relative bg-white rounded-2xl shadow-2xl mx-4 max-w-md w-full max-h-[80vh] overflow-hidden animate-in slide-in-from-bottom-4 duration-300">
                        <div className="p-6">
                            <div className="flex items-center justify-between mb-6">
                                <h3 className="text-lg font-semibold text-gray-900">Filters</h3>
                                <button
                                    onClick={toggleMobileFilters}
                                    className="p-2 hover:bg-gray-100 rounded-full transition-colors"
                                >
                                    <X className="h-5 w-5 text-gray-500" />
                                </button>
                            </div>
                            
                            <div className="space-y-6">
                                <FilterSection
                                    isVisible={true}
                                    isSticky={false}
                                    filters={filters as any}
                                    colors={colors}
                                    categories={categories}
                                    materials={materials}
                                    onFilterChange={handleFilterChange}
                                    onClearFilters={resetFilters}
                                />
                            </div>
                            
                            <div className="flex gap-3 mt-6 pt-4 border-t border-gray-200">
                                <Button
                                    variant="outline"
                                    onClick={resetFilters}
                                    className="flex-1"
                                >
                                    Clear All
                                </Button>
                                <Button
                                    onClick={toggleMobileFilters}
                                    className="flex-1"
                                >
                                    Apply Filters
                                </Button>
                            </div>
                        </div>
                    </div>
                </div>
            )}

            {/* Mobile Filter Button */}
            <Button
                variant="outline"
                onClick={toggleMobileFilters}
                className="fixed bottom-6 right-6 z-40 md:hidden shadow-lg"
            >
                <Filter className="h-4 w-4 mr-2" />
                Filters
            </Button>
        </main>
    );
}
