import { useState } from 'react'
import { Product } from '@/types'
import { ProductCard } from '@/components/ui/ProductCard'
import Link from 'next/link'

interface ProductListProps {
    products: Product[]
    productsPerPage?: number
}

export function ProductList({ products, productsPerPage = 12 }: ProductListProps) {
    const [currentPage, setCurrentPage] = useState(1);

    if (!products || products.length === 0) {
        return (
            <div className="w-full text-center py-10 text-gray-500 text-lg">
                No products found.
            </div>
        );
    }

    const totalPages = Math.ceil(products.length / productsPerPage);
    const startIdx = (currentPage - 1) * productsPerPage;
    const endIdx = startIdx + productsPerPage;
    const currentProducts = products.slice(startIdx, endIdx);

    return (
        <div>
            <div className="h-[600px] overflow-y-auto">
                <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
                    {currentProducts.map((product) => (
                        <Link href={`/room/${product.category.level_one_category.short_name}/${product.category.short_name}/${product.short_name}`} key={product._id}>
                            <ProductCard key={product._id} product={product} />
                        </Link>
                    ))}
                </div>
            </div>
            {/* Pagination Controls */}
            <div className="flex justify-center items-center gap-2 mt-4">
                <button
                    className="px-3 py-1 rounded border disabled:opacity-50"
                    onClick={() => setCurrentPage((p) => Math.max(1, p - 1))}
                    disabled={currentPage === 1}
                >
                    Prev
                </button>
                {Array.from({ length: totalPages }, (_, i) => (
                    <button
                        key={i}
                        className={`px-3 py-1 rounded border ${currentPage === i + 1 ? 'bg-primary text-white' : ''}`}
                        onClick={() => setCurrentPage(i + 1)}
                    >
                        {i + 1}
                    </button>
                ))}
                <button
                    className="px-3 py-1 rounded border disabled:opacity-50"
                    onClick={() => setCurrentPage((p) => Math.min(totalPages, p + 1))}
                    disabled={currentPage === totalPages}
                >
                    Next
                </button>
            </div>
        </div>
    )
} 