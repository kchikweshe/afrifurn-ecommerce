import axios from 'axios';

const API_URL =  'http://5.189.146.192:8000/api/v1';

export const api = axios.create({
  baseURL: API_URL,
});

export const productServiceURL = axios.create({
  baseURL: `${API_URL}/product-service`,
});

export const categoryServiceURL = axios.create({
  baseURL: `${API_URL}/product-service/categories`,
}); 