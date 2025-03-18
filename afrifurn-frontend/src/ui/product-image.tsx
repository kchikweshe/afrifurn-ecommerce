import Image from 'next/image';
import { useState } from 'react';
import { PRODUCT_IMAGE_URLS } from '@/data/urls';

interface ProductImageProps {
  images: string[];
  name: string;
}

export default function ProductImage({ images, name }: ProductImageProps) {
  const [selectedImage, setSelectedImage] = useState(0);
  
  return (
    <div>
      <div className="mb-4">
        <Image 
          src={PRODUCT_IMAGE_URLS+images[selectedImage]} 
          alt={name} 
          width={500} 
          height={500} 
          className="rounded-lg"
        />
      </div>
      <div className="flex gap-2">
        {images.map((image, index) => (
          <button 
            key={index}
            onClick={() => setSelectedImage(index)}
            className={`w-16 h-16 border-2 rounded-md ${selectedImage === index ? 'border-blue-500' : 'border-gray-200'}`}
          >
            <Image src={PRODUCT_IMAGE_URLS+image} alt={`${name} thumbnail ${index + 1}`} width={64} height={64} className="rounded-md" />
          </button>
        ))}
      </div>
    </div>
  );
}