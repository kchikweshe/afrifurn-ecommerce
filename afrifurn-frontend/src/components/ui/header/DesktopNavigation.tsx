'use client'
import { useRef } from 'react';
import { Category, Level1Category, Level2Category } from '@/types';
import Link from 'next/link';
import React, { useState } from 'react';
import { ChevronDown } from 'lucide-react';

interface DesktopNavigationProps {
    mainCategories: Category[]|undefined;
    level_one_categories: Level1Category[]|undefined;
    level_two_categories: Level2Category[]|undefined;
    hoveredCategory: string | null;
    setHoveredCategory: (data: string | null) => void;
}

const DesktopNavigation: React.FC<DesktopNavigationProps> = ({
    mainCategories,
    level_one_categories,
    level_two_categories,
    hoveredCategory,
    setHoveredCategory
}) => {
    // Hover delay logic
    const timeoutRef = useRef<NodeJS.Timeout | null>(null);

    const handleMouseEnter = (catId: string) => {
        if (timeoutRef.current) clearTimeout(timeoutRef.current);
        setHoveredCategory(catId);
    };

    const handleMouseLeave = () => {
        timeoutRef.current = setTimeout(() => {
            setHoveredCategory(null);
        }, 200); // 200ms delay before hiding
    };

    // Get level one categories filtered by main category
    const getLevelOneByMainCategory = (mainCategoryId: string) => {
        return level_one_categories?.filter(cat => cat.category?._id === mainCategoryId) || [];
    };

    // Get level two categories filtered by level one category
    const getLevelTwoByLevelOne = (levelOneCategoryId: string) => {
        return level_two_categories?.filter(cat => cat.level_one_category._id === levelOneCategoryId) || [];
    };

    return (
        <nav className="hidden lg:block py-1 w-full relative z-50">
            <div className="flex justify-center w-full">
                <ul className="flex items-center gap-4">
                    {mainCategories?.map((category) => (
                        <li
                            key={category._id}
                            className="relative"
                            onMouseEnter={() => handleMouseEnter(category._id)}
                            onMouseLeave={handleMouseLeave}
                        >
                            <Link
                                href={`/category/${category.short_name}`}
                                className={`
                                    flex items-center px-4 py-3 text-lg font-bold tracking-wide
                                    transition-colors duration-200 uppercase
                                    ${hoveredCategory === category._id
                                        ? 'text-primary'
                                        : 'text-gray-700 hover:text-primary'}
                                `}
                            >
                                {category.name}
                                <ChevronDown className={`
                                    ml-2 h-5 w-5 transition-transform duration-200
                                    ${hoveredCategory === category._id ? 'rotate-180' : ''}
                                `} />
                            </Link>

                            {/* Mega menu dropdown */}
                            <div
                                className={`
                                    absolute left-1/2 -translate-x-1/2 mt-2
                                    w-[1100px] max-w-screen-xl
                                    bg-white rounded-2xl shadow-2xl border border-gray-100
                                    transition-all duration-300 ease-in-out transform origin-top z-50
                                    overflow-hidden
                                    ${hoveredCategory === category._id
                                        ? 'opacity-100 visible scale-100 pointer-events-auto'
                                        : 'opacity-0 invisible scale-95 pointer-events-none'}
                                `}
                                style={{ minWidth: 600 }}
                                onMouseEnter={() => handleMouseEnter(category._id)}
                                onMouseLeave={handleMouseLeave}
                            >
                                {/* Arrow pointer */}
                                <div className="absolute top-0 left-1/2 -translate-x-1/2 -translate-y-1/2">
                                    <div className="w-4 h-4 bg-white border-t border-l border-gray-100 rotate-45 shadow-md"></div>
                                </div>
                                <div className="p-12 pt-8">
                                    <div className="grid grid-cols-5 gap-x-12 gap-y-10">
                                        {getLevelOneByMainCategory(category._id).map((levelOne) => (
                                            <div key={levelOne._id} className="space-y-5">
                                                {/* Level One Category as header */}
                                                <Link
                                                    href={`/room/${levelOne.short_name}`}
                                                    className="block text-xl font-extrabold text-gray-900 mb-3 hover:text-primary transition-colors"
                                                >
                                                    {levelOne.name}
                                                </Link>
                                                {/* Level Two Categories as list */}
                                                <ul className="space-y-3 mb-2">
                                                    {getLevelTwoByLevelOne(levelOne._id).map((levelTwo) => (
                                                        <li key={levelTwo._id}>
                                                            <Link
                                                                href={`/room/${levelOne.short_name}/${levelTwo.short_name}`}
                                                                className="block text-sm text-gray-700 hover:text-primary transition-colors pl-2"
                                                            >
                                                                {levelTwo.name}
                                                            </Link>
                                                        </li>
                                                    ))}
                                                </ul>
                                                {/* View All link */}
                                                <Link
                                                    href={`/room/${levelOne.short_name}`}
                                                    className="block text-sm text-primary font-semibold mt-4 hover:underline"
                                                >
                                                    View All &rarr;
                                                </Link>
                                            </div>
                                        ))}
                                    </div>
                                </div>
                                {/* Promotional banner at the bottom */}
                                <div className="bg-gray-50 p-6 border-t border-gray-100">
                                    <div className="flex items-center justify-between">
                                        <p className="text-lg text-gray-600 font-medium">
                                            {/* You can add a promo or info here */}
                                        </p>
                                    </div>
                                </div>
                            </div>
                        </li>
                    ))}
                </ul>
            </div>
        </nav>
    );
};

export default DesktopNavigation;