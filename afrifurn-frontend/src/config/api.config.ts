import { HOST_IP } from "@/data/urls";
import axios from "axios";

export const API_GATEWAY = `https://${HOST_IP}:8090`;
export const api_version:string="/api/v1"


  
export const authService= axios.create({
    baseURL: `${API_GATEWAY}/auth${api_version}`,  
    headers: {"Access-Control-Allow-Origin": "*"}

  });
  
export const productMicroService= axios.create({
    baseURL: `${API_GATEWAY}/product-service${api_version}`,
    headers: {"Access-Control-Allow-Origin": "*"}

  });

 export const orderMicroService= axios.create({
    baseURL: `${API_GATEWAY}/orders${api_version}`,
    headers: {"Access-Control-Allow-Origin": "*"}

  });