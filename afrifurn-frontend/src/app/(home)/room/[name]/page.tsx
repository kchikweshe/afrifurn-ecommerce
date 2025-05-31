import { fetchAll } from '@/data/data.fetcher'
import { Level2Category } from '@/types'
import React from 'react'
import FurniturePage from './furniture-page'
import { categoryService } from '@/services/category.service';

export default async function Page(props: { params: Promise<{ name: string }> }) {
    const params = await props.params;

    // fetch category
    const level2Categories = await categoryService.getLevel2CategoriesByShortName(params.name)
    console.log("Level 2: ", level2Categories)
    if(!level2Categories){return}
    return <FurniturePage shortName={params.name} title={params.name.toUpperCase().replace('-', ' ')} categories={level2Categories} />
}