import { productService } from '@/services/product.service';
import { FilterParams } from '@/types';
import { FilterProductsParams } from '@/services/product.service';
import ProductGrid from '@/ui/product-grid';
import ProductGridSkeleton from '@/ui/skeleton';
import React, { Suspense } from 'react';

export const revalidate = 3600; // Revalidate every hour, adjust as needed

interface ProductsPageProps {
  searchParams: Promise<FilterProductsParams & { page: string }>;
}

export default async function ProductsPage(props: ProductsPageProps) {
  const searchParams = await props.searchParams;
  const page = parseInt(searchParams.page || '1', 10);
  const pageSize = 12;

  const products =  await productService.filterProducts({
    ...searchParams,
    page,
    page_size: pageSize,
  });
  const filters:FilterParams={}

  return (
    <div>
      <h1>Products</h1>
      <Suspense fallback={<ProductGridSkeleton />}>
        <ProductGrid 
          page={page} 
          pageSize={pageSize} 
          filters={filters}  
          initialProducts={Promise.resolve(products)} 
        />
      </Suspense>
      
    </div>
  );
}