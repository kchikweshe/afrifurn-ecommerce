'use client';

import React, { useState, useEffect } from 'react';
import Link from 'next/link';
import { Package, ChevronRight, Search } from 'lucide-react';

// Order status type
type OrderStatus = 'processing' | 'shipped' | 'delivered' | 'cancelled';

// Order interface
interface Order {
  id: string;
  date: string;
  total: number;
  status: OrderStatus;
  items: {
    id: number;
    name: string;
    price: number;
    quantity: number;
  }[];
}

export default function OrdersPage() {
  const [orders, setOrders] = useState<Order[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');
  
  useEffect(() => {
    // Simulate fetching orders from an API
    const fetchOrders = async () => {
      try {
        // In a real app, this would be an API call
        await new Promise(resolve => setTimeout(resolve, 1000));
        
        // Sample orders data
        const sampleOrders: Order[] = [
          {
            id: 'ORD-2023-1001',
            date: '2023-06-15T10:30:00Z',
            total: 429.97,
            status: 'delivered',
            items: [
              { id: 1, name: 'Modern Wooden Coffee Table', price: 249.99, quantity: 1 },
              { id: 2, name: 'Handwoven Basket Set', price: 89.99, quantity: 2 }
            ]
          },
          {
            id: 'ORD-2023-0892',
            date: '2023-05-28T14:45:00Z',
            total: 349.99,
            status: 'shipped',
            items: [
              { id: 3, name: 'Leather Accent Chair', price: 349.99, quantity: 1 }
            ]
          },
          {
            id: 'ORD-2023-0764',
            date: '2023-04-12T09:15:00Z',
            total: 189.97,
            status: 'delivered',
            items: [
              { id: 4, name: 'Ceramic Vase Set', price: 59.99, quantity: 1 },
              { id: 5, name: 'Woven Wall Hanging', price: 129.98, quantity: 1 }
            ]
          },
          {
            id: 'ORD-2023-0651',
            date: '2023-03-05T16:20:00Z',
            total: 799.99,
            status: 'cancelled',
            items: [
              { id: 6, name: 'Teak Dining Table', price: 799.99, quantity: 1 }
            ]
          },
          {
            id: 'ORD-2023-0542',
            date: '2023-02-18T11:10:00Z',
            total: 459.96,
            status: 'delivered',
            items: [
              { id: 7, name: 'Rattan Pendant Light', price: 114.99, quantity: 4 }
            ]
          }
        ];
        
        setOrders(sampleOrders);
      } catch (error) {
        console.error('Error fetching orders:', error);
      } finally {
        setIsLoading(false);
      }
    };
    
    fetchOrders();
  }, []);
  
  // Filter orders based on search query
  const filteredOrders = orders.filter(order => 
    order.id.toLowerCase().includes(searchQuery.toLowerCase()) ||
    order.items.some(item => item.name.toLowerCase().includes(searchQuery.toLowerCase()))
  );
  
  // Format date
  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', { 
      year: 'numeric', 
      month: 'long', 
      day: 'numeric' 
    });
  };
  
  // Get status badge color
  const getStatusColor = (status: OrderStatus) => {
    switch (status) {
      case 'processing':
        return 'bg-yellow-100 text-yellow-800';
      case 'shipped':
        return 'bg-blue-100 text-blue-800';
      case 'delivered':
        return 'bg-green-100 text-green-800';
      case 'cancelled':
        return 'bg-red-100 text-red-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };
  
  return (
    <div className="container mx-auto px-4 py-8">
      <div className="max-w-6xl mx-auto">
        <h1 className="text-3xl font-bold mb-8">My Orders</h1>
        
        {/* Search */}
        <div className="mb-8">
          <div className="relative">
            <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <Search className="h-5 w-5 text-gray-400" />
            </div>
            <input
              type="text"
              placeholder="Search orders by ID or product name"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="pl-10 w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-blue-500 focus:border-blue-500"
            />
          </div>
        </div>
        
        {isLoading ? (
          <div className="flex justify-center items-center py-12">
            <svg className="animate-spin h-8 w-8 text-blue-600" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
              <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
          </div>
        ) : filteredOrders.length === 0 ? (
          <div className="text-center py-12 bg-white rounded-lg shadow-sm border border-gray-200">
            <Package className="h-12 w-12 text-gray-400 mx-auto mb-4" />
            <h3 className="text-lg font-medium text-gray-900 mb-2">No orders found</h3>
            {searchQuery ? (
              <p className="text-gray-500">No orders match your search criteria.</p>
            ) : (
              <>
                <p className="text-gray-500 mb-6">You haven't placed any orders yet.</p>
                <Link href="/" className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-blue-600 hover:bg-blue-700">
                  Start Shopping
                </Link>
              </>
            )}
          </div>
        ) : (
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden">
            <div className="divide-y divide-gray-200">
              {filteredOrders.map((order) => (
                <div key={order.id} className="p-6 hover:bg-gray-50 transition-colors">
                  <div className="flex flex-col sm:flex-row sm:justify-between sm:items-center mb-4">
                    <div>
                      <h3 className="text-lg font-medium text-gray-900">Order #{order.id}</h3>
                      <p className="text-sm text-gray-500">{formatDate(order.date)}</p>
                    </div>
                    <div className="mt-2 sm:mt-0 flex items-center">
                      <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getStatusColor(order.status)}`}>
                        {order.status.charAt(0).toUpperCase() + order.status.slice(1)}
                      </span>
                      <span className="ml-4 text-lg font-medium">${order.total.toFixed(2)}</span>
                    </div>
                  </div>
                  
                  <div className="mt-4 space-y-2">
                    {order.items.map((item) => (
                      <div key={item.id} className="flex justify-between items-center">
                        <div className="flex items-center">
                          <div className="ml-4">
                            <p className="text-sm font-medium text-gray-900">{item.name}</p>
                            <p className="text-sm text-gray-500">Qty: {item.quantity}</p>
                          </div>
                        </div>
                        <p className="text-sm font-medium text-gray-900">${(item.price * item.quantity).toFixed(2)}</p>
                      </div>
                    ))}
                  </div>
                  
                  <div className="mt-6 flex justify-end">
                    <Link 
                      href={`/orders/${order.id}`} 
                      className="inline-flex items-center px-4 py-2 border border-gray-300 shadow-sm text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50"
                    >
                      View Details
                      <ChevronRight className="ml-2 h-4 w-4" />
                    </Link>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
} 