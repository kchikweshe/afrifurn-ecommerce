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
        <div ref={cartRef} className="absolute right-0 mt-2 w-70 bg-white rounded-lg shadow-xl border border-gray-200 z-50 overflow-hidden">
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
                                    <div className="h-14 w-14 relative flex-shrink-0 rounded overflow-hidden">
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
                        <div className="mx-auto w-12 h-12 rounded-full bg-gray-50 flex items-center justify-center mb-3">
                            <ShoppingCart className="h-5 w-5 text-gray-400" />
                        </div>
                        <p className="text-gray-500 text-sm mb-3">Your cart is empty</p>
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

    const Logo = ({ isMobile = false }) => (
        <Link href="/" className={`${isMobile ? "md:hidden" : "hidden md:block"} flex items-center`}>
            <div className={`relative ${isMobile ? "h-14 w-40" : "h-16 w-48"}`}>
                <Image
                    src={logoUrl}
                    alt="AfrifurnShop Logo"
                    fill
                    className="object-contain"
                    priority
                    sizes={isMobile ? "128px" : "192px"}
                    quality={90}
                />
            </div>
        </Link>
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
            <header className="bg-white shadow-sm w-full z-50">
                <div className="container mx-auto flex items-center justify-between py-2 px-2 md:py-4 md:px-4 gap-2">
                    {/* Logo */}
                    <div className="relative h-10 w-28 flex-shrink-0 flex items-center justify-center md:justify-start">
                        <Logo />
                    </div>
                    <div className="sm:hidden flex bg-white px-2 pt-2 pb-1">
                        <SearchBar />
                    </div>
                    {/* Icons (user, wishlist, cart, menu) */}
                    <div className="flex items-center gap-2 sm:gap-4 md:gap-6 flex-shrink-0">
                        {/* User */}
                        <div className=" sm:block">
                            <UserMenu
                                isAuthenticated={user != null}
                                userImage={user?.photoURL}
                                userName={user?.displayName}
                            />
                        </div>

                        {/* Cart */}
                        <div className="relative">
                            <button
                                className="relative text-gray-700 hover:text-primary transition-colors"
                                onClick={() => setIsCartOpen((v) => !v)}
                                aria-label="Open cart preview"
                            >
                                <ShoppingCart className="h-6 w-6" />
                                {cartItemsCount > 0 && (
                                    <span className="absolute -top-2 -right-2 flex items-center justify-center w-5 h-5 text-xs text-white bg-primary rounded-full">
                                        {cartItemsCount}
                                    </span>
                                )}
                            </button>
                            {isCartOpen && <CartPreview />}
                        </div>
                        {/* Mobile menu button */}
                        <Button
                            variant="ghost"
                            size="icon"
                            className="h-8 w-8 md:hidden"
                            onClick={() => setIsMenuOpen(true)}
                        >
                            <Menu className="h-5 w-5 text-gray-700" />
                        </Button>
                    </div>
                </div>
                {/* Desktop Navigation (replaces navLinks) */}
                <div className="hidden lg:block">
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
            <div className="md:hidden block  bg-white px-2 pt-2 pb-1">
                <SearchBar />
            </div>
            {/* Spacer for fixed header if needed */}
            <div className="h-20 md:h-28" />
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
                    <div className="relative h-10 w-28">
                        <Image
                            src={logoUrl}
                            alt="Afrifurn Logo"
                            fill
                            className="object-contain"
                            priority
                            sizes="112px"
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
