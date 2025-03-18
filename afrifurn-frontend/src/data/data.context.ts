import { createContext, useContext } from "react";
import { State } from "./reducer/reducer";



export const DataContext = createContext<State | null>(null);


// Custom Hook
export const useDataContext = () => useContext(DataContext); 
