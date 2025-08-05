'use client'

import Image from 'next/image'
import { Product, ProductVariant } from '@/types'
import { PRODUCT_IMAGE_URLS } from '@/data/urls'
import { FaChevronLeft, FaChevronRight } from 'react-icons/fa'

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
  const hasMultipleImages = selectedVariant.images.length > 1;
  return (
    <div className="flex flex-col gap-4">
      {/* Main Image - Full width on mobile and desktop, taller on large screens */}
      <div className="relative shadow-lg border rounded-2xl border-gray-200 overflow-hidden bg-gradient-to-br from-gray-50 via-white to-gray-200 flex ">
        <div className=" overflow-hidden rounded-2xl border" />
        <Image
          src={PRODUCT_IMAGE_URLS + selectedVariant!.images[mainImage]}
          alt={`${product.name} - ${selectedVariant.color_id} - View ${mainImage + 1}`}
          width={800}
          height={800}
          className="rounded-2xl object-cover w-auto h-auto"        />
        {/* Left Arrow */}
        {hasMultipleImages && (
          <button
            className="absolute left-2 top-1/2 -translate-y-1/2 bg-white/80 hover:bg-white text-gray-700 rounded-full p-2 shadow z-30 disabled:opacity-50"
            onClick={() => setMainImage(mainImage - 1)}
            disabled={mainImage === 0}
            aria-label="Previous image"
          >
            <FaChevronLeft className="h-5 w-5" />
          </button>
        )}
        {/* Right Arrow */}
        {hasMultipleImages && (
          <button
            className="absolute right-2 top-1/2 -translate-y-1/2 bg-white/80 hover:bg-white text-gray-700 rounded-full p-2 shadow z-30 disabled:opacity-50"
            onClick={() => setMainImage(mainImage + 1)}
            disabled={mainImage === selectedVariant.images.length - 1}
            aria-label="Next image"
          >
            <FaChevronRight className="h-5 w-5" />
          </button>
        )}
      </div>

      {/* Thumbnails - Always below the main image, fill up horizontally */}
      <div className="flex gap-3 overflow-x-auto pb-2 justify-center w-full">
        {selectedVariant.images.map((img, index) => (
          <button
            key={index}
            className={`flex-shrink-0 w-24 h-24 md:w-28 md:h-28 lg:w-32 lg:h-32 rounded-lg overflow-hidden border transition-all duration-200 shadow-sm bg-white/80 hover:scale-105 hover:shadow-md ${
              index === mainImage ? 'ring-2 ring-primary border-primary scale-105' : 'border-gray-200'
            }`}
            onClick={() => setMainImage(index)}
            style={{ position: 'relative' }}
            aria-label={`Show image ${index + 1}`}
          >
            <div className="relative w-full h-full">
              <Image
                src={PRODUCT_IMAGE_URLS + img}
                alt={`${product.name} - ${selectedVariant.color_id} - Thumbnail ${index + 1}`}
                fill
                className="object-cover rounded-lg"
              />
            </div>
            {index === mainImage && (
              <span className="absolute inset-0 border-2 border-primary rounded-lg pointer-events-none" />
            )}
          </button>
        ))}
      </div>
    </div>
  )
}
