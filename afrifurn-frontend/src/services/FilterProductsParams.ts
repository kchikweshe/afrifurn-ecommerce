/**
 * Interface defining the parameters for filtering product queries
 */
export interface FilterProductsParams {
  /** Minimum price filter value */
  start_price?: number;
  /** Maximum price filter value */
  end_price?: number;
  /** Filter products by color */
  color?: string;
  /** Filter products by width (in units) */
  width?: number;
  /** Filter products by length (in units) */
  length?: number;
  /** Filter products by depth (in units) */
  depth?: number;
  /** Filter products by height (in units) */
  height?: number;
  /** Filter products by material type */
  material?: string;
  /** Filter products by category */
  category?: string;
  /** Page number for pagination */
  page?: number;
  /** Number of items per page */
  page_size?: number;
  /** Field name to sort by */
  sort_by?: string;
  /** Sort order: 1 for ascending, -1 for descending */
  sort_order?: number;
  /** Filter products by name */
  name?: string;
}
