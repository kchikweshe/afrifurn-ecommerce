'use client';

import { FilterParams } from '@/types';
import Link from 'next/link';
import React, { use, useEffect, useMemo, useRef, useState } from 'react';

import { Product } from '@/types';
import ProductCard from '@/ui/product-card';
import ProductGridSkeleton from '@/ui/skeleton';
import Pagination from '@/ui/pagination';
import { productService } from '@/services/product.service';

interface ProductGridProps {
  filters: FilterParams;
  page:number,
  pageSize:number
  initialProducts: Promise<Array<Product>>
}

function ProductGrid(props:ProductGridProps): React.JSX.Element {
  const {initialProducts, filters, page, pageSize} = props
  const allProducts = use(initialProducts)

  const [products, setProducts] = useState<Product[]>(allProducts);
  const [totalCount, setTotalCount] = useState<number>(allProducts.length);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const filtersRef = useRef(filters);

  useEffect(() => {
    // Only fetch if filters have changed
    if (JSON.stringify(filtersRef.current) !== JSON.stringify(filters)) {
      const fetchProducts = async () => {
        try {
          setLoading(true);
          const result = await productService.filterProducts(filters);
          setProducts(result);
          setTotalCount(result.length);
          filtersRef.current = filters;
        } catch (err) {
          console.error("Failed to fetch products:", err);
          setError("Failed to load products. Please try again later.");
        } finally {
          setLoading(false);
        }
      };
      
      fetchProducts();
    }
  }, [filters]);

  // Calculate paginated products
  const paginatedProducts = useMemo(() => {
    const startIndex = (page - 1) * pageSize;
    return products.slice(startIndex, startIndex + pageSize);
  }, [products, page, pageSize]);

  if (error) {
    return (
      <div className="flex items-center justify-center min-h-[400px] text-red-500">
        <div className="text-center">
          <span className="material-icons text-3xl mb-2">error_outline</span>
          <p>{error}</p>
        </div>
      </div>
    );
  }

  if (loading) {
    return <ProductGridSkeleton />;
  }

  if (!products || products.length === 0) {
    return (
      <div className="flex items-center justify-center min-h-[400px] text-gray-500">
        <div className="text-center">
          <span className="material-icons text-4xl mb-3">inventory_2</span>
          <p className="text-lg">No products found</p>
          <p className="text-sm mt-2">Try adjusting your filters</p>
        </div>
      </div>
    );
  }

  return (
    <main className="container mx-auto px-4 py-8">
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
        {paginatedProducts.map((product: Product) => (
          <Link
            key={product.short_name}
            href={`/products/${product.short_name}`}
            className="transform transition-transform hover:scale-105 duration-200"
          >
            <ProductCard product={product} />
          </Link>
        ))}
      </div>
      
      {totalCount > pageSize && (
        <div className="mt-8">
          <Pagination
            currentPage={page}
            totalPages={Math.ceil(totalCount / pageSize)}
            baseUrl="/products"
          />
        </div>
      )}
    </main>
  );
}

export default ProductGrid;