export interface CommonModel {
  _id: string;
  short_name: string;
  name: string;
  is_archived:boolean
  created_at: string
  updated_at:string
}
 export interface CategoryProducts{
  category_name:string;
  products:Array<Product>
 }

export interface Dimensions {
    width: number;
    height: number;
    depth?: number;
    length: number;
    weight?: number;
  }
  
  export interface Color extends CommonModel {
    color_code: string;
    image?: string;
  }
  
  export interface Currency extends CommonModel {
    code: string;
    symbol: string;
  }
  export interface Material extends CommonModel{
    name: string;
  
   };
  export interface Category  extends CommonModel {
    images: string[];
    description?: string;
  }

  
  export interface Level1Category extends CommonModel {

    id:string
    category: Category;
    images: string[];
    description?: string;

    
  }
  
  export interface Level2Category extends CommonModel {
    id:string

    level_one_category: Level1Category;
    images: string[];
    description?: string;
  }
  
  export interface ProductVariant  extends CommonModel{
    color_id: string;
    quantity_in_stock: number;
    product_id: string;
    images: string[];
  }
  
  export interface Product  extends CommonModel{
  
    description: string;
    category: Level2Category;
    dimensions: Dimensions;
    is_new: boolean;
    price: number;
    currency: string;
    colors: string[];
    product_variants: ProductVariant[];
    discount?: number;
    views: number;
    material?: string;
  }

  export interface Cart {
    items: CartItem[];
  }
  export interface CartItem {
    product: Product;
    quantity: number;
  }

  // Define the parameters for the filter function
export interface FilterParams {
  start_price?: number;
  end_price?: number;
  colors?: Array<string>;
  width?: number;
  length?: number;
  depth?: number;
  height?: number;
  materials?: Array<string>;
  category?: string;
  page?: number;
  page_size?: number;
  sort_by?: string;
  name?: string; short_name?: string;


  sort_order?: number;
}
