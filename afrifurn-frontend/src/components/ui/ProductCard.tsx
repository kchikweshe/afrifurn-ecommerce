'use client'

import Image from 'next/image'
import { PRODUCT_IMAGE_URLS } from '@/data/urls'
import { Product } from '@/types'
import { useCallback, useContext, useRef } from 'react'
import { DataContext } from '@/data/data.context'
import {
    Carousel,
    CarouselContent,
    CarouselItem,
    CarouselNext,
    CarouselPrevious
} from './carousel'

export const ProductCard = ({ product }: { product: Product }) => {
    const state = useContext(DataContext)
    const imageRefs = useRef<(HTMLDivElement | null)[]>([])

    const getMaterialName = useCallback((materialId: string | null) => {
        if (!materialId) return 'Unknown'
        const materials = state?.materials ?? []
        const material = materials.find(m => m._id === materialId)
        return material ? material.name : materialId
    }, [state])

    if (!state) return <div>State is null</div>

    const { colors } = state

    const formatPrice = (price: number) => {
        const [whole, cents] = price.toFixed(2).split('.')
        return { whole, cents }
    }

    const price = product?.price ?? 0
    const { whole, cents } = formatPrice(price)

    const scrollToVariant = (index: number) => {
        const ref = imageRefs.current[index]
        if (ref) {
            ref.scrollIntoView({ behavior: 'smooth', inline: 'center', block: 'nearest' })
        }
    }

    const uniqueVariants = Array.from(
        new Map(product.product_variants.map(v => [v.color_id, v])).values()
    )

    return (
        <div className="group relative bg-white rounded-2xl shadow-md hover:shadow-xl transition-all duration-300 overflow-hidden border border-gray-100">
            {/* Carousel */}
            <Carousel>
                <CarouselContent>
                    {uniqueVariants.map((variant, index) => (
                        <CarouselItem
                            key={variant.color_id}
                            className="relative aspect-[4/3] overflow-hidden"
                        >
                            <Image
                                src={PRODUCT_IMAGE_URLS + variant.images[0]}
                                alt={product.name}
                                fill
                                quality={85}
                                sizes="(max-width: 768px) 100vw, 33vw"
                                className="object-cover group-hover:scale-105 transition-transform duration-300 ease-in-out"
                                priority={index === 0}
                            />
                            {product.discount && (
                                <div className="absolute top-2 right-2 bg-red-500 text-white px-2 py-1 text-xs font-semibold rounded">
                                    {product.discount}% OFF
                                </div>
                            )}
                        </CarouselItem>
                    ))}
                </CarouselContent>

                <CarouselPrevious className="left-2 md:left-4 h-8 w-8 bg-white/70 backdrop-blur-md text-black border-none rounded-full shadow" />
                <CarouselNext className="right-2 md:right-4 h-8 w-8 bg-white/70 backdrop-blur-md text-black border-none rounded-full shadow" />
            </Carousel>

            {/* Content */}
            <div className="px-4 pt-4 pb-5 space-y-2">
                {/* Title */}
                <h3 className="text-base font-semibold text-gray-700 group-hover:text-primary transition-colors truncate">
                    {product.name}
                </h3>

                {/* Price */}
                <p className="text-xl font-bold text-gray-900">
                    ${whole}
                    <sup className="text-xs font-medium ml-0.5 align-super">{cents}</sup>
                </p>

                {/* Colors */}
                <div className="pt-3">
                    <div className="text-xs text-gray-500 mb-1">
                        {uniqueVariants.length} Color{uniqueVariants.length > 1 ? 's' : ''} Available
                    </div>

                    <div className="flex gap-2 overflow-x-auto scrollbar-hide">
                        {uniqueVariants.map((variant, index) => {
                            const colorObj = colors.find(c => c.color_code === variant.color_id)
                            return (
                                <button
                                    key={variant.color_id}
                                    onClick={() => scrollToVariant(index)}
                                    className="relative flex-shrink-0 w-7 h-7 rounded-full border shadow-sm hover:ring-2 hover:ring-primary focus:outline-none transition-transform duration-200 hover:scale-110 active:scale-95"
                                    aria-label={colorObj?.name || variant.color_id}
                                    title={colorObj?.name || variant.color_id}
                                >
                                    {colorObj?.image?.length ? (
                                        <Image
                                            width={28}
                                            height={28}
                                            src={PRODUCT_IMAGE_URLS + colorObj.image}
                                            alt={colorObj.name}
                                            className="rounded-full object-cover w-full h-full"
                                        />
                                    ) : (
                                        <span
                                            className="rounded-full w-full h-full block"
                                            style={{ backgroundColor: colorObj?.color_code || '#ccc' }}
                                        />
                                    )}
                                </button>
                            )
                        })}
                    </div>
                </div>
            </div>
        </div>
    )
}
