import { CategoryProductsGrid } from "./category-product-list";
import { productService } from "@/services/product.service";

/**
 * Next.js page component for displaying products filtered by subcategory
 * This component is used in the dynamic route /room/[name]/[subcategory]
 * 
 * @param props.params - Contains the subcategory parameter from the URL
 * @returns React component displaying a grid of products for the specified subcategory
 */ 
export default async function Page(props: { params: Promise<{ subcategory: string }> }) {
    // Await and destructure the subcategory parameter
    const params = await props.params;
    const { subcategory } = params;
    
    
    // Fetch products filtered by the subcategory's short_name
    const data = await productService.filterCategoryProducts({ category_short_name: subcategory });
    
    // Render the product grid component with the filtered products
    return <CategoryProductsGrid categoryProducts={data} short_name={subcategory} />;
}