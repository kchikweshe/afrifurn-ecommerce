import { Carousel } from "@/components/ui/carousel";
import React from 'react'
import Image from 'next/image'
import { Button } from '@/components/ui/button'
import { CategoryProducts } from "@/types";
import { ProductCard } from "@/components/ui/ProductCard";
interface CategoryProductsPageProps {
  categoryProducts: CategoryProducts
  carouselImages: string[]
}

export function CategoryProductsPage({ categoryProducts, carouselImages }: CategoryProductsPageProps) {
  return (
    <div className="container mx-auto px-4 py-8">
      <Carousel className="mb-8">
        {carouselImages.map((image, index) => (
          <Image
            key={index}
            src={image}
            alt={`${categoryProducts.category_name} furniture ${index + 1}`}
            width={1200}
            height={600}
            className="object-cover w-full h-[60vh]"
          />
        ))}
      </Carousel>

      <div className="mb-12 text-center">
        <h1 className="text-4xl font-bold mb-4">{categoryProducts.category_name} Furniture</h1>
        <p className="text-xl text-gray-600 max-w-3xl mx-auto">
          Discover our exquisite collection of {categoryProducts.category_name.toLowerCase()} furniture, 
          designed to elevate your space with style and comfort. From classic pieces to modern designs, 
          find the perfect additions to your home.
        </p>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
        {categoryProducts.products.map((product) => (
          <ProductCard key={product._id} product={product} />
        ))}
      </div>
    </div>
  )
}