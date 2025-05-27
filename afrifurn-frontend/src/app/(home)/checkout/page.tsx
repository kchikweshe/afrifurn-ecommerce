'use client';

import { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'
import { Button } from '@/components/ui/button'
import useCart from '@/context/cart/hook'

function getOrCreateGuestId(key: string) {
  let id = typeof window !== 'undefined' ? localStorage.getItem(key) : null
  if (!id) {
    id = 'guest-' + Math.random().toString(36).substring(2, 15)
    if (typeof window !== 'undefined') localStorage.setItem(key, id)
  }
  return id
}

export default function CheckoutPage() {
  const { cartItems, clearCart } = useCart()
  const router = useRouter()
  const [form, setForm] = useState({ name: '', phone: '', address: '' })
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  useEffect(() => {
    if (cartItems.length === 0) router.replace('/cart')
  }, [cartItems, router])

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    setForm({ ...form, [e.target.name]: e.target.value })
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    setError('')
    try {
      // 1. Get or create guest user id
      const userId = getOrCreateGuestId('guest_user_id')
      // 2. Get or create cart id
      let cartId = typeof window !== 'undefined' ? localStorage.getItem('guest_cart_id') : null
      if (!cartId) {
        // Create cart
        const res = await fetch(`${process.env.NEXT_PUBLIC_CART_API}/cart/create/${userId}`, { method: 'POST' })
        const data = await res.json()
        if (!res.ok || data.status_code !== 201) throw new Error('Failed to create cart')
        cartId = userId // Assume cart id is user id for simplicity
        if (typeof window !== 'undefined') localStorage.setItem('guest_cart_id', cartId)
      }
      // 3. Add all items to cart
      for (const item of cartItems) {
        await fetch(`${process.env.NEXT_PUBLIC_CART_API}/cart/add-product/${cartId}/?user_id=${userId}&product_id=${item.productId}&quantity=${item.quantity || 1}&variant_id=${item.variantId}`, { method: 'POST' })
      }
      // 4. Create order
      const orderRes = await fetch(`${process.env.NEXT_PUBLIC_ORDER_API}/orders/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          customer_name: form.name,
          customer_phone: form.phone,
          customer_address: form.address,
          user_id: userId,
          cart_id: cartId
        })
      })
      if (!orderRes.ok) throw new Error('Failed to place order')
      clearCart()
      router.push('/orders')
    } catch (err: any) {
      setError(err.message || 'Something went wrong')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="container mx-auto px-4 py-8 max-w-lg">
      <h1 className="text-2xl font-bold mb-6">Checkout</h1>
      <form onSubmit={handleSubmit} className="space-y-4 bg-white p-6 rounded-lg shadow">
        <div>
          <label className="block mb-1 font-medium" htmlFor="name">Name</label>
          <input
            id="name"
            name="name"
            type="text"
            required
            value={form.name}
            onChange={handleChange}
            className="w-full border px-3 py-2 rounded focus:ring focus:ring-blue-200"
          />
        </div>
        <div>
          <label className="block mb-1 font-medium" htmlFor="phone">Phone</label>
          <input
            id="phone"
            name="phone"
            type="tel"
            required
            value={form.phone}
            onChange={handleChange}
            className="w-full border px-3 py-2 rounded focus:ring focus:ring-blue-200"
          />
        </div>
        <div>
          <label className="block mb-1 font-medium" htmlFor="address">Address</label>
          <textarea
            id="address"
            name="address"
            required
            value={form.address}
            onChange={handleChange}
            className="w-full border px-3 py-2 rounded focus:ring focus:ring-blue-200"
          />
        </div>
        {error && <div className="text-red-600 text-sm">{error}</div>}
        <Button type="submit" className="w-full" size="lg" disabled={loading}>
          {loading ? 'Placing Order...' : 'Place Order'}
        </Button>
      </form>
    </div>
  )
} 