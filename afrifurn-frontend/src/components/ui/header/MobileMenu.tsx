'use client'
import React, { useState } from 'react';
import Link from 'next/link';
import Image from 'next/image';
import { X, User, ChevronRight, Truck, ChevronLeft } from 'lucide-react';
import { Category, Level1Category, Level2Category } from '@/types';

interface UtilityLink {
    name: string;
    href: string;
}

interface MobileMenuProps {
    isOpen: boolean;
    onClose: () => void;
    mainCategories: Category[] | undefined;
    levelOneCategories?: Level1Category[];
    levelTwoCategories?: Level2Category[];
    utilityLinks?: UtilityLink[];
    logo?: React.ReactNode;
}

const MobileMenu: React.FC<MobileMenuProps> = ({
    isOpen,
    onClose,
    mainCategories,
    levelOneCategories = [],
    levelTwoCategories = [],
    utilityLinks = [],
    logo,
}) => {
    const [activeMainCategory, setActiveMainCategory] = useState<Category | null>(null);
    const [activeLevel1Category, setActiveLevel1Category] = useState<Level1Category | null>(null);

    if (!isOpen) return null;

    // Helper functions
    const getLevelOneByMainCategory = (mainCategoryId: string) =>
        levelOneCategories.filter(cat => cat.category?._id === mainCategoryId);
    const getLevelTwoByLevelOne = (levelOneCategoryId: string) =>
        levelTwoCategories.filter(cat => cat.level_one_category._id === levelOneCategoryId);

    // Navigation logic
    let content;
    if (activeLevel1Category) {
        // Show level two categories
        const levelTwo = getLevelTwoByLevelOne(activeLevel1Category._id);
        content = (
            <>
                <div className="flex items-center px-4 py-3 border-b">
                    <button onClick={() => setActiveLevel1Category(null)} className="p-2 mr-2 rounded-full hover:bg-gray-100">
                        <ChevronLeft className="h-5 w-5 text-gray-700" />
                    </button>
                    <span className="text-base font-bold text-gray-900">{activeLevel1Category.name}</span>
                </div>
                <ul className="py-2">
                    {levelTwo.map((cat) => (
                        <li key={cat._id}>
                            <Link
                                href={`/room/${activeLevel1Category.short_name}/${cat.short_name}`}
                                onClick={onClose}
                                className="flex items-center px-8 py-3 text-base text-gray-700 hover:bg-gray-50 transition-colors"
                            >
                                {cat.name}
                            </Link>
                        </li>
                    ))}
                </ul>
            </>
        );
    } else if (activeMainCategory) {
        // Show level one categories
        const levelOne = getLevelOneByMainCategory(activeMainCategory._id);
        content = (
            <>
                <div className="flex items-center px-4 py-3 border-b">
                    <button onClick={() => setActiveMainCategory(null)} className="p-2 mr-2 rounded-full hover:bg-gray-100">
                        <ChevronLeft className="h-5 w-5 text-gray-700" />
                    </button>
                    <span className="text-lg font-bold text-gray-900">{activeMainCategory.name}</span>
                </div>
                <ul className="py-2">
                    {levelOne.map((cat) => (
                        <li key={cat._id}>
                            <button
                                onClick={() => setActiveLevel1Category(cat)}
                                className="flex items-center justify-between w-full px-6 py-4 text-base text-gray-900 hover:bg-gray-50 transition-colors"
                            >
                                {cat.name}
                                <ChevronRight className="h-5 w-5 text-gray-400" />
                            </button>
                        </li>
                    ))}
                </ul>
            </>
        );
    } else {
        // Show main categories
        content = (
            <ul className="py-2">
                {mainCategories?.map((cat) => (
                    <li key={cat._id}>
                        <button
                            onClick={() => setActiveMainCategory(cat)}
                            className="flex items-center justify-between w-full px-6 py-4 text-lg font-bold text-gray-900 hover:bg-gray-50 transition-colors"
                        >
                            {cat.name}
                            <ChevronRight className="h-5 w-5 text-gray-400" />
                        </button>
                    </li>
                ))}
            </ul>
        );
    }

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

            {/* Navigation (main, level one, level two) */}
            <nav className="flex-1 overflow-y-auto">
                {content}
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