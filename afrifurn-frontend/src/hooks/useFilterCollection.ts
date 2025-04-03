import { FilterParams } from  "@/types";
import { AxiosResponse } from "axios";
import { useState, useCallback } from "react";
import { productMicroService } from "@/config/api.config";

export function useFilterCollection<T>(doFetch:boolean=false) {
    const [data, setData] = useState<T[]>([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<Error | null>(null);
  
    const filterCollection = useCallback(async (collection: string, params: FilterParams) => {
      setLoading(true);
      setError(null);
      const queryParams = new URLSearchParams();
  
      if (params.start_price !== undefined) queryParams.append('start_price', params.start_price.toString());
      if (params.end_price !== undefined) queryParams.append('end_price', params.end_price.toString());
      if (params.colors) queryParams.append('colors', JSON.stringify(params.colors));
      if (params.width !== undefined) queryParams.append('width', params.width.toString());
      if (params.length !== undefined) queryParams.append('length', params.length.toString());
      if (params.depth !== undefined) queryParams.append('depth', params.depth.toString());
      if (params.height !== undefined) queryParams.append('height', params.height.toString());
      if (params.materials !== undefined) queryParams.append('materials', JSON.stringify(params.materials));
      if (params.category !== undefined) queryParams.append('category', params.category);
      if (params.page !== undefined) queryParams.append('page', params.page.toString());
      if (params.page_size !== undefined) queryParams.append('page_size', params.page_size.toString());
      if (params.sort_by) queryParams.append('sort_by', params.sort_by);
      if (params.name) queryParams.append('name', params.name);
      if (params.short_name) queryParams.append('short_name', params.short_name);
    
      if (params.sort_order !== undefined) queryParams.append('sort_order', params.sort_order.toString());
    
      const url = `${collection}/filter?${queryParams.toString()}`;
  
      try {
        const response: AxiosResponse<{data: T[]}> = await productMicroService.get(url);
        console.log("Input: \n",url,queryParams.entries,"Output:\n",response)
        const data = response.data.data || [];
        setData(data);
      } catch (error) {
        console.error('Error fetching filtered data', error);
        setError(error as Error);
      } finally {
        setLoading(false);
      }
    }, []);
  
    return { data, loading, error, filterCollection };
  }

