import { useState, useEffect } from 'react'
import { CategoryProducts } from '@/types'
import { productService } from '@/services/product.service'


export function useCategoryProducts(categories: string[], shortName: string) {
    const [categoryProducts, setCategoryProducts] = useState<CategoryProducts[]>([])
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState<Error | null>(null)

    useEffect(() => {
        const fetchProducts = async () => {
            try {
                console.log("Fetching products for categories:", categories)
                console.log("Using shortName:", shortName)
                
                setLoading(true)
                const productsPromises = categories.map(category =>
               productService.filterCategoryProducts({ name: category })
                )
                const results = await Promise.all(productsPromises)
                console.log("API Results:", results)

                // Map the results to the correct format
                
            
                setCategoryProducts(results)
            } catch (err) {
                console.error('Error fetching category products:', err)
                setError(err as Error)
            } finally {
                setLoading(false)
            }
        }

        if (categories.length > 0 && shortName) {
            fetchProducts()
        }
    }, [categories, shortName])

    return { categoryProducts, loading, error }
}