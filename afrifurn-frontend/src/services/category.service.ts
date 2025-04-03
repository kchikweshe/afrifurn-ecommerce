import { Level1Category, Level2Category } from '../types';
import { productMicroService } from '@/config/api.config';
/**
 * Interface defining the methods for category-related API operations
 */
interface ICategoryService {
  getLevel1Categories(name: string): Promise<Level1Category[]>;
  getLevel2Categories(name: string): Promise<Level2Category[]>;
  getLevel2CategoriesByLevel1(level1categoryId: string): Promise<Level2Category[]>;
}

/**
 * Service responsible for handling category-related API operations
 */
export class CategoryService implements ICategoryService {
  /**
   * Fetches Level 1 categories by name
   * @param name - The name parameter to filter Level 1 categories
   * @returns Promise containing an array of Level1Category objects
   * @throws Error if the API request fails
   */
  async getLevel1Categories(name: string): Promise<Level1Category[]> {
    try {
      const response = await productMicroService.get(`/categories/level-1/${name}`);
      return response.data;
    } catch (error) {
      console.error('Error fetching Level 1 categories:', error);
      throw error;
    }
  }

  /**
   * Fetches Level 2 categories by name
   * @param name - The name parameter to filter Level 2 categories
   * @returns Promise containing an array of Level2Category objects
   * @throws Error if the API request fails
   */
  async getLevel2Categories(name: string): Promise<Level2Category[]> {
    try {
      const response = await productMicroService.get(`/categories/level-2/${name}`);
      return response.data;
    } catch (error) {
      console.error('Error fetching Level2 categories:', error);
      throw error;
    }
  }

  /**
   * Fetches Level 2 categories by Level 1 category ID
   * @param level1categoryId - The ID of the Level 1 category
   * @returns Promise containing an array of Level2Category objects
   * @throws Error if the API request fails
   */
  async getLevel2CategoriesByLevel1(level1categoryId: string): Promise<Level2Category[]> {
    try {
      const response = await productMicroService.get(`/categories/level-2/${level1categoryId}`);
      return response.data;
    } catch (error) {
      console.error('Error fetching Level 2 categories by Level 1:', error);
      throw error;
    }
  }
}

// Export a singleton instance
export const categoryService = new CategoryService();

