/**
 * ProductOverview Component
 * 
 * Main product display component that shows detailed product information and handles
 * product variant selection and cart interactions.
 * 
 * Features:
 * - Product image gallery with thumbnail navigation
 * - Product variant selection
 * - Dynamic price calculation with discounts
 * - Add to cart functionality with success feedback
 * - Responsive layout
 * 
 * State Management:
 * - selectedVariant: Currently selected product variant
 * - mainImage: Index of the currently displayed main image
 * - showAddedBadge: Controls visibility of "Added to Cart" indicator
 * 
 * @component
 * @param {Object} props
 * @param {Product} props.product - The product object containing all product information
 */

'use client'

import { useState, useMemo, useCallback } from 'react'
import { useToast } from '@/hooks/use-toast'
import { Product, ProductVariant, ProductFeature, ProductReview } from '@/types'
import type { CartItem } from '@/types/cart'
import { useCart } from '@/context/cart/use-cart'
import { ProductGallery } from '@/components/products/product-gallery'
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { FaStar, FaWhatsapp } from "react-icons/fa"
import { useDataContext } from '@/data/data.context'
import { PRODUCT_IMAGE_URLS } from '@/data/urls'
import Image from 'next/image'

interface ProductOverviewProps {
    /** Product object containing all product details */
    product: Product;
}

const TABS = [
    { key: 'features', label: 'Features' },
    { key: 'specs', label: 'Specifications' },
    { key: 'shipping', label: 'Shipping' },
    { key: 'reviews', label: `Reviews` },
]

export default function ProductOverview({ product }: ProductOverviewProps) {
    /** Currently selected product variant */
    const [selectedVariant, setSelectedVariant] = useState(product.product_variants[0])

    /** Index of currently displayed main image */
    const [mainImage, setMainImage] = useState(0)

    /** Controls visibility of "Added to Cart" indicator */
    const [showAddedBadge, setShowAddedBadge] = useState(false)

    const [quantity, setQuantity] = useState(1)
    const [activeTab, setActiveTab] = useState('features')
    const [starFilter, setStarFilter] = useState<number | null>(null)
    const [page, setPage] = useState(1)
    const pageSize = 3

    const { toast } = useToast()
    const { addToCart } = useCart()

    const state = useDataContext()

    if (!state) {
        return <div>Loading...</div>
    }
    const { colors } = state

    /**
     * Handles selection of a new product variant
     * @param variant - The selected product variant
     */
    const handleVariantSelect = useCallback((variant: ProductVariant) => {
        const targetVariant = product.product_variants.find(v => v.color_id === variant.color_id)
        if (targetVariant) {
            setSelectedVariant(targetVariant)
            setMainImage(0)
        }
    }, [product.product_variants])

    /**
     * Calculates the discounted price based on original price and discount percentage
     */
    const discountedPrice = useMemo(() => {
        return product.price * (1 - (product.discount || 0) / 100)
    }, [product.price, product.discount])

    /**
     * Handles adding the current product variant to the cart
     * Shows success/error toast and temporary success badge
     */
    const handleAddToCart = useCallback(() => {
        try {
            const cartItem: CartItem = {
                productId: product._id,
                name: product.name,
                price: discountedPrice,
                image: selectedVariant.images[0],
                variantId: selectedVariant._id,
                color: selectedVariant.color_id,
                quantity,
            }
            addToCart(cartItem)
            setShowAddedBadge(true)
            toast({ title: "Success", description: "Item added to cart successfully.", variant: "default" })


            setTimeout(() => setShowAddedBadge(false), 2000)
        } catch (error) {
            toast({ title: "Error", description: "Failed to add item to cart", variant: "destructive" })
        }
    }, [product, selectedVariant, discountedPrice, quantity, toast, addToCart])

    // WhatsApp chat handler
    const handleWhatsAppClick = () => {
        const productUrl = typeof window !== 'undefined'
            ? window.location.href
            : `https://afri-furn.co.zw/room/${product.category.level_one_category.short_name}/${product.category.short_name}/${product.short_name}`;

        const imageUrl = PRODUCT_IMAGE_URLS + selectedVariant.images[0];
        const colorObj = colors.find(c => c.color_code === selectedVariant.color_id);
        const colorName = colorObj?.name || selectedVariant.color_id;

        const message = `Hi, I'm interested in this product:\n\n${product.name} (${colorName})\n${productUrl}`;
        const whatsappUrl = `https://wa.me/263778588495?text=${encodeURIComponent(message)}`;

        window.open(whatsappUrl, '_blank');
    }

    if (product.reviews?.length === 0) {
        return <div>No reviews found</div>
    }
    // Reviews logic (pagination and filter)
    const filteredReviews = starFilter
        ? product?.reviews?.filter(r => r.rating === starFilter)
        : product?.reviews
    const totalReviews = filteredReviews?.length
    const paginatedReviews = filteredReviews?.slice((page - 1) * pageSize, page * pageSize)
    const maxPage = totalReviews ? Math.max(1, Math.ceil(totalReviews / pageSize)) : 1

    // Star rating average
    const avgRating =
        Array.isArray(product?.reviews) && product.reviews.length > 0
            ? (
                product.reviews.reduce((sum, r) => sum + r.rating, 0) /
                product.reviews.length
            ).toFixed(1)
            : '0.0'


    const handleQuantityChange = (delta: number) => {
        setQuantity(q => Math.max(1, Math.min(q + delta, 5))) // Assume 5 available for now
    }

    return (
        <div className=" px-2 min-h-screen flex flex-col lg:flex-row gap-10 lg:gap-16 items-stretch">
            {/* Gallery */}
            <div className="w-full flex flex-col justify-center
                lg:w-3/5 lg:min-h-[500px] xl:w-2/3 xl:min-h-[700px]">
                <ProductGallery
                    product={product}
                    selectedVariant={selectedVariant}
                    mainImage={mainImage}
                    setMainImage={setMainImage}
                />
            </div>
            {/* Product Details */}
            <div className="lg:w-1/2 w-full flex flex-col gap-6 h-full justify-center overflow-y-auto">
                {/* Category badge */}
                <div className="mb-2">
                    <Badge className="bg-blue-100 text-blue-800 font-semibold px-3 py-1 rounded-full text-md">
                        {product.category?.name || 'Category'}
                    </Badge>
                </div>
                {/* Name, rating, reviews */}
                <h1 className="text-3xl font-extrabold mb-1 leading-tight">{product.name}</h1>
                <div className="flex items-center gap-2 mb-2">
                    <span className="flex items-center text-yellow-500">
                        {Array.from({ length: 5 }).map((_, i) => (
                            <FaStar
                                key={i}
                                className={
                                    i < Math.round(Number(avgRating))
                                        ? 'text-yellow-500'
                                        : 'text-gray-300'
                                }
                            />
                        ))}
                    </span>
                    <span className="font-semibold text-lg text-gray-800 ml-2">{avgRating}</span>
                    <span className="text-gray-500 text-sm">({product?.reviews?.length} reviews)</span>
                </div>
                {/* Price */}
                <div className="text-3xl font-bold text-gray-900 mb-2">${product.price.toFixed(2)}</div>
                {/* Description */}
                <div className="text-gray-700 mb-4 text-base leading-relaxed">
                    {product.description}
                </div>
                {/* Color selection */}
                <div className="mb-4">
                    <div className="font-semibold mb-1">Color(s)</div>
                    <div className="flex gap-4 ">
                        {Array.from(
                            new Map(product.product_variants.map(v => [v.color_id, v])).values()
                        ).map(variant => {
                            const colorObj = colors.find(c => c.color_code === variant.color_id)
                            return (
                                <button
                                    key={variant.color_id}
                                    className={`w-16 h-16 rounded-full border-1 flex items-center justify-center shadow-md transition-all duration-200 p-0 focus:outline-none bg-white hover:scale-105 active:scale-95 ${selectedVariant.color_id === variant.color_id
                                        ? ' ring-primary border-primary'
                                        : 'border-gray-300 hover:border-primary'
                                        }`}
                                    onClick={() => handleVariantSelect(variant)}
                                    aria-label={colorObj?.name || variant.color_id}
                                >
                                    {colorObj?.image ? (
                                        <Image width={64} height={64} src={PRODUCT_IMAGE_URLS + colorObj.image} alt={colorObj.name} className="rounded-full object-cover w-14 h-14" />
                                    ) : (
                                        <span
                                            className="rounded-full w-14 h-14 block"
                                            style={{ backgroundColor: colorObj?.color_code || '#ccc' }}
                                        />
                                    )}
                                </button>
                            )
                        })}
                    </div>
                </div>
                {/* Quantity selector */}
                <div className="mb-4 flex items-center gap-4">
                    <div className="font-semibold">Quantity</div>
                    <div className="flex items-center border rounded overflow-hidden">
                        <button
                            className="px-3 py-1 text-lg font-bold text-gray-700 hover:bg-gray-100"
                            onClick={() => handleQuantityChange(-1)}
                            disabled={quantity === 1}
                        >-</button>
                        <span className="px-4 py-1 text-lg font-semibold bg-white">{quantity}</span>
                        <button
                            className="px-3 py-1 text-lg font-bold text-gray-700 hover:bg-gray-100"
                            onClick={() => handleQuantityChange(1)}
                            disabled={quantity === 5}
                        >+</button>
                    </div>
                    <span className="text-gray-500 text-sm ml-2">5 available</span>
                </div>
                {/* Tabs */}
                <div className="mt-6">
                    <div className="flex gap-2 border-b mb-4">
                        {TABS.map(tab => (
                            <button
                                key={tab.key}
                                className={`py-2 px-4 text-base font-semibold border-b-2 transition-colors duration-150 ${activeTab === tab.key
                                    ? 'border-gray-900 text-gray-900'
                                    : 'border-transparent text-gray-500 hover:text-gray-900'
                                    }`}
                                onClick={() => setActiveTab(tab.key)}
                            >
                                {tab.label}
                                {tab.key === 'reviews' && (
                                    <span className="ml-1 text-xs text-gray-500">({product?.reviews?.length})</span>
                                )}
                            </button>
                        ))}
                    </div>
                    {/* Tab content */}
                    {activeTab === 'features' && (
                        <ul className="list-disc pl-6 text-gray-700 space-y-1">
                            {product.product_features && product.product_features.length > 0 ? (
                                product.product_features.map((feature: ProductFeature, idx: number) => (
                                    <li key={idx}>{feature.name && <span className="font-medium">{feature.name}: </span>}{feature.description}</li>
                                ))
                            ) : (
                                <li>No features listed.</li>
                            )}
                        </ul>
                    )}
                    {activeTab === 'specs' && (
                        <div className="grid grid-cols-2 gap-x-6 gap-y-2 text-base text-gray-500">
                            <div className="flex flex-col">
                                <span className="font-semibold text-lg">Length</span>
                                <span className="text-gray-900 text-xl">{product.dimensions.length} mm</span>
                            </div>
                            <div className="flex flex-col">
                                <span className="font-semibold text-lg">Width</span>
                                <span className="text-gray-900 text-xl">{product.dimensions.width} mm</span>
                            </div>
                            <div className="flex flex-col">
                                <span className="font-semibold text-lg">Height</span>
                                <span className="text-gray-900 text-xl">{product.dimensions.height} mm</span>
                            </div>
                            {product.dimensions.depth && (
                                <div className="flex flex-col">
                                    <span className="font-semibold text-lg">Depth</span>
                                    <span className="text-gray-900 text-xl">{product.dimensions.depth} mm</span>
                                </div>
                            )}
                            {product.dimensions.weight && (
                                <div className="flex flex-col">
                                    <span className="font-semibold text-lg">Weight</span>
                                    <span className="text-gray-900 text-xl">{product.dimensions.weight} lbs</span>
                                </div>
                            )}
                        </div>
                    )}
                    {activeTab === 'shipping' && (
                        <div className="text-gray-700 text-base">
                            <div>Free nationwide shipping in Zimbabwe.</div>
                            <div>14 day returns. See our Shipping & Returns policy for more info.</div>
                        </div>
                    )}
                    {activeTab === 'reviews' && (
                        <div>
                            {/* Star filter */}
                            <div className="flex items-center gap-2 mb-4">
                                <span className="text-sm text-gray-600">Filter by:</span>
                                {[5, 4, 3, 2, 1].map(star => (
                                    <button
                                        key={star}
                                        className={`px-2 py-1 rounded-full border text-xs font-medium ${starFilter === star ? 'bg-gray-900 text-white border-gray-900' : 'bg-white text-gray-900 border-gray-300 hover:bg-gray-100'}`}
                                        onClick={() => setStarFilter(starFilter === star ? null : star)}
                                    >
                                        {star}★
                                    </button>
                                ))}
                            </div>
                            {/* Reviews list */}
                            {paginatedReviews && paginatedReviews.length > 0 ? (
                                paginatedReviews.map((review: ProductReview, idx: number) => (
                                    <div key={idx} className="mb-4 p-4 border rounded bg-white/80 shadow-sm">
                                        <div className="flex items-center mb-1">
                                            <span className="font-semibold">{review.title}</span>
                                            <span className="ml-2 text-yellow-500">
                                                {Array.from({ length: 5 }).map((_, i) => (
                                                    <FaStar key={i} className={i < review.rating ? 'text-yellow-500' : 'text-gray-300'} />
                                                ))}
                                            </span>
                                        </div>
                                        <div className="text-gray-700">{review.description}</div>
                                    </div>
                                ))
                            ) : (
                                <div className="text-gray-500">No reviews found.</div>
                            )}
                            {/* Pagination */}
                            <div className="flex gap-2 mt-4 items-center">
                                <button
                                    disabled={page === 1}
                                    onClick={() => setPage(page - 1)}
                                    className="px-3 py-1 border rounded disabled:opacity-50"
                                >Previous</button>
                                <span className="text-sm">Page {page} of {maxPage}</span>
                                <button
                                    disabled={page === maxPage}
                                    onClick={() => setPage(page + 1)}
                                    className="px-3 py-1 border rounded disabled:opacity-50"
                                >Next</button>
                            </div>
                        </div>
                    )}
                </div>
                {/* Add to Cart */}
                <Button
                    size="lg"
                    className="w-full bg-gray-900 text-white font-bold text-lg py-3 rounded-lg hover:bg-gray-800 transition-colors mt-6"
                    onClick={handleAddToCart}
                >
                    Add to Cart
                </Button>
            </div>
            {/* Floating WhatsApp Button */}
            <div className="fixed bottom-8 right-8 z-50">
                <button
                    onClick={handleWhatsAppClick}
                    className="w-16 h-16 rounded-full bg-green-600 hover:bg-green-700 flex items-center justify-center shadow-xl text-white text-3xl transition-transform duration-200 hover:scale-110 focus:outline-none"
                    aria-label="Chat on WhatsApp"
                >
                    <FaWhatsapp className="w-8 h-8" />
                </button>
            </div>
        </div>
    )
}



