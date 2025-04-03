import { useState, useEffect } from 'react';
import {  fetchAll } from '../data.fetcher';
import { Product, Level2Category, Level1Category, Currency, Material, Color } from '@/types';


function useFetchAllData( ) {
  const [products, setProducts] = useState<Product[]>([]);
  const [categories, setCategories] = useState<Level2Category[]>([]);
  const [parentCategories, setParentCategories] = useState<Level1Category[]>([]);

  const [currencies, setCurrencies] = useState<Currency[]>([]);
  const [colors, setColors] = useState<Color[]>([]);
  const [materials, setMaterial] = useState<Material[]>([]);


  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {

    const fetchData = async () => {
      try {
       const[products,categories,parentCategories,currencies,colors,materials]= await Promise.all([
            fetchAll<Product>('/products'),
            fetchAll<Level2Category>('/categories/level-2'),
            fetchAll<Level1Category>('/categories/level-1'),

            fetchAll<Currency>('/currencies'),
            fetchAll<Color>('/colors'),
            fetchAll<Material>('/materials'),


          ]);
   
        setParentCategories(parentCategories || [])
        setProducts(products || [])
        setCategories(categories || [])
        setColors(colors || [])
        setCurrencies(currencies || [])
        setMaterial(materials || [])

        console.debug("Cats: ",parentCategories)
      } catch (err) {
        setError(err as string); // Type assertion for TypeScript
      } finally {
        setLoading(false);
      }
    };

     fetchData();
  }, [ ]); // Only fetch when url or enabled changes

  return { products,categories,parentCategories,materials,currencies,colors, loading, error,  };
}

export default useFetchAllData;
