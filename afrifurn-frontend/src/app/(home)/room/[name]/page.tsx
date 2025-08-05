import { fetchAll } from '@/data/data.fetcher'
import { Level2Category } from '@/types'
import React from 'react'
import FurniturePage from './furniture-page'
import { categoryService } from '@/services/category.service';
import { Metadata } from 'next';
import { formatSubcategoryName } from './[subcategory]/page';

interface PageProps {
    params: { name: string };
}
// ✅ SEO Metadata Function
export async function generateMetadata(
    { params }: { params: Promise<{ shortName: string ,subcategory:string,name:string}> }

): Promise<Metadata> {


    const { name } = await params;

    const formattedName = formatSubcategoryName(name);
    const fullUrl = `https://afri-furn.co.zw/room/${name}`
    console.log(fullUrl)
    return {
        title: `${formattedName} | Afri Furn`,
        description: `Explore top-quality furniture in the ${formattedName} category. Shop modern designs, custom finishes, and fast delivery.`,
        openGraph: {
            title: `${formattedName} Furniture | Afri-Furn`,
            description: `Discover modern and stylish ${formattedName} furniture perfect for every room.`,
            url: fullUrl,
            type: 'website',
        },
        alternates: {
            canonical: fullUrl,
        },
    };
}
export default async function Page(props: { params: Promise<{ name: string }> }) {
    const params = await props.params;

    // fetch category
    const level2Categories = await categoryService.getLevel2CategoriesByShortName(params.name)
    return <FurniturePage shortName={params.name} title={params.name.toUpperCase().replace('-', ' ')} categories={level2Categories} />
}