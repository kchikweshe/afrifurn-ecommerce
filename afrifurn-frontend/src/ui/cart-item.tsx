import Image from 'next/image';
import { Product, ProductVariant, Currency } from '@/types';
import { DataContext } from '@/data/data.context';
import { useContext } from 'react';
interface CartItemProps {
  item: {
    product: Product;
    variant: ProductVariant;
    quantity: number;
  };
  updateQuantity: (productId: string, variantId: string, quantity: number) => void;
  removeItem: (productId: string, variantId: string) => void;
}

export default function CartItem({ item, updateQuantity, removeItem }: CartItemProps) {
  const state = useContext(DataContext)
  if(!state){
    return <div>State is null</div>
  }
  const {currencies}=state
  const getCurrencySymbol = (currency: string) => {
    const currencyData = currencies.find((c: Currency) => c.code === currency);
    return currencyData ? currencyData.symbol : currency;
  };
  return (
    <div className="flex items-center border-b border-gray-200 py-4">
      <Image src={item.variant.images[0]} alt={item.product.name} width={80} height={80} className="rounded-md" />
      <div className="ml-4 flex-grow">
        <h3 className="font-semibold">{item.product.name}</h3>
        <p className="text-gray-600">{item.variant.color_id}</p>
        <p className="text-gray-600">
          {item.product.currency}{item.product.price.toFixed(2)} {getCurrencySymbol(item.product.currency)}
        </p>
      </div>
      <div className="flex items-center">
        <button onClick={() => updateQuantity(item.product._id, item.variant._id, item.quantity - 1)} className="px-2 py-1 bg-gray-200 rounded">-</button>
        <span className="mx-2">{item.quantity}</span>
        <button onClick={() => updateQuantity(item.product._id, item.variant._id, item.quantity + 1)} className="px-2 py-1 bg-gray-200 rounded">+</button>
      </div>
      <button onClick={() => removeItem(item.product._id, item.variant._id)} className="ml-4 text-red-500">Remove</button>
    </div>
  );
}