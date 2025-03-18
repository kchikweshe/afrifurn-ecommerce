import type { CartItem } from '@/types/cart'

export class CartService {
  static addToCart(item: CartItem): void {
    // Get existing cart from localStorage
    const cart = JSON.parse(localStorage.getItem('cart') || '[]')
    
    // Add new item
    cart.push(item)
    
    // Save back to localStorage
    localStorage.setItem('cart', JSON.stringify(cart))
  }
} 