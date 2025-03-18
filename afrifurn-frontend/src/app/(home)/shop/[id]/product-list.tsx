import { Product } from "@/types"
import ProductCard from "@/ui/product-card"
import Link from "next/link"

interface ProductListProps {
    products: Product[]
    viewMode: 'grid' | 'list'
    filters:{}
}

export default function ProductList({ filters,products, viewMode }: ProductListProps) {

    return (
        <div className={viewMode === 'grid' ? 'grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4' : 'space-y-4'}>
            {products.map((product: Product) => (
        <Link key={product._id} href={`/products/${product.short_name}`}>
          <ProductCard product={product} />
        </Link>
      ))}
        </div>
    )
}