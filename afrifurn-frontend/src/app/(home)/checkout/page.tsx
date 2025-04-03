'use client';

import React, { useState } from 'react';
import { useRouter } from 'next/navigation';
import { CheckCircle } from 'lucide-react';
import Image from 'next/image';

export default function SimpleCheckoutPage() {
  const router = useRouter();
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [orderComplete, setOrderComplete] = useState(false);
  const [error, setError] = useState<string | null>(null);
  
  // Form state
  const [formData, setFormData] = useState({
    fullName: '',
    email: '',
    address: '',
    city: '',
    zipCode: '',
    country: 'Kenya',
    cardNumber: '',
    cardName: '',
    expiryDate: '',
    cvv: ''
  });
  
  // Sample cart items - in a real app, these would come from your cart state/context
  const cartItems = [
    { id: 1, name: 'Modern Wooden Coffee Table', price: 249.99, quantity: 1 },
    { id: 2, name: 'Handwoven Basket Set', price: 89.99, quantity: 2 }
  ];
  
  const subtotal = cartItems.reduce((sum, item) => sum + (item.price * item.quantity), 0);
  const shipping = 10;
  const tax = subtotal * 0.16; // 16% VAT
  const total = subtotal + shipping + tax;
  
  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };
  
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSubmitting(true);
    setError(null);
    
    try {
      // Simulate API call to process order
      await new Promise(resolve => setTimeout(resolve, 1500));
      setOrderComplete(true);
      
      // In a real app, you would redirect to an order confirmation page
      setTimeout(() => {
        router.push('/orders');
      }, 3000);
      
    } catch (err) {
      setError('There was a problem processing your order. Please try again.');
    } finally {
      setIsSubmitting(false);
    }
  };
  
  const handlePaynowCheckout = () => {
    // In a real app, you would redirect to Paynow payment page
    // For now, we'll just simulate a redirect
    router.push('/paynow-checkout');
  };
  
  if (orderComplete) {
    return (
      <div className="container mx-auto px-4 py-16 max-w-4xl">
        <div className="text-center bg-white p-8 rounded-lg shadow-sm border border-gray-200">
          <div className="inline-flex items-center justify-center w-16 h-16 bg-green-100 rounded-full mb-6">
            <CheckCircle className="h-8 w-8 text-green-600" />
          </div>
          <h1 className="text-3xl font-bold mb-4">Thank You for Your Order!</h1>
          <p className="text-lg text-gray-600 mb-8">
            Your order has been placed successfully. We're preparing it for shipment.
          </p>
          <p className="text-gray-600 mb-6">
            A confirmation email has been sent to {formData.email}
          </p>
          <div className="mt-8">
            <button
              onClick={() => router.push('/orders')}
              className="bg-blue-600 text-white px-6 py-3 rounded-lg font-medium hover:bg-blue-700 transition-colors"
            >
              View Your Orders
            </button>
          </div>
        </div>
      </div>
    );
  }
  
  return (
    <div className="container mx-auto px-4 py-8">
      <div className="max-w-6xl mx-auto">
        <h1 className="text-3xl font-bold mb-8">Checkout</h1>
        
        {error && (
          <div className="bg-red-50 border-l-4 border-red-500 text-red-700 p-4 mb-6 rounded-md">
            <div className="flex">
              <div className="ml-3">
                <p className="text-sm font-medium">{error}</p>
              </div>
            </div>
          </div>
        )}
        
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Order Summary */}
          <div className="lg:col-span-2">
            <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
              <h2 className="text-xl font-semibold mb-6">Order Summary</h2>
              
              <div className="space-y-4 mb-6">
                {cartItems.map(item => (
                  <div key={item.id} className="flex justify-between items-center py-3 border-b border-gray-100">
                    <div className="flex-1">
                      <p className="font-medium">{item.name}</p>
                      <p className="text-sm text-gray-500">Qty: {item.quantity}</p>
                    </div>
                    <p className="font-medium">${(item.price * item.quantity).toFixed(2)}</p>
                  </div>
                ))}
              </div>
              
              <div className="border-t border-gray-200 pt-4 mb-4">
                <div className="flex justify-between mb-2">
                  <p className="text-gray-600">Subtotal</p>
                  <p className="font-medium">${subtotal.toFixed(2)}</p>
                </div>
                <div className="flex justify-between mb-2">
                  <p className="text-gray-600">Shipping</p>
                  <p className="font-medium">${shipping.toFixed(2)}</p>
                </div>
                <div className="flex justify-between mb-2">
                  <p className="text-gray-600">Tax (16%)</p>
                  <p className="font-medium">${tax.toFixed(2)}</p>
                </div>
              </div>
              
              <div className="border-t border-gray-200 pt-4">
                <div className="flex justify-between mb-6">
                  <p className="font-semibold text-lg">Total</p>
                  <p className="font-semibold text-xl">${total.toFixed(2)}</p>
                </div>
                
                {/* <button
                  onClick={handlePaynowCheckout}
                  className="w-full bg-blue-600 text-white px-6 py-3 rounded-lg font-medium hover:bg-blue-700 transition-colors"
                >
                  Proceed to Paynow
                </button> */}
                <a  href='https://www.paynow.co.zw/Payment/Link/?q=c2VhcmNoPWtjaGlrd2VzaGUlNDBnbWFpbC5jb20mYW1vdW50PTE1MC4wMCZyZWZlcmVuY2U9Jmw9MA%3d%3d' target='_blank'>
                <img 
                className=' bg-blue-600 text-white  rounded-lg font-medium hover:bg-blue-700 transition-colors'
                src='https://www.paynow.co.zw/Content/Buttons/Medium_buttons/button_buy-now_medium.png' style={{border: '0'}} /></a>
                
                <p className="text-center text-sm text-gray-500 mt-4">
                  You will be redirected to Paynow to complete your payment securely.
                </p>
              </div>
            </div>
          </div>
          
          {/* Payment Information */}
          <div className="lg:col-span-1">
            <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200 sticky top-6">
              <h2 className="text-xl font-semibold mb-6">Payment Methods</h2>
              
              <div className="space-y-4">
                <div className="flex items-center p-3 border border-gray-200 rounded-lg">
                  <div className="w-10 h-6 mr-3">
                    <Image 
                      src="/paynow-logo.png" 
                      alt="Paynow" 
                      width={40} 
                      height={24} 
                      className="object-contain"
                    />
                  </div>
                  <span className="font-medium">Paynow</span>
                </div>
                
                <div className="flex items-center p-3 border border-gray-200 rounded-lg opacity-50">
                  <div className="w-10 h-6 mr-3">
                    <Image 
                      src="/visa-logo.png" 
                      alt="Visa" 
                      width={40} 
                      height={24} 
                      className="object-contain"
                    />
                  </div>
                  <span className="font-medium">Credit Card (Coming Soon)</span>
                </div>
                
                <div className="flex items-center p-3 border border-gray-200 rounded-lg opacity-50">
                  <div className="w-10 h-6 mr-3">
                    <Image 
                      src="/mpesa-logo.png" 
                      alt="M-Pesa" 
                      width={40} 
                      height={24} 
                      className="object-contain"
                    />
                  </div>
                  <span className="font-medium">M-Pesa (Coming Soon)</span>
                </div>
              </div>
              
              <div className="mt-6 pt-4 border-t border-gray-200">
                <h3 className="font-medium mb-2">Secure Checkout</h3>
                <p className="text-sm text-gray-500">
                  Your payment information is processed securely. We do not store credit card details.
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
} 