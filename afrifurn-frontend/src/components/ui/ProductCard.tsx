'use client'
import Image from 'next/image'
import { PRODUCT_IMAGE_URLS } from '@/data/urls'
import { Product } from '@/types'
import { useCallback, useContext, useRef } from 'react'
import { DataContext } from '@/data/data.context'
import { Carousel, CarouselContent, CarouselItem, CarouselNext, CarouselPrevious } from './carousel'

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
        <div className="group">
            {/* Image Carousel */}
            {/* <div className="relative w-full overflow-x-auto mb-4 whitespace-nowrap scroll-smooth">
                <div className="flex gap-4 w-fit">
                    {uniqueVariants.map((variant, index) => (
                        <div
                            key={variant.color_id}
                            className="relative min-w-[250px] aspect-square rounded-2xl shadow-lg overflow-hidden"
                            ref={el => (imageRefs.current[index] = el)}
                        >
                            <Image
                                src={PRODUCT_IMAGE_URLS + variant.images[0]}
                                alt={product.name}
                                layout="fill"
                                objectFit="cover"
                                className="transition-transform duration-300 ease-in-out group-hover:scale-105"
                            />
                            {product.discount && (
                                <div className="absolute top-2 right-2 bg-red-500 text-white px-2 py-1 text-xs font-semibold rounded">
                                    {product.discount}% OFF
                                </div>
                            )}
                        </div>
                    ))}
                </div>
            </div> */}
            <Carousel>
                <CarouselContent>
                    {uniqueVariants.map((variant, index) => (
                        <CarouselItem
                            key={variant.color_id}
                            className="relative min-w-[250px] aspect-square rounded-2xl shadow-lg "
                        >
                            <Image
                                src={PRODUCT_IMAGE_URLS + variant.images[0]}
                                alt={product.name}
                                layout="fill"
                                quality={100}
                                objectFit="cover"
                                className="rounded-2xl transition-transform duration-300 ease-in-out group-hover:scale-105"
                            />
                            {product.discount && (
                                <div className="absolute top-2 right-2 bg-red-500 text-white px-2 py-1 text-xs font-semibold rounded">
                                    {product.discount}% OFF
                                </div>
                            )}
                        </CarouselItem>
                    ))}
                </CarouselContent>
                <CarouselPrevious className="left-2 md:left-8 h-8 w-8 md:h-10 md:w-10 bg-white text-black border-none rounded-full" />
                <CarouselNext className="right-2 md:right-8 h-8 w-8 md:h-10 md:w-10 bg-white text-black border-none rounded-full" />

            </Carousel>

            {/* Product Info */}
            <h3 className="text-sm mt-3 text-gray-600  font-semibold mb-1 transition-colors duration-200 ease-in-out group-hover:text-primary">
                {product.name}
            </h3>

            <p className="text-2xl mt-3 font-bold text-gray-800 mb-2">
                ${whole}
                <sup className="align-super text-xs font-medium ml-0.5">{cents}</sup>
            </p>

            {/* Color Swatches */}
            <div className="flex items-center space-x-3 mt-3">
                <div className="grid grid-cols-5 gap-2">
                    {uniqueVariants.map((variant, index) => {
                        const colorObj = colors.find(c => c.color_code === variant.color_id)
                        return (
                            <button
                                key={variant.color_id}
                                onClick={() => scrollToVariant(index)}
                                className="w-7 h-7 rounded-full border-1 shadow-md focus:outline-none hover:scale-105 active:scale-95 transition-all duration-200"
                                aria-label={colorObj?.name || variant.color_id}
                            >
                                {colorObj?.image?.length ? (
                                    <Image
                                        width={128}
                                        height={128}
                                        src={PRODUCT_IMAGE_URLS + colorObj.image}
                                        alt={colorObj.name}
                                        className="rounded-full object-cover w-7 h-7"
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
    )
}
