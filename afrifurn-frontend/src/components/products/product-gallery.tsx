'use client'

import Image from 'next/image'
import { Product, ProductVariant } from '@/types'
import { PRODUCT_IMAGE_URLS } from '@/data/urls'

interface ProductGalleryProps {
  product: Product
  selectedVariant: ProductVariant
  mainImage: number
  setMainImage: (index: number) => void
}

export function ProductGallery({
  product,
  selectedVariant,
  mainImage,
  setMainImage
}: ProductGalleryProps) {
  return (
    <div className="flex flex-col lg:flex-row gap-4">
      {/* Main Image - Full width on mobile, side by side on desktop */}
      <div className="order-1 lg:order-2 lg:flex-1 relative aspect-square">
        <Image
          src={PRODUCT_IMAGE_URLS + selectedVariant!.images[mainImage]}
          alt={`${product.name} - ${selectedVariant.color_id} - View ${mainImage + 1}`}
          fill
          className="object-cover rounded-lg"
          priority
        />
      </div>

      {/* Thumbnails - Horizontal scroll on mobile, vertical on desktop */}
      <div className="order-2 lg:order-1 flex lg:flex-col gap-2 overflow-x-auto lg:overflow-x-visible pb-2 lg:pb-0">
        {selectedVariant.images.map((img, index) => (
          <button
            key={index}
            className={`flex-shrink-0 w-20 h-20 rounded-md overflow-hidden ${
              index === mainImage ? 'ring-2 ring-primary' : ''
            }`}
            onClick={() => setMainImage(index)}
          >
            <Image
              src={PRODUCT_IMAGE_URLS + img}
              alt={`${product.name} - ${selectedVariant.color_id} - Thumbnail ${index + 1}`}
              width={80}
              height={80}
              className="object-cover"
            />
          </button>
        ))}
      </div>
    </div>
  )
}
