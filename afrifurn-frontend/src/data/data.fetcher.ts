import { productMicroService } from '@/config/api.config';

/**
 * Toggles between replacing spaces with hyphens and hyphens with spaces
 * @param name The string to process
 * @param toHyphens If true, replaces spaces with hyphens; if false, replaces hyphens with spaces
 * @returns The processed string
 */

export async function fetchAll<T>(part: string): Promise<T[]> {
  try {
    const response = await productMicroService.get<T[]>(`${part}`);
    return response.data;

  } catch (error) {
    console.error('Error fetching data:', error);

    return [];
  }
}




