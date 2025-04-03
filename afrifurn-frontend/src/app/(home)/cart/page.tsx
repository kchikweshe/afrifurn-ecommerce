'use client'

import { Button } from '@/components/ui/button'
import Image from 'next/image'
import { PRODUCT_IMAGE_URLS } from '@/data/urls'
import { useToast } from '@/hooks/use-toast'
import { X } from 'lucide-react'
import useCart from '@/context/cart/hook'
export default function CartPage() {
  const { cartItems, removeFromCart } = useCart()
  const { toast } = useToast()

  const handleRemoveItem = (itemId: string, productName: string) => {
    removeFromCart(itemId)
    toast({
      title: "Removed from Cart",
      description: `${productName} removed from cart`,
    })
  }

  if (cartItems.length === 0) {
    return (
      <div className="container mx-auto px-4 py-8">
        <h1 className="text-2xl font-bold mb-4 text-center justify-center">Your Cart is Empty</h1>
      </div>
    )
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-2xl font-bold mb-4">Your Cart</h1>
      <div className="space-y-4">
        {cartItems.map((item, index) => (
          <div key={`${item.productId}-${item.variantId}-${index}`}
            className="flex items-center gap-4 p-4 border rounded-lg">
            <div className="relative w-24 h-24">
              <Image
                src={PRODUCT_IMAGE_URLS + item.image}
                alt={item.name}
                fill
                className="object-cover rounded-md"
              />
            </div>
            <div className="flex-1">
              <h3 className="font-semibold">{item.name}</h3>
              <p className="text-sm text-muted-foreground">Color: {item.color}</p>
              <p className="font-medium">${item.price.toFixed(2)}</p>
            </div>
            <Button
              variant="ghost"
              size="icon"
              onClick={() => handleRemoveItem(item.productId, item.name)}
              className="text-red-500 hover:text-red-700"
            >
              <X className="h-5 w-5" />
            </Button>
          </div>
        ))}

        <div className="pt-4 border-t">
          <div className="flex justify-between items-center">
            <span className="text-lg font-semibold">Total:</span>
            <span className="text-lg font-bold">
              ${cartItems.reduce((sum, item) => sum + item.price, 0).toFixed(2)}
            </span>
          </div>
          <Button className="w-full mt-4" size="lg">
            Proceed to Checkout
          </Button>
        </div>
      </div>
    </div>
  )
} 