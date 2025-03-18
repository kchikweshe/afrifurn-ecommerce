import React from 'react';
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Sheet, SheetContent, SheetHeader, SheetTitle, SheetTrigger } from "@/components/ui/sheet";
import { ScrollArea } from "@/components/ui/scroll-area";
import { formatPrice } from '@/lib/utils/format';
import { ShoppingCart } from 'lucide-react';
import CartItem from './CartItem';

interface CartSheetProps {
    cartItems: any[];
    cartItemsCount: number;
}

const CartSheet = ({ cartItems, cartItemsCount, onRemove }: { cartItems: any[], cartItemsCount: number; onRemove: (id: string) => void }) => {
    const totalPrice = cartItems.reduce((total, item) => total + (item.price * item.quantity), 0);

    return (
        <Sheet>
            <SheetTrigger asChild>
                <div className="relative">
                    <Button variant="ghost" size="icon">
                        <ShoppingCart className="h-5 w-5 lg:h-6 lg:w-6" />
                        {cartItemsCount > 0 && (
                            <Badge
                                className="absolute -top-2 -right-2 h-5 w-5 flex items-center justify-center p-0 text-xs"
                                variant="destructive"
                            >
                                {cartItemsCount}
                            </Badge>
                        )}
                    </Button>
                </div>
            </SheetTrigger>
            <SheetContent className="w-full sm:max-w-lg">
                <SheetHeader>
                    <SheetTitle>Shopping Cart ({cartItemsCount})</SheetTitle>
                </SheetHeader>
                {cartItemsCount > 0 ? (
                    <>
                        <ScrollArea className="h-[calc(100vh-12rem)]">
                            <div className="flex flex-col divide-y">
                                {cartItems.map((item) => (
                                    <CartItem key={item.id} item={item} onRemove={onRemove}/>
                                ))}
                            </div>
                        </ScrollArea>
                        <div className="space-y-4 mt-4">
                            <div className="flex items-center justify-between text-base font-medium">
                                <span>Subtotal</span>
                                <span>{formatPrice(totalPrice)}</span>
                            </div>
                            <Button className="w-full">
                                Checkout
                            </Button>
                        </div>
                    </>
                ) : (
                    <div className="flex h-[450px] items-center justify-center">
                        <div className="text-center">
                            <ShoppingCart className="mx-auto h-12 w-12 text-gray-400" />
                            <h3 className="mt-2 text-sm font-medium text-gray-900">No items in cart</h3>
                            <p className="mt-1 text-sm text-gray-500">Start shopping to add items to your cart.</p>
                        </div>
                    </div>
                )}
            </SheetContent>
        </Sheet>
    );
};

export default CartSheet; 