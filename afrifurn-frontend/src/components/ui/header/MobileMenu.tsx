'use client'
import React from 'react';
import Link from 'next/link';
import Image from 'next/image';
import { X, User, ChevronRight, Truck } from 'lucide-react';
import { Category } from '@/types';

interface UtilityLink {
    name: string;
    href: string;
}

interface MobileMenuProps {
    isOpen: boolean;
    onClose: () => void;
    mainCategories: Category[] | undefined;
    utilityLinks?: UtilityLink[];
    logo?: React.ReactNode;
}

const MobileMenu: React.FC<MobileMenuProps> = ({
    isOpen,
    onClose,
    mainCategories,
    utilityLinks = [],
    logo,
}) => {
    if (!isOpen) return null;

    return (
        <div className="fixed inset-0 z-50 bg-white flex flex-col">
            {/* Header */}
            <div className="flex items-center justify-between px-4 py-4 border-b">
                <div className="flex items-center">
                    {logo ? (
                        <div className="h-10 w-28 flex items-center">{logo}</div>
                    ) : (
                        <Image src="/logo.svg" alt="Logo" width={100} height={40} />
                    )}
                </div>
                <div className="flex items-center gap-4">
                    <Link href="/profile" onClick={onClose} className="p-2 rounded-full hover:bg-gray-100">
                        <User className="h-7 w-7 text-gray-700" />
                    </Link>
                    <button onClick={onClose} className="p-2 rounded-full hover:bg-gray-100">
                        <X className="h-7 w-7 text-gray-700" />
                    </button>
                </div>
            </div>

            {/* Main Categories */}
            <nav className="flex-1 overflow-y-auto">
                <ul className="py-2">
                    {mainCategories?.map((cat) => (
                        <li key={cat._id}>
                            <Link
                                href={`/category/${cat.short_name}`}
                                onClick={onClose}
                                className="flex items-center justify-between px-6 py-4 text-lg font-bold text-gray-900 hover:bg-gray-50 transition-colors"
                            >
                                {cat.name}
                                <ChevronRight className="h-5 w-5 text-gray-400" />
                            </Link>
                        </li>
                    ))}
                </ul>
            </nav>

            {/* Utility Links */}
            <div className="border-t">
                {utilityLinks.map((link) => (
                    <Link
                        key={link.name}
                        href={link.href}
                        className="flex items-center px-6 py-4 text-base text-gray-700 hover:bg-gray-50 transition-colors"
                        onClick={onClose}
                    >
                        {link.name}
                        <ChevronRight className="ml-auto h-5 w-5 text-gray-400" />
                    </Link>
                ))}
            </div>

            {/* Delivery Info */}
            <div className="bg-gray-50 border-t flex items-center px-6 py-3 text-sm text-gray-700">
                <Truck className="h-5 w-5 mr-2 text-gray-500" />
                Standard delivery starting at $19
            </div>
        </div>
    );
};

export default MobileMenu;