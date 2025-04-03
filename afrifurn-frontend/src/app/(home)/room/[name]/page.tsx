import { fetchAll } from '@/data/data.fetcher'
import { Level2Category } from '@/types'
import React from 'react'
import FurniturePage from './furniture-page'

export default async function Page(props: { params: Promise<{ name: string }> }) {
    const params = await props.params;

    // fetch category
    let data = await fetchAll<Level2Category>("/categories/level-2/short-name/" + params.name)
    if (data) {
        console.log("Level 2 Categories \n", data)
    }

    return <FurniturePage shortName={params.name} title={params.name.toUpperCase().replace('-', ' ')} categories={data || []} />
}