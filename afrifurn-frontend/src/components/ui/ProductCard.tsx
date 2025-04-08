import Image from 'next/image'
import { PRODUCT_IMAGE_URLS } from '@/data/urls'
import { Product } from '@/types'
import { useCallback, useContext } from 'react'
import { DataContext } from '@/data/data.context'

export const ProductCard = ({ product }: { product: Product }) => {
    const state = useContext(DataContext)
    const getMaterialName = useCallback((materialId: string | null) => {
        if (!materialId) return 'Unknown'
        const materials = state?.materials ?? []
        const material = materials.find(m => m._id === materialId)
        return material ? material.name : materialId
    }, [state])

    if(!state){
        return <div>
            State is null
        </div>
    }
    
    console.log("Product in ProductCard: ",product)
    return <div className="group">
        <div className="relative aspect-square overflow-hidden mb-4 rounded-lg">
            <Image
                src={PRODUCT_IMAGE_URLS + product?.product_variants[0]?.images[0]}
                alt={product.name}
                layout="fill"
                objectFit="cover"
                className="transition-transform duration-300 ease-in-out group-hover:scale-105"
            />
            {product.is_new && (
                <div className="absolute top-2 left-2 bg-primary text-primary-foreground px-2 py-1 text-xs font-semibold rounded">
                    New
                </div>
            )}
            {product.discount && (
                <div className="absolute top-2 right-2 bg-red-500 text-white px-2 py-1 text-xs font-semibold rounded">
                    {product.discount}% OFF
                </div>
            )}
        </div>
        <h3 className="text-lg font-normal mb-1 transition-colors duration-200 ease-in-out group-hover:text-primary">{product.name}</h3>
        <p className="text-sm text-gray-600 mb-1">${product?.price?.toFixed(2)}</p>
        <div className="flex items-center space-x-2">
            <div className="flex space-x-1">
                {product.product_variants?.map((variant,i) => (
                    <div
                        key={i}
                        className="w-4 h-4 rounded-full border border-gray-300"
                        style={{ backgroundColor: variant.color_id }}
                        // title={variant.color}
                    />
                ))}
            </div>
            <span className="text-sm text-gray-500">{getMaterialName(product.material ?? null)}</span>
        </div>
    </div>
}