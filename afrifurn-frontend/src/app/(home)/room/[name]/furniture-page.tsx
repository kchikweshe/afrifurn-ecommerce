'use client'
import { useState, useEffect } from 'react'

import { useFilterCollection } from '@/hooks/useFilterCollection'
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import ProductSkeleton from '@/ui/product-skeleton'
import { CategorySection } from '@/components/CategorySection'
import { CategoryProducts, Level2Category, Product } from '@/types'
import ErrorState from './ErrorState'
import { Link } from 'lucide-react'
import { Carousel, CarouselItem, CarouselContent, CarouselPrevious, CarouselNext } from '@/components/ui/carousel'
import { Button } from '@/components/ui/button'
import { AspectRatio } from "@radix-ui/react-aspect-ratio";
import Image from "next/image";
import { PRODUCT_IMAGE_URLS, PUBLIC_URL } from '@/data/urls'

// Updated carousel items with Ikea-style messaging
const carouselItems = [
    {
        image: "/living.jpg",
        title: "Create a home that's you",
        description: "Affordable solutions for better living",
        link: "/rooms/living-room"
    },
    {
        image: "/f2.png",
        title: "Summer sale",
        description: "Up to 50% off selected items",
        link: "/offers"
    },
    {
        image: "/wide.png",
        title: "New lower price",
        description: "Making sustainable living more affordable",
        link: "/new-arrivals"
    }
]
interface FurniturePageProps {
    shortName: string
    title: string
    categories: Array<Level2Category>
}

export default function FurniturePage({ shortName, title, categories }: FurniturePageProps) {
    const [activeCategory, setActiveCategory] = useState<string>(categories[0]?.name || '')
    const { data: products, loading, error, filterCollection } = useFilterCollection<Product>()
    const [isDelayedLoading, setIsDelayedLoading] = useState(true)

    useEffect(() => {
        if (activeCategory && shortName) {
            setIsDelayedLoading(true)
            filterCollection('products/by-level-two-category', {
                short_name: activeCategory
            })
        }
    }, [activeCategory, shortName, filterCollection])

    useEffect(() => {
        if (!loading) {
            const timer = setTimeout(() => {
                setIsDelayedLoading(false)
            }, 300)
            return () => clearTimeout(timer)
        }
    }, [loading])

    const handleTabChange = (value: string) => {
        setActiveCategory(value)
    }

    if (error) {
        return <ErrorState message={error.message} />
    }

    const renderContent = () => {
        if (loading || isDelayedLoading) {
            return (
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
                    {[...Array(8)].map((_, index) => (
                        <ProductSkeleton key={index} />
                    ))}
                </div>
            );
        }

        const categoryProducts: CategoryProducts = {
            category_name: activeCategory,
            products: products || []
        };

        return <CategorySection category={categoryProducts} />;
    };

    return (
        <div>
            {/* <header className="mb-8">
                <h1 className="text-4xl font-bold text-center">{title}</h1>
            </header> */}
            <section className="relative ">
                <Carousel className="w-full h-full">
                    <CarouselContent className="h-full">
                        {categories.map((item, index) => (
                            <CarouselItem key={index} className="h-full">
                                <div className="relative h-[70vh]">
                                    <AspectRatio ratio={16 / 9} className="hidden md:block h-[70vh]">
                                        <Image
                                            src={`${PRODUCT_IMAGE_URLS}${item.images[0]}`}
                                            alt={item.name}
                                            fill
                                            className="object-cover"
                                            priority
                                            sizes="(max-width: 768px) 100vw, 100vw"
                                            quality={100}
                                        />
                                    </AspectRatio>
                                    {/* Mobile-specific image container */}
                                    <div className="block md:hidden h-full">
                                        <AspectRatio className="h-full"></AspectRatio>
                                        <Image
                                            src={`${PRODUCT_IMAGE_URLS}${item.images[0]}`}
                                            alt={item.name}
                                            fill
                                            className="object-cover"
                                            priority
                                        />
                                    </div>
                                    <div className="absolute inset-0 flex items-center justify-start bg-black/10">
                                        <div className="text-left text-black max-w-xl px-8 md:px-16 py-8 bg-white/80 ml-0 md:ml-16 transform transition-all duration-700">
                                            <h2 className="text-2xl md:text-4xl font-bold mb-2 md:mb-4">{item.name}</h2>
                                            <p className="text-base md:text-xl mb-4 md:mb-6">{item.description}</p>
                                           
                                        </div>
                                    </div>
                                </div>
                            </CarouselItem>
                        ))}
                    </CarouselContent>
                    <CarouselPrevious className="left-2 md:left-8 h-8 w-8 md:h-10 md:w-10 bg-white text-black border-none rounded-full" />
                    <CarouselNext className="right-2 md:right-8 h-8 w-8 md:h-10 md:w-10 bg-white text-black border-none rounded-full" />
                </Carousel>
            </section>
            <section className="mt-8 px-8">
                <Tabs
                    defaultValue={activeCategory}
                    className="w-full"
                    onValueChange={handleTabChange}
            >
                <TabsList className="w-full justify-start  bg-gray-100 rounded-lg overflow-x-auto flex-nowrap">
                    {categories?.map((category) => (
                        <TabsTrigger
                            key={category?._id}
                            value={category?.name}
                            className=" w-full text-xl"
                        >
                            {category?.name}
                        </TabsTrigger>
                    ))}
                </TabsList>

                <TabsContent
                    value={activeCategory}
                    className="mt-4 focus-visible:outline-none focus-visible:ring-0"
                >
                    {renderContent()}
                </TabsContent>
                </Tabs>
                </section>
        </div>
    )
}
