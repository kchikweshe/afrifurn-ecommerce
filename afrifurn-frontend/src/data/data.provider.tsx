'use client'
import React, { useReducer, useEffect, useMemo, useCallback, Suspense } from "react";
import { DataContext } from "./data.context";
import { dataReducer, State } from "./reducer/reducer";
import {  fetchAll } from "./data.fetcher";
import { Level2Category, Level1Category, Color, Material, Currency, Category } from "../types";
import LoadingState from "@/app/(home)/room/[name]/LoadingState";
const initialState: State = {

  mainCategories: [],
  levelTwoCategories: [],
  levelOneCategories: [],
  currencies: [],
  colors: [],
  materials: [],
  loading: true,
  error: null,
};

export function DataProvider({ children }:{children:React.ReactNode}) {
  const [state, dispatch] = useReducer(dataReducer, initialState);

  const fetchData = useCallback(async () => {
    dispatch({ type: 'FETCH_START' });
    try {
      const [ currencies, categories, parentCategories, colors, materials, mainCategories] = await Promise.all([
        fetchAll<Currency>('/currencies/'),
        fetchAll<Level2Category>('/categories/level-2/'),
        fetchAll<Level1Category>('/categories/level-1/'),
        fetchAll<Color>('/colors/'),
        fetchAll<Material>('/materials/'),
        fetchAll<Category>('/categories/'),
      ])
      
      dispatch({ 
        type: 'FETCH_SUCCESS', 
        payload: { currencies, levelTwoCategories: categories, levelOneCategories: parentCategories, colors, materials, mainCategories } 
      });
      
    } catch (err) {
      dispatch({ 
        type: 'FETCH_ERROR', 
        payload: err instanceof Error ? err.message : String(err) 
      });
    }
  }, []);

  useEffect(() => {
    fetchData();
  }, [fetchData]);

  const contextValue = useMemo(() => ({
    ...state,
    refetch: fetchData
  }), [state, fetchData]);

  if (state.error) {
    return (
      <div role="alert" className="bg-red-50 border-l-4 border-red-500 p-4 my-4 rounded shadow-sm">
        <div className="flex items-center">
          <div className="flex-shrink-0">
            <svg className="h-5 w-5 text-red-500" viewBox="0 0 20 20" fill="currentColor">
              <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
            </svg>
          </div>
          <div className="ml-3">
            <h3 className="text-lg font-medium text-red-800">Error loading data</h3>
            <p className="text-sm text-red-700 mt-1">{state.error}</p>
            <button 
              onClick={fetchData}
              className="mt-3 px-4 py-2 bg-red-600 text-white rounded hover:bg-red-700 transition-colors"
            >
              Try again
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <DataContext.Provider value={contextValue}>
     {children}
    </DataContext.Provider>
  );
}