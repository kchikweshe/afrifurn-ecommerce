import { CartItem } from "@/types/cart"
import { createContext } from "react"

export interface CartContextType {
  cartItems: CartItem[]
  addToCart: (item: CartItem) => void
  removeFromCart: (itemId: string) => void
  updateQuantity: (itemId: string, quantity: number) => void
  clearCart: () => void
  getCartItems: () => CartItem[]
}

export const CartContext = createContext<CartContextType | undefined>(undefined)
  
  
  