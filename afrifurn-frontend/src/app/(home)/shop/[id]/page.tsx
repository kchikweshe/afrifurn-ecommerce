import React from "react";

import { FilterParams } from '@/types';
import Shop from "./shop";
import { productService } from "@/services/product.service";




export default async function Page(props0: { params: Promise<{ id: string }> }) {
  const params = await props0.params;
  const filterParams: FilterParams = {
    category: params.id
  }
  console.debug(filterParams)
  console.debug("Product ID: ", params.id)
  try {
    // Fetch product data based on productId

    const data = await productService.filterProducts(filterParams);
    if (data === undefined) {
      console.error('Error fetching product data:');
  
    }
 
    else {
      console.debug("Data: ", data)

      return <Shop data={data} initialFilters={filterParams} />

    }

  } catch (error) {
    console.error('Error fetching product data:', error);
    return {
      props: {
        product: null,
      },
    };
  }
}