'use client'

import { Suspense, useContext, useEffect, useState } from 'react'
import Image from 'next/image'
import { Tabs, TabsList, TabsTrigger, TabsContent } from "@/components/ui/tabs"
import { Card, CardContent, CardFooter } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { ShoppingCart, ChevronRight, Heart } from 'lucide-react'
import { CategoryProducts, Currency, FilterParams, Level1Category, Level2Category, Product } from '@/types'
import { useFilterCategoryProducts } from '@/hooks/useFilterCategoryProducts'

import { PRODUCT_IMAGE_URLS } from '@/data/urls'
import Link from 'next/link'
import ProductGridSkeleton from './skeleton'
import { motion, AnimatePresence } from 'framer-motion'

import { DataContext } from '@/data/data.context'
import { useFetchAll } from '@/hooks/useFetch'
const ProductCard = ({ product }: { product: Product }) => {
    const state = useContext(DataContext)
    if(!state){
        return <div>State is null</div>
    }
    const {currencies}=state
    const getCurrencySymbol = (currency: string) => {
        const currencyData = currencies.find((c: Currency) => c.code === currency);
        return currencyData ? currencyData.symbol : currency;
    };
    return (
        <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            transition={{ duration: 0.3 }}
        >
            <div className="relative h-[270px] w-full">
                <Image
                    src={PRODUCT_IMAGE_URLS + product.product_variants[0].images[0]}
                    alt={product.name}
                    width={270}
                    height={270}
                    className="h-[270px] w-full rounded-[16px] object-cover"
                />
                <div className="absolute inset-0 m-auto flex h-max flex-col items-center p-2">
                    <div className="flex w-full max-w-[254px] flex-col items-center justify-center pb-[218px] pl-[218px] md:pb-5 md:pl-5">
                        <Button
                            size="icon"
                            variant="ghost"
                            className="h-[36px] w-[36px] rounded-full bg-black-900_4c transition-colors hover:bg-black-900_6c"
                        >
                            <Heart className="h-5 w-5 text-white" />
                        </Button>
                    </div>
                </div>
            </div>
            <div className="flex w-full flex-col items-center gap-[11px] self-stretch px-3">
                <div className="mx-auto flex w-full max-w-[246px] items-center justify-between gap-5 self-stretch">
                    <div className="flex flex-col items-start gap-[3px]">
                        <p className="text-[16px] font-normal text-black-900_01">{product.name}</p>
                        <p className="text-[14px] font-normal text-gray-600_01">
                            {product.description.length > 20
                                ? `${product.description.substring(0, 20)}...`
                                : product.description}
                        </p>
                    </div>
                    <Button
                        size="icon"
                        variant="outline"
                        className="h-[36px] w-[36px] rounded-lg border-gray-200_01 transition-colors hover:bg-gray-100"
                    >
                        <ShoppingCart className="h-5 w-5 text-gray-600_01" />
                    </Button>
                </div>
                <div className="mx-auto flex w-full max-w-[246px] items-center justify-between gap-5 self-stretch">
                    <div className="flex flex-wrap items-center gap-1">
                        <h6 className="text-[16px] font-semibold text-black-900_01">
                            {getCurrencySymbol(product.currency)}{product.price.toFixed(2)}
                        </h6>
                        {product.discount && (
                            <p className="text-[14px] font-normal text-gray-600_01 line-through">
                                {getCurrencySymbol(product.currency)}
                                {(product.price / (1 - product.discount / 100)).toFixed(2)}
                            </p>
                        )}
                    </div>  
                    {product.discount && (
                        <p className="text-[14px] font-normal text-green-900">
                            {product.discount}% OFF
                        </p>
                    )}
                </div>
            </div>
        </motion.div>
    )
}

export default function CategoryProductsShowcase({ category }: { category: Level1Category }) {
    const { data: level2Categories, error: categoriesError, loading: categoriesLoading } = useFetchAll<Level2Category>(`categories/level-2/${category?._id}`)
    const level2CategoriesArray = Array.isArray(level2Categories) ? level2Categories : [level2Categories]
    
    const initialParams: FilterParams = {
        name: category?.name,
        page: 1,
        page_size: 10
    }

    const { categoryProducts, loading: productsLoading, error: productsError, setParams } = useFilterCategoryProducts(initialParams)
    const [activeTab, setActiveTab] = useState<string>('')

    useEffect(() => {
        if (level2CategoriesArray?.length > 0) {
            setActiveTab(level2CategoriesArray.at(0)?.name || '')
            setParams(prevParams => ({ ...prevParams, name: level2CategoriesArray.at(0)?.name || '' }))
        }
    }, [level2Categories, setParams])

    if(!level2CategoriesArray){
        return <div>No categories found</div>
    }

    const handleTabChange = (tabValue: string) => {
        setActiveTab(tabValue)
        setParams(prevParams => ({ ...prevParams, name: tabValue }))
    }

    return (
        <div className="flex flex-col items-center gap-6 min-h-screen bg-gray-50">
            <div className="px-4 mx-auto flex w-full max-w-6xl flex-col items-center md:px-5 py-8">
                <div className="gap-[3px] flex flex-col items-center">
                    <h2 className="sm:text-[38px] md:text-[44px] text-[48px] font-medium text-black-900 text-center">
                        {category?.name}
                    </h2>
                    <p className="text-[16px] font-normal text-gray-600 text-center">
                        Crafted with love specially for you
                    </p>
                </div>
            </div>

            <div className="mx-auto w-full max-w-6xl px-4 md:px-5 flex-grow">
                <Tabs defaultValue={level2CategoriesArray.at(0)?.name || ''} onValueChange={handleTabChange} className="w-full">
                    <div className="flex items-center justify-between gap-4 md:flex-col mb-6">
                        <TabsList className="w-full bg-transparent">
                            {level2CategoriesArray.map((subCategory) => (
                                <TabsTrigger
                                    key={subCategory?.name}
                                    value={subCategory?.name ?? ''}
                                    className="flex-1 text-lg font-medium data-[state=active]:text-lime-900 data-[state=active]:border-b-2 data-[state=active]:border-lime-900 transition-all duration-300 ease-in-out"
                                >
                                    {subCategory?.name}
                                </TabsTrigger>
                            ))}
                        </TabsList>
                        <Link href={`/category/${activeTab}`}>
                            <Button variant="outline" className="rounded-[15px] text-lime-900 border-lime-900 hover:bg-lime-50 transition-colors">
                                View all
                                <ChevronRight className="w-4 h-4 ml-2" />
                            </Button>
                        </Link>

                    </div>

                    <AnimatePresence mode="wait">
                        <motion.div
                            key={activeTab}
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            exit={{ opacity: 0, y: -20 }}
                            transition={{ duration: 0.3 }}
                        >
                            <TabsContent value={activeTab} className="mt-0">
                                <Suspense fallback={<ProductGridSkeleton />}>
                                    <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
                                        {categoryProducts?.products.map((product) => (
                                            <Link key={product._id} href={`/products/${product.short_name}`} className="transform transition-transform hover:scale-105">
                                                <ProductCard product={product} />
                                            </Link>
                                        ))}
                                    </div>
                                </Suspense>
                            </TabsContent>
                        </motion.div>
                    </AnimatePresence>
                </Tabs>
            </div>
        </div>
    )
} 