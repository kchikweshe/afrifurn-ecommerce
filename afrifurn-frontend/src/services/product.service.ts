import { productMicroService } from '@/config/api.config';
import { CategoryProducts, Product, FilterParams } from '@/types';

/**
 * Interface representing parameters for filtering products
 */
export interface FilterProductsParams {
  /** Minimum price filter */
  start_price?: number;
  /** Maximum price filter */
  end_price?: number;
  /** Color filter */
  color?: string;
  /** Width dimension filter in cm */
  width?: number;
  /** Length dimension filter in cm */
  length?: number;
  /** Depth dimension filter in cm */
  depth?: number;
  /** Height dimension filter in cm */
  height?: number;
  /** Material type filter */
  material?: string;
  /** Category filter */
  category?: string;
  /** Page number for pagination */
  page?: number;
  /** Number of items per page */
  page_size?: number;
  /** Field to sort by */
  sort_by?: string;
  /** Sort order (1 for ascending, -1 for descending) */
  sort_order?: number;
  /** Product name filter */
  name?: string;
}

/**
 * Interface defining product service operations
 */
export interface IProductService {
  filterProducts(params: FilterProductsParams): Promise<Product[]>;
  filterCategoryProducts(params: FilterParams): Promise<CategoryProducts>;
  getProductByShortName(shortName: string): Promise<Product>;
}

/**
 * Implementation of product service operations
 */
export class ProductService implements IProductService {
  /**
   * Filters products based on provided parameters
   * @param params - Filter parameters for products
   * @returns Promise containing array of filtered products
   * @throws Error if the API request fails
   */
  async filterProducts(params: FilterProductsParams): Promise<Product[]> {
    try {
      const response = await productMicroService.get('/filter', { params });
      return response.data["data"] as Product[];
    } catch (error) {
      console.error('Error filtering products:', error);
      throw error;
    }
  }

  /**
   * Filters products by category using provided parameters
   * @param params - Filter parameters including category information
   * @returns Promise containing category products data
   * @throws Error if the API request fails
   */
  async filterCategoryProducts(params: FilterParams): Promise<CategoryProducts> {
    const queryParams = new URLSearchParams();
    Object.entries(params).forEach(([key, value]) => {
      if (value !== undefined) {
        queryParams.append(key, value.toString());
      }
    });

    try {
      console.info('Filtering products by Category:', params.short_name);
      const response = await productMicroService.get(`/products/by-level-two-category/filter?short_name=${params.name}`);
      return response.data["data"] as CategoryProducts;
    } catch (error) {
      console.error('Error filtering products:', error);
      throw error;
    }
  }

  /**
   * Retrieves a specific product by its short name
   * @param shortName - Short name identifier of the product
   * @returns Promise containing the requested product
   * @throws Error if the API request fails
   */
  async getProductByShortName(shortName: string): Promise<Product> {
    try {
      const response = await productMicroService.get('/products/filter-one', { params: { short_name: shortName } });
      return response.data["data"] as Product;
    } catch (error) {
      console.error('Error getting product:', error);
      throw error;
    }
  }
}

// Export a singleton instance
export const productService = new ProductService(); 