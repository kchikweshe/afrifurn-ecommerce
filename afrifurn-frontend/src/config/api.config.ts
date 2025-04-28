import { HOST_IP } from "@/data/urls";
import axios from "axios";

// Use the actual domain instead of HOST_IP for production
export const API_GATEWAY = process.env.NODE_ENV === 'production' 
  ? 'https://afrifurn.co.zw/api'
  : `http://${HOST_IP}`;
export const api_version:string="/api/v1"


  
export const authService= axios.create({
    baseURL: `${API_GATEWAY}/auth${api_version}`,  
    headers: {
        "Access-Control-Allow-Origin": "*",
        "Content-Type": "application/json"
    }
});
  
export const productMicroService= axios.create({
    baseURL: `${API_GATEWAY}/product-service${api_version}`,
    headers: {
        "Access-Control-Allow-Origin": "*",
        "Content-Type": "application/json"
    }
});

export const orderMicroService= axios.create({
    baseURL: `${API_GATEWAY}/orders${api_version}`,
    headers: {
        "Access-Control-Allow-Origin": "*",
        "Content-Type": "application/json"
    }
});