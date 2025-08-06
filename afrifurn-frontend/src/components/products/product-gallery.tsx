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
    <div className="flex flex-col gap-3 scale-[0.97] max-w-5xl mx-auto">
      {/* Main Image */}
      <div className="relative shadow-md border rounded-xl border-gray-200 overflow-hidden bg-gradient-to-br from-gray-50 via-white to-gray-200 flex justify-center">
        <Image
          src={PRODUCT_IMAGE_URLS + selectedVariant!.images[mainImage]}
          alt={`${product.name} - ${selectedVariant.color_id} - View ${mainImage + 1}`}
          width={720}
          height={720}
          className="rounded-xl object-contain max-h-[75vh] w-full"
        />
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
            className="absolute right-2 top-1/2 -translate-y-1/2 bg-white/80 hover:bg-white text-gray-700 rounded-full p-2 shadow z-30 disabled={mainImage === selectedVariant.images.length - 1}"
            onClick={() => setMainImage(mainImage + 1)}
            aria-label="Next image"
          >
            <FaChevronRight className="h-5 w-5" />
          </button>
        )}
      </div>

      {/* Thumbnails */}
      <div className="flex gap-2 md:gap-3 overflow-x-auto pb-1 justify-center w-full">
        {selectedVariant.images.map((img, index) => (
          <button
            key={index}
            className={`flex-shrink-0 w-20 h-20 md:w-24 md:h-24 rounded-lg overflow-hidden border transition-transform duration-150 shadow-sm hover:scale-105 hover:shadow-md ${
              index === mainImage
                ? 'ring-2 ring-primary border-primary scale-105'
                : 'border-gray-200'
            }`}
            onClick={() => setMainImage(index)}
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
          </button>
        ))}
      </div>
    </div>
  )
}
