import { Product } from '@/types'
import { ProductCard } from '@/components/ui/ProductCard'
import Link from 'next/link'

interface ProductListProps {
    products: Product[]
}

export function ProductList({ products }: ProductListProps) {
    console.log("Products in ProductList:  ",products)
    return (
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
            {products?.map((product) => (
                <Link href={`/products/${product.short_name}`} key={product._id}>
                     <ProductCard key={product._id} product={product} />
                </Link>
               
            ))}
        </div>
    )
} 