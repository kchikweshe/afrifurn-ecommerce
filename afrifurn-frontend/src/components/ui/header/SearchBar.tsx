'use client'
import React, { useState, useEffect, useRef } from 'react';
import Image from 'next/image';
import { Input } from "@/components/ui/input";
import { Search, X } from 'lucide-react';
import { useFilterCollection } from '@/hooks/useFilterCollection';
import { useDebounce } from '@/hooks/useDebounce';
import { useOnClickOutside } from '@/hooks/useOnClickOutside';
import { Product } from '@/types';
import { PRODUCT_IMAGE_URLS } from '@/data/urls';

interface SearchBarProps {
    onClose?: () => void;
}

const SearchBar: React.FC<SearchBarProps> = ({ onClose }) => {
    const [searchTerm, setSearchTerm] = useState('');
    const [isOpen, setIsOpen] = useState(false);
    const [isFocused, setIsFocused] = useState(false);
    const debouncedSearch = useDebounce(searchTerm, 300);
    const containerRef = useRef<HTMLDivElement>(null);
    const inputRef = useRef<HTMLInputElement>(null);
    
    const { data: products, loading, filterCollection } = useFilterCollection<Product>();

    useOnClickOutside(containerRef, () => {
        setIsOpen(false);
        setIsFocused(false);
    });

    useEffect(() => {
        if (debouncedSearch) {
            filterCollection('products', { name: debouncedSearch });
            setIsOpen(true);
        } else {
            setIsOpen(false);
        }
    }, [debouncedSearch, filterCollection]);

    const handleSearch = (e: React.ChangeEvent<HTMLInputElement>) => {
        setSearchTerm(e.target.value);
        if (e.target.value === '') {
            setIsOpen(false);
        }
    };

    const clearSearch = () => {
        setSearchTerm('');
        setIsOpen(false);
        inputRef.current?.focus();
    };

    return (
        <div className="relative">
            <div className="relative w-full" ref={containerRef}>
                <div 
                    className={`
                        flex items-center bg-white/90 backdrop-blur-md rounded-full border transition-all duration-300
                        ${isFocused 
                            ? 'border-primary/30 ring-2 ring-primary/20 shadow-lg shadow-primary/10' 
                            : 'border-gray-200/80 hover:border-gray-300/90 hover:shadow-md'
                        }
                    `}
                >
                    <Search className="ml-4 text-gray-400" size={18} strokeWidth={2.5} />
                    <Input
                        ref={inputRef}
                        type="text"
                        value={searchTerm}
                        onChange={handleSearch}
                        onFocus={() => {
                            setIsFocused(true);
                            if (searchTerm) setIsOpen(true);
                        }}
                        placeholder="Search products..."
                        className="border-0 focus:ring-0 focus:outline-none bg-transparent h-12 px-3 text-base font-medium placeholder:text-gray-400/80"
                        autoComplete="off"
                    />
                    {searchTerm && (
                        <button
                            onClick={clearSearch}
                            className="p-2 hover:bg-gray-100/80 rounded-full mx-2 transition-colors"
                            aria-label="Clear search"
                        >
                            <X size={16} className="text-gray-500" strokeWidth={2.5} />
                        </button>
                    )}
                </div>
                
                {isOpen && (
                    <div className="absolute left-0 right-0 mt-2 bg-white/95 backdrop-blur-md rounded-xl shadow-xl border border-gray-200/70 max-h-[calc(100vh-180px)] overflow-y-auto z-50 animate-in fade-in slide-in-from-top-2 duration-200">
                        {loading ? (
                            <div className="p-6 text-center text-gray-500">
                                <div className="animate-spin rounded-full h-7 w-7 border-b-2 border-primary mx-auto"></div>
                                <p className="mt-3 text-sm font-medium">Searching products...</p>
                            </div>
                        ) : products && products.length > 0 ? (
                            <div className="py-2">
                                {products.map((product) => (
                                    <div
                                        key={product.short_name}
                                        className="px-4 py-3 hover:bg-gray-50/80 cursor-pointer flex items-center gap-4 transition-colors group"
                                        onClick={() => {
                                            setIsOpen(false);
                                            setSearchTerm('');
                                        }}
                                    >
                                        {product.product_variants[0].images[0] && (
                                            <div className="relative flex-shrink-0 w-14 h-14 overflow-hidden rounded-lg">
                                                <Image
                                                    src={PRODUCT_IMAGE_URLS + product.product_variants[0].images[0]}
                                                    alt={product.name}
                                                    fill
                                                    className="object-cover transition-transform duration-300 group-hover:scale-110"
                                                />
                                            </div>
                                        )}
                                        <div className="flex-1 min-w-0">
                                            <div className="text-base font-medium text-gray-900 truncate group-hover:text-primary transition-colors">{product.name}</div>
                                            <div className="text-sm text-gray-500 mt-0.5">${product.price}</div>
                                        </div>
                                    </div>
                                ))}
                            </div>
                        ) : (
                            <div className="p-8 text-center">
                                <div className="w-16 h-16 mx-auto mb-4 bg-gray-100 rounded-full flex items-center justify-center">
                                    <Search className="text-gray-400" size={24} />
                                </div>
                                <p className="text-gray-700 text-sm font-medium">No products found</p>
                                <p className="text-gray-400 text-xs mt-1.5">Try a different search term</p>
                            </div>
                        )}
                    </div>
                )}
            </div>
            
            {onClose && (
                <button
                    onClick={onClose}
                    className="absolute right-3 top-1/2 -translate-y-1/2 md:hidden"
                >
                    <X className="h-5 w-5 text-gray-500" />
                </button>
            )}
        </div>
    );
};

export default SearchBar;