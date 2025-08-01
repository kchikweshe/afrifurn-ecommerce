'use client'

import React, { useState, useEffect, useRef } from 'react'
import Image from 'next/image'
import Link from 'next/link'
import { Menu, ShoppingCart, Search } from 'lucide-react'
import { Button } from "@/components/ui/button"
import { useDataContext } from '@/data/data.context'
import { useCart } from '@/context/cart/use-cart'
import SearchBar from './SearchBar'
import DesktopNavigation from './DesktopNavigation'
import MobileMenu from './MobileMenu'
import UserMenu from './UserMenu'
import { useAuthContext } from '@/ui/auth-provider'
import { PRODUCT_IMAGE_URLS } from '@/data/urls'

interface HeaderProps {
    logoUrl: string;
}

const Header: React.FC<HeaderProps> = ({ logoUrl }) => {
    const { cartItems } = useCart();
    const cartItemsCount = cartItems.length;
    const { user } = useAuthContext();
    const state = useDataContext();
    const [hoveredCategory, setHoveredCategory] = useState<string | null>(null);
    const [isMenuOpen, setIsMenuOpen] = useState(false);
    const [isCartOpen, setIsCartOpen] = useState(false);
    const [isSearchOpen, setIsSearchOpen] = useState(false);
    const cartRef = useRef<HTMLDivElement>(null);

    if (!state) return <div>Loading...</div>;
    const { levelOneCategories, levelTwoCategories, mainCategories } = state;

    // Close cart preview when clicking outside
    useEffect(() => {
        function handleClickOutside(event: MouseEvent) {
            if (cartRef.current && !cartRef.current.contains(event.target as Node)) {
                setIsCartOpen(false);
            }
        }
        if (isCartOpen) {
            document.addEventListener('mousedown', handleClickOutside);
        } else {
            document.removeEventListener('mousedown', handleClickOutside);
        }
        return () => {
            document.removeEventListener('mousedown', handleClickOutside);
        };
    }, [isCartOpen]);

    const CartPreview = () => (
        <div ref={cartRef} className="absolute right-0 mt-2 w-72 bg-white rounded-lg shadow-xl border border-gray-200 z-50 overflow-hidden">
            <div className="p-3">
                <div className="flex justify-between items-center mb-3">
                    <h3 className="font-medium text-sm">Cart ({cartItemsCount})</h3>
                    <button
                        onClick={() => setIsCartOpen(false)}
                        className="text-gray-400 hover:text-gray-600"
                    >
                        <span className="sr-only">Close</span>
                        <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12"></path></svg>
                    </button>
                </div>

                {cartItems.length > 0 ? (
                    <>
                        <div className="max-h-56 overflow-y-auto divide-y divide-gray-100">
                            {cartItems.map((item) => (
                                <div key={item.name} className="flex items-center py-2 group">
                                    <div className="h-12 w-12 relative flex-shrink-0 rounded overflow-hidden">
                                        <Image
                                            src={PRODUCT_IMAGE_URLS + item.image || '/placeholder.png'}
                                            alt={item.name}
                                            fill
                                            className="object-cover transition-transform group-hover:scale-105"
                                        />
                                    </div>
                                    <div className="ml-3 flex-1">
                                        <p className="text-xs font-medium line-clamp-1">{item.name}</p>
                                        <div className="flex justify-between items-center mt-1">
                                            <p className="text-xs text-gray-500">Qty: {item.quantity}</p>
                                            <p className="text-xs font-semibold">${item.price.toFixed(2)}</p>
                                        </div>
                                    </div>
                                </div>
                            ))}
                        </div>

                        <div className="mt-3 pt-2 border-t border-gray-100">
                            <div className="flex justify-between mb-3">
                                <span className="text-xs">Subtotal:</span>
                                <span className="font-medium text-sm">
                                    ${cartItems.reduce((total, item) => total + (item.price * item.quantity), 0).toFixed(2)}
                                </span>
                            </div>

                            <div className="flex gap-2 mt-2">
                                <Link href="/cart" className="flex-1">
                                    <Button
                                        className="w-full h-8 text-xs"
                                        variant="outline"
                                        onClick={() => setIsCartOpen(false)}
                                    >
                                        View Cart
                                    </Button>
                                </Link>
                                <Link href="/checkout" className="flex-1">
                                    <Button
                                        className="w-full h-8 text-xs"
                                        onClick={() => setIsCartOpen(false)}
                                    >
                                        Checkout
                                    </Button>
                                </Link>
                            </div>
                        </div>
                    </>
                ) : (
                    <div className="py-5 text-center">
                        <div className="mx-auto w-10 h-10 rounded-full bg-gray-50 flex items-center justify-center mb-3">
                            <ShoppingCart className="h-5 w-5 text-gray-400" />
                        </div>
                        <p className="text-gray-500 text-xs mb-3">Your cart is empty</p>
                        <Link href="/products">
                            <Button
                                variant="outline"
                                className="text-xs h-8"
                                onClick={() => setIsCartOpen(false)}
                            >
                                Continue Shopping
                            </Button>
                        </Link>
                    </div>
                )}
            </div>
        </div>
    );

    const MobileSearchModal = () => (
        <div className={`fixed inset-0 z-50 transition-all duration-300 ${isSearchOpen ? 'opacity-100' : 'opacity-0 pointer-events-none'}`}>
            {/* Backdrop */}
            <div
                className="absolute inset-0 bg-black/50"
                onClick={() => setIsSearchOpen(false)}
            />

            {/* Search Container */}
            <div className={`absolute top-0 left-0 right-0 bg-white p-4 transition-transform duration-300 ${isSearchOpen ? 'translate-y-0' : '-translate-y-full'}`}>
                <div className="relative">
                    <SearchBar onClose={() => setIsSearchOpen(false)} />
                </div>
            </div>
        </div>
    );

    return (
        <>
            <header className="bg-white shadow-sm w-full z-50 text-base">
                <div className="mx-auto flex items-center justify-between h-24 px-2 md:px-6 relative">
                    {/* Left: Menu (mobile) */}
                    <div className="flex items-center gap-2 min-w-0 md:static absolute left-0 top-0 h-full z-10">
                        <Button
                            variant="ghost"
                            size="icon"
                            className="h-9 w-9 p-0 mr-1 lg:hidden"
                            onClick={() => setIsMenuOpen(true)}
                        >
                            <Menu className="h-5 w-5 text-gray-700" />
                        </Button>
                    </div>
                    {/* Center: Logo (always centered on mobile, left on desktop) */}
                    <div className="flex flex-shrink-0 justify-center  absolute md:static left-0 right-0 top-0 h-full pointer-events-none md:pointer-events-auto">
                        <div className="pointer-events-auto flex items-center">
                            <Link href="/" className="flex items-center min-w-0 ">
                                <Image
                                    src={logoUrl}
                                    alt="Afrifurn Logo"
                                    width={128}
                                    height={128}
                                    className="h-28 w-full md:h-[128px] md:w-auto object-contain"
                                />
                            </Link>
                        </div>
                    </div>
                    {/* Center: SearchBar (desktop only) */}
                    <div className="hidden md:flex flex-1 justify-center px-4">
                        <div className="w-full">
                            <SearchBar />
                        </div>
                    </div>
                    {/* Right: Utility icons and nav (desktop) */}
                    <div className="flex items-center gap-2 min-w-0 md:static absolute right-0 top-0 h-full z-10">
                        <nav className="hidden md:flex items-center gap-4 text-sm font-medium">
                            <Link href="/about" className="text-gray-700 hover:text-primary transition-colors">About</Link>
                            <Link href="/contact" className="text-gray-700 hover:text-primary transition-colors">Contact</Link>
                            <Link href="/deals" className="text-gray-700 hover:text-primary transition-colors">Sales</Link>
                        </nav>
                        <UserMenu
                            isAuthenticated={user != null}
                            userImage={user?.photoURL}
                            userName={user?.displayName}
                        />
                        <div className="relative">
                            <button
                                className="relative text-gray-700 hover:text-primary transition-colors"
                                onClick={() => setIsCartOpen((v) => !v)}
                                aria-label="Open cart preview"
                            >
                                <ShoppingCart className="h-5 w-5" />
                                {cartItemsCount > 0 && (
                                    <span className="absolute -top-2 -right-2 flex items-center justify-center w-4 h-4 text-[10px] text-white bg-primary rounded-full">
                                        {cartItemsCount}
                                    </span>
                                )}
                            </button>
                            {isCartOpen && <CartPreview />}
                        </div>
                    </div>
                </div>
                {/* Desktop Navigation (replaces navLinks) */}
                <div className="hidden lg:block border-t border-gray-100">
                    <DesktopNavigation
                        mainCategories={mainCategories}
                        level_one_categories={levelOneCategories}
                        level_two_categories={levelTwoCategories}
                        hoveredCategory={hoveredCategory}
                        setHoveredCategory={setHoveredCategory}
                    />
                </div>
            </header>
            {/* Mobile: Search bar below header */}
            <div className="hidden   bg-white px-4 pt-2 pb-1 border-b border-gray-100">
                <SearchBar />
            </div>
            <MobileMenu
                isOpen={isMenuOpen}
                onClose={() => setIsMenuOpen(false)}
                mainCategories={mainCategories}
                levelOneCategories={levelOneCategories}
                levelTwoCategories={levelTwoCategories}
                utilityLinks={[
                    { name: "About", href: "/about" },
                    { name: "Contact Us", href: "/contact" },
                    { name: "Sales", href: "/deals" }
                ]}
                logo={
                    <div className="relative h-12 w-24">
                        <Image
                            src={logoUrl}
                            alt="Afrifurn Logo"
                            fill
                            className="object-contain"
                            priority
                            sizes="96px"
                            quality={90}
                        />
                    </div>
                }
            />
            <MobileSearchModal />
        </>
    );
};

export default Header
