import { CategoryProducts } from '@/types'
import { ProductList } from '@/components/ProductList'

export function CategorySection({ category }: { category: CategoryProducts }) {
   
    console.log('CategorySection rendered with category:', category)
    if (category?.products?.length===0) {
        return (
            <div className="flex items-center justify-center py-8">
                <p className="text-xl text-gray-500">No products found in {category?.category_name}</p>
            </div>
        )
    }

    return (
        <section className="mb-6">
            <ProductList products={category?.products} />
        </section>
    )
} 