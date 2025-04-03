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

// Update function declaration to use direct destructuring
export default async function ProductPage({ params }: { params: Promise<{ shortName: string } >}) {
  const {shortName}=await params
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