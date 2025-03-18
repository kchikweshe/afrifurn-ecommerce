import { FilterParams } from "@/types";
import { CategoryProducts } from "@/types";
import { useState, useEffect, useCallback } from "react";
import { productService } from "@/services/product.service";

/**
 * Custom hook to filter and fetch category products based on filter parameters
 * @param initialParams Initial filter parameters to use
 * @returns Object containing:
 *  - categoryProducts: The filtered products data
 *  - loading: Boolean indicating if fetch is in progress
 *  - error: Error object if fetch fails
 *  - setParams: Function to update filter parameters
 *  - setCategoryProducts: Function to directly update category products
 */
export function useFilterCategoryProducts(initialParams: FilterParams) {
  const [params, setParams] = useState<FilterParams>(initialParams);
  const [categoryProducts, setCategoryProducts] = useState<CategoryProducts | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      setError(null);

      try { 
        const data = await productService.filterCategoryProducts(params);
        setCategoryProducts(data);
      } catch (error) {
        console.error('Error filtering products:', error);
        setError(error as Error);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [params]);

  return { categoryProducts, loading, error, setParams, setCategoryProducts };
}

/**
 * Generic hook to filter any collection type with the product service
 * @template T The type of data in the collection
 * @param doFetch Optional boolean to control initial fetch (defaults to false)
 * @returns Object containing:
 *  - data: Array of filtered items
 *  - loading: Boolean indicating if fetch is in progress
 *  - error: Error object if fetch fails
 *  - filterCollection: Function to trigger filtering with new parameters
 */
export function useFilterCollection<T>(doFetch: boolean = false) {
  const [data, setData] = useState<T[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<Error | null>(null);

  const filterCollection = useCallback(async (collection: string, params: FilterParams) => {
    setLoading(true);
    setError(null);

    try {
      const response = await productService.filterProducts(params);
      setData(response as T[]);
    } catch (error) {
      console.error('Error fetching filtered data', error);
      setError(error as Error);
    } finally {
      setLoading(false);
    }
  }, []);

  return { data, loading, error, filterCollection };
} 