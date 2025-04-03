'use client'

import React, { useState } from 'react'
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
    const state = useDataContext();
    const { cartItems } = useCart();
    const cartItemsCount = cartItems.length;
    const [isMenuOpen, setIsMenuOpen] = useState(false);
    const [hoveredCategory, setHoveredCategory] = useState<string | null>(null);
    const [isCartOpen, setIsCartOpen] = useState(false);
    const { user } = useAuthContext()
    const [isSearchOpen, setIsSearchOpen] = useState(false);

    if (state == null) return <div>Loading...</div>;

    const { levelOneCategories, levelTwoCategories, mainCategories } = state;

    // Add utility links data
    const utilityLinks = [
        { name: "About", href: "/about" },
        { name: "Contact Us", href: "/contact" },
    ];

    const CartPreview = () => (
        <div className="absolute right-0 mt-2 w-70 bg-white rounded-lg shadow-xl border border-gray-200 z-50 overflow-hidden">
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
            <header className="fixed top-0 left-0 right-0 z-50 w-full lg:p-3 bg-white shadow-md">
                <div className="container mx-auto">
                    {/* Main header bar */}
                    <div className="flex items-center h-20 px-2">
                        {/* Left section - Desktop Logo */}
                        <div className="hidden md:flex items-center gap-3 flex-grow-0">
                            <Logo isMobile={false} />
                        </div>

                        {/* Mobile header layout */}
                        <div className="flex items-center justify-between w-full md:hidden">
                            {/* Mobile Logo */}
                            <Logo isMobile={true} />
                            
                            {/* Mobile actions group */}
                            <div className="flex items-center gap-2">
                                <Button
                                    variant="ghost"
                                    size="icon"
                                    className="h-8 w-8"
                                    onClick={() => setIsSearchOpen(true)}
                                >
                                    <Search className="h-5 w-5 text-gray-700" />
                                </Button>

                                

                                <div className="relative">
                                    <Button
                                        variant="ghost"
                                        size="icon"
                                        className="rounded-full w-8 h-8 hover:bg-gray-100"
                                        onClick={() => setIsCartOpen(!isCartOpen)}
                                    >
                                        <ShoppingCart className="h-4 w-4 text-gray-700" />
                                        {cartItemsCount > 0 && (
                                            <span className="absolute -top-1 -right-1 flex items-center justify-center w-4 h-4 text-xs text-white bg-primary rounded-full">
                                                {cartItemsCount}
                                            </span>
                                        )}
                                    </Button>
                                    {isCartOpen && <CartPreview />}
                                </div>
                                <div className="relative">
                                    <UserMenu
                                        isAuthenticated={user != null}
                                        userImage={user?.photoURL}
                                        userName={user?.displayName}
                                    />
                                </div>
                                <Button
                                    variant="ghost"
                                    size="icon"
                                    className="h-8 w-8"
                                    onClick={() => setIsMenuOpen(!isMenuOpen)}
                                >
                                    <Menu className="h-5 w-5 text-gray-700" />
                                </Button>
                            </div>
                        </div>

                        {/* Center section - Desktop Search */}
                        <div className="flex-1 px-4 max-w-3xl mx-auto hidden md:block">
                            <SearchBar />
                        </div>

                        {/* Right section - Desktop only */}
                        <div className="hidden md:flex items-center gap-3">
                            {/* Utility Links */}
                            <nav className="hidden lg:flex items-center gap-4 mr-2">
                                {utilityLinks.map((link) => (
                                    <Link
                                        key={link.name}
                                        href={link.href}
                                        className="uppercase font-medium text-gray-600 hover:text-primary transition-colors"
                                    >
                                        {link.name}
                                    </Link>
                                ))}
                            </nav>
                            
                            {/* User menu */}
                            <div className="relative">
                                <UserMenu
                                    isAuthenticated={user != null}
                                    userImage={user?.photoURL}
                                    userName={user?.displayName}
                                />
                            </div>

                            {/* Cart */}
                            <div className="relative">
                                <Button
                                    variant="ghost"
                                    size="icon"
                                    className="rounded-full w-8 h-8 hover:bg-gray-100"
                                    onClick={() => setIsCartOpen(!isCartOpen)}
                                >
                                    <ShoppingCart className="h-4 w-4 text-gray-700" />
                                    {cartItemsCount > 0 && (
                                        <span className="absolute -top-1 -right-1 flex items-center justify-center w-4 h-4 text-xs text-white bg-primary rounded-full">
                                            {cartItemsCount}
                                        </span>
                                    )}
                                </Button>
                                {isCartOpen && <CartPreview />}
                            </div>
                        </div>
                    </div>

                    {/* Navigation bar - desktop only */}
                    <div className="hidden md:block ">
                        <div className="h-10">
                            <DesktopNavigation
                                mainCategories={mainCategories}
                                level_one_categories={levelOneCategories}
                                level_two_categories={levelTwoCategories}
                                hoveredCategory={hoveredCategory}
                                setHoveredCategory={setHoveredCategory}
                            />
                        </div>
                    </div>
                </div>

                {/* Mobile menu */}
                <MobileMenu
                    isOpen={isMenuOpen}
                    onClose={() => setIsMenuOpen(false)}
                    mainCategories={mainCategories}
                    levelOneCategories={levelOneCategories}
                    levelTwoCategories={levelTwoCategories}
                    utilityLinks={utilityLinks}
                    logo={<Logo isMobile />}
                />
            </header>
            <div className="h-20 md:h-[128px]" /> {/* Spacer for fixed header */}

            <MobileSearchModal />
        </>
    );
};

export default Header
