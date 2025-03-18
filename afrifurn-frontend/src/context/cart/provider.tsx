import { CartItem } from "@/types/cart";
import { ReactNode, useEffect, useState } from "react";
import { CartContext } from "./context";

export function CartProvider({ children }: { children: ReactNode }) {
    const [cartItems, setCartItems] = useState<CartItem[]>([]);

    useEffect(() => {
        try {
            // Load cart from localStorage on mount
            const savedCart = localStorage.getItem('cart')
            if (savedCart) {
                const parsedCart = JSON.parse(savedCart)
                // Verify that parsed data is an array
                setCartItems(Array.isArray(parsedCart) ? parsedCart : [])
            }
        } catch (error) {
            console.error('Error loading cart:', error)
            setCartItems([])
        }
    }, [])

    const addToCart = (item: CartItem) => {
        setCartItems(prev => {
            // Ensure prev is an array
            const currentCart = Array.isArray(prev) ? prev : []
            const newCart = [...currentCart, item]
            try {
                localStorage.setItem('cart', JSON.stringify(newCart))
            } catch (error) {
                console.error('Error saving cart:', error)
            }
            return newCart
        })
    }

    const removeFromCart = (itemId: string) => {
        setCartItems(prev => {
            // Ensure prev is an array
            const currentCart = Array.isArray(prev) ? prev : []
            const newCart = currentCart.filter(item => item.productId !== itemId)
            try {
                localStorage.setItem('cart', JSON.stringify(newCart))
            } catch (error) {
                console.error('Error saving cart:', error)
            }
            return newCart
        })
    }

    const updateQuantity = (itemId: string, quantity: number) => {
        setCartItems(prev => {
            // Ensure prev is an array
            const currentCart = Array.isArray(prev) ? prev : []
            const newCart = currentCart.map(item =>
                item.productId === itemId ? { ...item, quantity } : item
            )
            try {
                localStorage.setItem('cart', JSON.stringify(newCart))
            } catch (error) {
                console.error('Error saving cart:', error)
            }
            return newCart
        })
    }

    const clearCart = () => {
        setCartItems([])
        try {
            localStorage.removeItem('cart')
        } catch (error) {
            console.error('Error clearing cart:', error)
        }
    }

    const getCartItems = () => cartItems

    return (
        <CartContext.Provider value={{
            cartItems,
            addToCart,
            removeFromCart,
            updateQuantity,
            clearCart,
            getCartItems
        }}>
            {children}
        </CartContext.Provider>
    )
}



// Example usage in a component
