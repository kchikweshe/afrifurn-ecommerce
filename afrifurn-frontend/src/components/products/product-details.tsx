'use client'

import { Button } from "@/components/ui/button"
import { Card, CardContent } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { ShoppingCart, Heart } from "lucide-react"
import { FaWhatsapp } from "react-icons/fa"
import {  Product, ProductVariant } from '@/types'
import { useCallback, useContext } from 'react'
import { DataContext } from "@/data/data.context"
import { PRODUCT_IMAGE_URLS } from "@/data/urls"

interface ProductDetailsProps {
  product: Product
  selectedVariant: ProductVariant
  setSelectedVariant: (variant: ProductVariant) => void
  onAddToCart: () => void
  showAddedBadge: boolean
  setMainImage: (index: number) => void
}

export function ProductDetails({
  product,
  selectedVariant,
  setSelectedVariant,
  onAddToCart,
  showAddedBadge}: ProductDetailsProps) {
  const state = useContext(DataContext)
  
  // Move all hooks before any conditional returns
  const getColorName = useCallback((colorId: string | null) => {
    if (!colorId) return 'Unknown'
    const color = state?.colors.find(c => c.color_code === colorId)
    console.log("Color:",color)
    return color ? color.name : colorId
  }, [state?.colors])

  const getCurrencySymbol = useCallback((currencyCode: string) => {
    console.log("Code:",currencyCode)
    console.log("Currencies: ",state?.currencies)
    const currency = state?.currencies.find(c => c.code === currencyCode)
    console.log("Code:",currency)
    return currency ? currency.symbol : currencyCode
  }, [state?.currencies])

   const getMaterialName = useCallback((materialId: string | null) => {
    if (!materialId) return 'Unknown'
    const material = state?.materials.find(m => m._id === materialId)
    return material ? material.name : materialId
  }, [state?.materials])

  const handleWhatsAppClick = useCallback(() => {
    const phoneNumber = "+263778588495"
    const productUrl = window.location.href
    const message = `Hi, I'm interested in ${product.name} (${getColorName(selectedVariant.color_id)}) priced at ${product.currency}$ ${(product.price * (1 - (product.discount || 0) / 100)).toFixed(2)}.\n\n${productUrl}`
    const whatsappUrl = `https://wa.me/${phoneNumber}?text=${encodeURIComponent(message)}`
    window.open(whatsappUrl, '_blank')
  }, [product, selectedVariant, getColorName])

  if(!state){
    return <div>
      State is null
    </div>
  }
  const{currencies,colors,materials}=state

  return (
    <div className="lg:w-1/2 space-y-6 container mx-auto px-4">
      {/* Product Header Section */}
      <div className="border-b pb-4">
        <h1 className="text-3xl sm:text-4xl font-bold mb-2">{product.name}</h1>
        <div className="flex items-center gap-2 mb-3">
          {product.is_new && <Badge className="bg-emerald-500 hover:bg-emerald-600">New</Badge>}
          {product.discount && product.discount > 0 && (
            <Badge className="bg-red-500 hover:bg-red-600">{product.discount}% OFF</Badge>
          )}
        </div>
        
        <p className="text-2xl lg:text-3xl font-bold text-primary flex items-center">
          {getCurrencySymbol(product.currency.toString())}
          {(product.price * (1 - (product.discount || 0) / 100)).toFixed(2)}
          {product.discount && product.discount > 0 && (
            <span className="text-sm text-muted-foreground line-through ml-2">
              {getCurrencySymbol(product.currency.toString())}
              {product.price.toFixed(2)}
            </span>
          )}
        </p>
      </div>

      {/* Colors Section with improved layout */}
      <div className="py-4">
        <h2 className="text-lg font-semibold mb-3">Colors</h2>
        <div className="flex flex-wrap gap-4">
          {product.product_variants.map((variant) => {
            const variantColor = colors.find(c => c.color_code === variant.color_id)
            return (
              <button
                key={variant.color_id}
                className={`
                  group relative w-12 h-12 rounded-full transition-all duration-200
                  ${selectedVariant.color_id === variant.color_id 
                    ? 'ring-2 ring-primary ring-offset-2' 
                    : 'hover:ring-1 hover:ring-primary/50 hover:ring-offset-1'
                  }
                  shadow-sm
                `}
                style={{ 
                  backgroundImage: `url(${PRODUCT_IMAGE_URLS+variantColor?.image})`,
                  backgroundSize: 'cover',
                  backgroundPosition: 'center'
                }}
                onClick={() => setSelectedVariant(variant)}
                aria-label={getColorName(variant.color_id)}
              >
                {selectedVariant.color_id === variant.color_id && (
                  <span className="absolute inset-0 flex items-center justify-center">
                    <span className="w-5 h-5 rounded-full bg-white/30 flex items-center justify-center">
                      <svg 
                        xmlns="http://www.w3.org/2000/svg" 
                        className="h-3 w-3 text-white" 
                        viewBox="0 0 20 20" 
                        fill="currentColor"
                      >
                        <path 
                          fillRule="evenodd" 
                          d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" 
                          clipRule="evenodd" 
                        />
                      </svg>
                    </span>
                  </span>
                )}
                <span className="absolute -bottom-6 left-1/2 -translate-x-1/2 whitespace-nowrap text-xs font-medium opacity-0 group-hover:opacity-100 transition-opacity">
                  {getColorName(variant.color_id)}
                </span>
              </button>
            )
          })}
        </div>
      </div>

      {/* Description Card */}
      <div className="bg-gray-50 p-4 rounded-lg border border-gray-100 shadow-sm">
        <h2 className="text-lg font-semibold mb-2">Description</h2>
        <p className="text-gray-700 leading-relaxed">{product.description}</p>
      </div>

      {/* Product Details Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
        <div className="bg-gray-50 p-4 rounded-lg border border-gray-100 shadow-sm">
          <h2 className="text-lg font-semibold mb-2">Material</h2>
          <p className="text-gray-700 flex items-center">
            <span className="mr-2 text-primary">
              <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4" viewBox="0 0 20 20" fill="currentColor">
                <path fillRule="evenodd" d="M11.3 1.046A1 1 0 0112 2v5h4a1 1 0 01.82 1.573l-7 10A1 1 0 018 18v-5H4a1 1 0 01-.82-1.573l7-10a1 1 0 011.12-.38z" clipRule="evenodd" />
              </svg>
            </span>
            {getMaterialName(product!.material!.toString())}
          </p>
        </div>

        <Card className="bg-gray-50 shadow-sm border-gray-100">
          <CardContent className="p-4">
            <h2 className="text-lg font-semibold mb-2">Dimensions</h2>
            <div className="grid grid-cols-2 gap-3 text-sm">
              <p className="flex items-center text-gray-700"><span className="font-medium mr-1">Length:</span> {product.dimensions.length}mm</p>
              <p className="flex items-center text-gray-700"><span className="font-medium mr-1">Width:</span> {product.dimensions.width}mm</p>
              <p className="flex items-center text-gray-700"><span className="font-medium mr-1">Height:</span> {product.dimensions.height}mm</p>
              {product.dimensions.depth && <p className="flex items-center"><span className="font-medium mr-1">Depth:</span> {product.dimensions.depth}mm</p>}
              {product.dimensions.weight && <p className="flex items-center"><span className="font-medium mr-1">Weight:</span> {product.dimensions.weight} lbs</p>}
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Action Buttons */}
      <div className="flex flex-col gap-3 pt-4 sticky bottom-0 bg-white pb-4 border-t mt-4">
        <div className="flex gap-3">
          <Button 
            size="lg" 
            className="flex-1 relative hover:scale-102 transition-transform" 
            onClick={onAddToCart}
          >
            <ShoppingCart className="mr-2 h-5 w-5" />
            {showAddedBadge && (
              <span className="absolute -top-2 -right-2 bg-primary text-primary-foreground rounded-full w-5 h-5 flex items-center justify-center text-xs animate-pulse">
                +1
              </span>
            )}
            Add to Cart
          </Button>
          <Button 
            size="lg" 
            variant="outline" 
            className="hover:bg-pink-50 hover:text-pink-600 hover:border-pink-200 transition-colors"
          >
            <Heart className="h-5 w-5" />
          </Button>
        </div>
        <Button 
          size="lg"
          onClick={handleWhatsAppClick}
          className="w-full flex items-center justify-center gap-2 bg-green-600 hover:bg-green-700 text-white hover:scale-102 transition-transform shadow-md"
        >
          <FaWhatsapp className="h-5 w-5" />
          Chat on WhatsApp
        </Button>
      </div>
    </div>
  )
}
