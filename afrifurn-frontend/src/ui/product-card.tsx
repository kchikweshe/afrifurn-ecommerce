'use client';

import React from 'react';
import { Product } from '@/types';
import { PRODUCT_IMAGE_URLS } from '@/data/urls';
import Image from 'next/image'
import { Badge, ShoppingCart } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent } from '@/components/ui/card';
interface ProductCardProps {
  product: Product;
}

const ProductCard: React.FC<ProductCardProps> = ({ product }) => {
  const { name, price, currency, is_new, product_variants: variants } = product;
  const mainImage = PRODUCT_IMAGE_URLS.concat(variants[0]?.images[0]) || 'https://via.placeholder.com/150';

  return (
    <Card className="overflow-hidden max-h-dvh transition-all duration-300 hover:shadow-lg">
      <div className="relative aspect-square overflow-hidden">
        <Image
          src={mainImage}
          alt={name}
          fill
          sizes="(max-width: 768px) 80vw, (max-width: 1200px) 50vw, 33vw"
          className="object-cover transition-transform duration-300 hover:scale-110"
        />
        {is_new && (
          <Badge className="absolute top-2 right-2 bg-yellow-400 text-yellow-900 hover:bg-yellow-500">
            New
          </Badge>
        )}
      </div>
      <CardContent className="p-4">
        <h3 className="font-semibold text-lg mb-2 line-clamp-2">{name}</h3>
        <div className="flex items-center justify-between">
          <p className="text-2xl font-bold text-primary">
            {currency}{price.toFixed(2)}
          </p>
          <Button  className="rounded-full">
            <ShoppingCart className="mr-2 h-4 w-4" />
            Add to Cart
          </Button>
        </div>
      </CardContent>
    </Card>
  );
};

export default ProductCard;