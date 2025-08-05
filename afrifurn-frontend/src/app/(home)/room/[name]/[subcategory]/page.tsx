import { CategoryProductsGrid } from './category-product-list';
import { productService } from '@/services/product.service';
import { Metadata } from 'next';


interface PageProps {
    params: { subcategory: string, name: string };
}
export function formatSubcategoryName(slug: string): string {
    return slug
        .replace(/-/g, ' ')                     // Replace dashes with spaces
        .replace(/\s+/g, ' ')                   // Remove multiple spaces
        .trim()                                 // Trim whitespace
        .replace(/\b\w/g, c => c.toUpperCase()) // Capitalize each word
}

// ✅ SEO Metadata Function
export async function generateMetadata(
    { params }: PageProps
): Promise<Metadata> {


    const { name, subcategory } = params;

    const formattedName = formatSubcategoryName(subcategory);
    const fullUrl = `https://afri-furn.co.zw/room/${name}/${subcategory}`
    console.log(fullUrl)
    return {
        title: `${formattedName} | Afri-Furn`,
        description: `Explore top-quality furniture in the ${formattedName} category. Shop modern designs, custom finishes, and fast delivery.`,
        openGraph: {
            title: `${formattedName} Furniture | Afri-Furn`,
            description: `Discover modern and stylish ${formattedName} furniture perfect for every room.`,
            url: fullUrl,
            type: 'website',
        },
        alternates: {
            canonical: fullUrl,
        },
    };
}

// ✅ Page Component
export default async function Page({ params }: PageProps) {
    const { subcategory } = params;
    const data = await productService.filterCategoryProducts({
        category_short_name: subcategory,
    });

    return (
        <CategoryProductsGrid
            categoryProducts={data}
            short_name={subcategory}
        />
    );
}
