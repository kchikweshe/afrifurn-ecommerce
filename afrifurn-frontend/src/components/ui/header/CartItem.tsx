import React from 'react';
import Image from 'next/image';
import { Button } from "@/components/ui/button";
import { formatPrice } from '@/lib/utils/format';
import { PRODUCT_IMAGE_URLS } from '@/data/urls';

const CartItem = ({ item, onRemove }: { item: any; onRemove: (id: string) => void }) => (
    <div className="flex py-4 border-b">
        <div className="w-16 h-16 relative">
            <Image
                src={PRODUCT_IMAGE_URLS + item.image}
                alt={item.name}
                fill
                className="object-cover rounded"
            />
        </div>
        <div className="flex-1 ml-4">
            <h3 className="text-sm font-medium">{item.name}</h3>
            <p className="text-sm text-gray-500">{formatPrice(item.price)}</p>
            <div className="flex items-center mt-2">
                <Button variant="outline" size="icon" className="h-8 w-8">-</Button>
                <span className="mx-2 text-sm">{item.quantity}</span>
                <Button variant="outline" size="icon" className="h-8 w-8">+</Button>
            </div>
        </div>
        <Button variant="ghost" size="icon" className="h-8 w-8" onClick={() => onRemove(item.id)}>
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <line x1="18" y1="6" x2="6" y2="18"></line>
                <line x1="6" y1="6" x2="18" y2="18"></line>
            </svg>
        </Button>
    </div>
);

export default CartItem; 