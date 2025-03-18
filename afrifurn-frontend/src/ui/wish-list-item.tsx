import Image from 'next/image';
import { Product } from '@/types';

interface WishlistItemProps {
  item: Product;
  moveToCart: (productId: string) => void;
  removeItem: (productId: string) => void;
}

export default function WishlistItem({ item, moveToCart, removeItem }: WishlistItemProps) {
  return (
    <div className="border border-gray-200 rounded-lg p-4">
      <Image src={item.product_variants[0].images[0]} alt={item.name} width={200} height={200} className="rounded-md mb-4" />
      <h3 className="font-semibold">{item.name}</h3>
      <p className="text-gray-600 mb-4">
        {item.currency}{item.price.toFixed(2)} {item.currency}
      </p>
      <div className="flex justify-between">
        <button onClick={() => moveToCart(item._id)} className="bg-blue-500 text-white px-4 py-2 rounded">Add to Cart</button>
        <button onClick={() => removeItem(item._id)} className="text-red-500">Remove</button>
      </div>
    </div>
  );
}