import { useState, useEffect } from "react";
import { api } from "@/services/baseApi";

// Combined useFetchAll and useFetchOne into a single hook
export function useFetch<T>(url: string, isList: boolean = false) {
  const [data, setData] = useState<T | T[] | null>(isList ? [] : null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await api.get(url);
        setData(response.data);
      } catch (e) {
        console.error(e);
        setError(e as Error);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [url]);

  return { data, loading, error };
}

// Convenience hooks that use the base useFetch
export function useFetchAll<T>(url: string) {
  return useFetch<T>(url, true);
}

export function useFetchOne<T>(url: string) {
  return useFetch<T>(url, false);
} 