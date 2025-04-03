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
import { useRouter } from 'next/navigation'
import { useToast } from '@/hooks/use-toast'
import { Product, ProductVariant } from '@/types'
import type { CartItem } from '@/types/cart'
import { useCart } from '@/context/cart/use-cart'
import { ProductGallery } from '@/components/products/product-gallery'
import { ProductDetails } from '@/components/products/product-details'
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { FaWhatsapp } from "react-icons/fa"

interface ProductOverviewProps {
    /** Product object containing all product details */
    product: Product;
}

export default function ProductOverview({ product }: ProductOverviewProps) {
    /** Currently selected product variant */
    
    console.debug("Debug product", product)
    const [selectedVariant, setSelectedVariant] = useState(product.product_variants[0])
    
    /** Index of currently displayed main image */
    const [mainImage, setMainImage] = useState(0)
    
    /** Controls visibility of "Added to Cart" indicator */
    const [showAddedBadge, setShowAddedBadge] = useState(false)

    const { toast } = useToast()
    const { addToCart } = useCart()

    /**
     * Handles selection of a new product variant
     * @param variant - The selected product variant
     */
    const handleVariantSelect = useCallback((variant: ProductVariant) => {
        // Find the variant with matching color_id to ensure we get the right images
        const targetVariant = product.product_variants.find(v => v.color_id === variant.color_id)
        if (targetVariant) {
            setSelectedVariant(targetVariant)
            setMainImage(targetVariant.images.findIndex(img => img === targetVariant.images[0])) // Reset to first image when changing variant
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
                quantity: 1
            }

            addToCart(cartItem)  
            setShowAddedBadge(true)  

            toast({
                title: "Success",
                description: "Added to cart successfully!"
            })

            // Hide the badge after 2 seconds
            setTimeout(() => {
                setShowAddedBadge(false)
            }, 2000)
        } catch (error) {
            toast({
                title: "Error",
                description: "Failed to add item to cart",
                variant: "destructive"
            })
        }
    }, [product, selectedVariant, discountedPrice, toast, addToCart])

    return (
        <div className="  py-8">
            <div className="flex flex-col gap-8">
                {/* <div className="block lg:hidden">
                    <h1 className="text-3xl font-bold mb-2">{product.name}</h1>
                    {product.is_new && <Badge>New</Badge>}
                </div>
                 */}
                <div className="lg:w-full py-6 px-3 shadow-md  flex flex-col lg:flex-row gap-20">
                  <div className="md:w-1/2">
                  <ProductGallery
                        product={product}
                        selectedVariant={selectedVariant}
                        mainImage={mainImage}
                        setMainImage={setMainImage}
                    />
                  </div>
                
                    <ProductDetails
                        product={product}
                        selectedVariant={selectedVariant}
                        setSelectedVariant={handleVariantSelect}
                        onAddToCart={handleAddToCart}
                        showAddedBadge={showAddedBadge}
                        setMainImage={setMainImage}
                    />
                </div>
            </div>
        </div>
    )
}

          
 