import { Metadata } from 'next';
import { notFound } from 'next/navigation';
import ProductOverview from './product-overview';
import { productService } from '@/services/product.service';

// Update interface to extend proper Next.js page props
interface PageProps {
  params: {
    shortName: string;
  };
}

// Generate dynamic metadata for SEO
export async function generateMetadata({ params }: { params: Promise<{ shortName: string ,subcategory:string,name:string}> }): Promise<Metadata> {
  const { shortName,name,subcategory } = await params;

  try {
    const product = await productService.getProductByShortName(shortName);

    if (!product) {
      return {
        title: 'Product Not Found',
        description: 'The requested product could not be found.',
      };
    }

    // Extract key product information for SEO
    const {
      name,
      description,
      price,
      category,
      material,
      product_variants

    } = product;

    // Create structured data for rich snippets
    const structuredData = {
      "@context": "https://schema.org/",
      "@type": "Product",
      "name": name,
      "description": description,
      "brand": {
        "@type": "Brand",
        "name": name
      },
      "category": category.name,
      "offers": {
        "@type": "Offer",
        "price": price,
        "priceCurrency": "USD",
        "availability": "https://schema.org/InStock"
      },
      "image": product_variants[0].images?.[0] || '',

    };
    const fullUrl = `https://afri-furn.co.zw/room/${name}/${subcategory}/${shortName}/${name}`


    return {
      title: `${name} | Afri-Furn`,
      description: description || `Discover the ${name}. Premium quality ${category.name} with advanced features and competitive pricing.`,
      keywords: [
        name,
        category.name,
        'buy online',
        'best price',
        'premium quality'
      ].join(', '),

      // Open Graph tags for social media
      openGraph: {
        type: "website",
        title: `${name}`,
        description: description || `Premium ${category.name}`,
        // images: images?.map(img => ({
        //   url: img,
        //   alt: `${name} by ${brand}`
        // })) || [],
        siteName: 'Afri Furn',
        url:fullUrl
      },

      // Twitter Card tags
      twitter: {
        card: 'summary_large_image',
        title: `${name}`,
        description: description || `Premium ${category} `,
        images: product_variants[0].images?.[0],
      },

      // Additional SEO tags
      alternates: {
        canonical:fullUrl,
      },

      // Structured data
      other: {
        'application/ld+json': JSON.stringify(structuredData),
      },

      // Product-specific meta tags
      category: category.name,
      robots: {
        index: true,
        follow: true,
        googleBot: {
          index: true,
          follow: true,
          'max-video-preview': -1,
          'max-image-preview': 'large',
          'max-snippet': -1,
        },
      },
    };
  } catch (error) {
    console.error('Error generating metadata:', error);
    return {
      title: 'Product Page',
      description: 'Product information page',
    };
  }
}

// Update function declaration to use direct destructuring
export default async function ProductPage({ params }: { params: Promise<{ shortName: string }> }) {
  const { shortName } = await params
  try {
    const product = await productService.getProductByShortName(shortName);

    if (!product) {
      notFound();
    }

    return <ProductOverview product={product} />;
  } catch (error) {
    console.error('Error fetching product data:', error);
    throw error; // Let Next.js error boundary handle this
  }
}