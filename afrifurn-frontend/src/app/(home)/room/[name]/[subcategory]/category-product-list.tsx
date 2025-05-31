'use client'

import React, { useState, useEffect, useRef, useCallback } from 'react'
import { Filter } from 'lucide-react'
import { Button } from "@/components/ui/button"
import { Skeleton } from "@/components/ui/skeleton"
import { FilterParams } from '@/types'
import { useDataContext } from '@/data/data.context'
import { useFilters } from '@/app/(home)/shop/[id]/shop'
import { useFilterCollection } from '@/hooks/useFilterCollection'
import { CategoryProducts, Product } from '@/types'

import { FilterSection } from '../FilterSection'
import { Pagination } from '@/components/ui/Pagination'
import { ProductCard } from '@/components/ui/ProductCard'
import Link from 'next/link'


const PRODUCTS_PER_PAGE = 10

export function CategoryProductsGrid({ categoryProducts,short_name }: { categoryProducts: CategoryProducts,short_name:string }) {
    
    const [currentPage, setCurrentPage] = useState(1)
    const [isFilterVisible, setIsFilterVisible] = useState(false)
    const [isFilterSticky, setIsFilterSticky] = useState(false)
    const filterRef = useRef<HTMLDivElement>(null)

    const state = useDataContext()
    const { filters, updateFilters, resetFilters } = useFilters({
        start_price: 0,
        end_price: 1000,
        colors: [],
        materials: [],
        category_short_name: short_name,
        sort_by: 'price',
        sort_order: 1,
    })
    const { data: filteredProducts, error, loading, filterCollection } = useFilterCollection<Product>()

    const fetchProducts = useCallback(() => {
        filterCollection('products', filters)
    }, [filterCollection, filters])

    useEffect(() => {
        fetchProducts()
    }, [filters, fetchProducts])

    useEffect(() => {
        const handleScroll = () => {
            if (filterRef.current) {
                const { top } = filterRef.current.getBoundingClientRect()
                setIsFilterSticky(top <= 0)
            }
        }

        window.addEventListener('scroll', handleScroll)
        return () => window.removeEventListener('scroll', handleScroll)
    }, [])

    if (!state) {
        return <div>Loading...</div>
    }

    const { materials, colors } = state

    const handleFilterChange = (newFilters: Partial<FilterParams>) => {
        updateFilters({ ...filters, ...newFilters, page: 1 })
        setCurrentPage(1)
    }

    const clearFilters = () => {
        resetFilters()
        setCurrentPage(1)
    }

    const toggleFilters = () => setIsFilterVisible(!isFilterVisible)

    const indexOfLastProduct = currentPage * PRODUCTS_PER_PAGE
    const indexOfFirstProduct = indexOfLastProduct - PRODUCTS_PER_PAGE
    const currentProducts = filteredProducts.length>0 ? filteredProducts.slice(indexOfFirstProduct, indexOfLastProduct) : []
    const totalPages = filteredProducts.length>0 ? Math.ceil(filteredProducts.length / PRODUCTS_PER_PAGE) : 0
    console.log("Current Products:  \n",currentProducts)
    
    // if (!categoryProducts) { }
    return (
        <div className="min-h-screen flex flex-col">
            <main className="flex-grow container mx-auto px-4 py-8 relative">
                <h1 className="text-4xl font-normal tracking-wide mb-8">{categoryProducts.category_name}</h1>

                <Button
                    variant="outline"
                    onClick={toggleFilters}
                    className="fixed left-2 top-1/2 z-10 transition-all duration-300 ease-in-out -translate-y-1/2"
                >
                    <Filter className="h-4 w-4" />
                </Button>

                <FilterSection
                categories={[]}
                    ref={filterRef}
                    isVisible={isFilterVisible}
                    isSticky={isFilterSticky}
                    filters={filters}
                    colors={colors}
                    materials={materials}
                    onFilterChange={handleFilterChange}
                    onClearFilters={clearFilters}
                />

                <div className="mt-8">
                    {loading || !state ? (
                        <ProductSkeletons count={PRODUCTS_PER_PAGE} />
                    ) : error ? (
                        <p>Error: {error.message}</p>
                    ) : (
                        <>
                            <p className="text-sm mb-4">{filteredProducts?.length || 0} products</p>

                            <div className="grid grid-cols-2 sm:grid-cols-2 lg:grid-cols-4 xl:grid-cols-4 gap-6">
                                {currentProducts?.map((product) => (
                                    <Link href={'/room/' + product.short_name} key={product._id}>
                                        <ProductCard key={product._id }product={product} />
                                    </Link>
                                ))}
                            </div>

                            {totalPages > 1 && (
                                <Pagination
                                    currentPage={currentPage}
                                    totalPages={totalPages}
                                    onPageChange={setCurrentPage}
                                />
                            )}
                        </>
                    )}
                </div>
            </main>
        </div>
    )
}

const ProductSkeletons = ({ count }: { count: number }) => (
    <>
        <p className="text-sm mb-4">Loading products...</p>
        <div className="grid grid-cols-2 sm:grid-cols-2 lg:grid-cols-4 xl:grid-cols-4 gap-6">
            {Array(count).fill(0).map((_, index) => (
                <div key={index} className="space-y-2">
                    <Skeleton className="h-[200px] w-full" />
                    <Skeleton className="h-4 w-3/4" />
                    <Skeleton className="h-4 w-1/2" />
                </div>
            ))}
        </div>
    </>
)