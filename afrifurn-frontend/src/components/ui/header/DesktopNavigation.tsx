'use client'
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
    const [hoveredLevelOne, setHoveredLevelOne] = useState<string | null>(null);

    // Get level one categories filtered by main category
    const getLevelOneByMainCategory = (mainCategoryId: string) => {
        return level_one_categories?.filter(cat => cat.category?._id === mainCategoryId) || [];
    };

    // Get level two categories filtered by level one category
    const getLevelTwoByLevelOne = (levelOneCategoryId: string) => {
        return level_two_categories?.filter(cat => cat.level_one_category._id === levelOneCategoryId) || [];
    };

    return (
        <nav className="hidden lg:block py-1">
            <div className="flex justify-center">
                <ul className="flex items-center gap-1">
                    {mainCategories?.map((category) => (
                        <li
                            key={category._id}
                            className="relative px-4"
                            onMouseEnter={() => setHoveredCategory(category._id)}
                            onMouseLeave={() => setHoveredCategory(null)}
                        >
                            <Link 
                                href={`/category/${category.short_name}`} 
                                className={`
                                    flex items-center px-4 py-2.5 text-xl font-medium tracking-wide
                                    transition-colors duration-200 uppercase
                                    ${hoveredCategory === category._id 
                                        ? 'text-primary' 
                                        : 'text-gray-600 hover:text-primary'}
                                `}
                            >
                                {category.name}
                                <ChevronDown className={`
                                    ml-1 h-5 w-5 transition-transform duration-200
                                    ${hoveredCategory === category._id ? 'rotate-180' : ''}
                                `} />
                            </Link>

                            {/* Redesigned Mega menu dropdown with 3-column grid */}
                            <div 
                                className={`
                                    absolute left-1/2 -translate-x-1/2 mt-1 w-[1000px] bg-white rounded-xl shadow-2xl
                                    transition-all duration-300 ease-in-out transform origin-top z-50
                                    border border-gray-100 overflow-hidden
                                    ${hoveredCategory === category._id 
                                        ? 'opacity-100 visible scale-100' 
                                        : 'opacity-0 invisible scale-95 pointer-events-none'}
                                `}
                                onMouseEnter={() => setHoveredCategory(category._id)}
                                onMouseLeave={() => setHoveredCategory(null)}
                            >
                                <div className="p-8">
                                    <h3 className="text-lg font-bold text-gray-700 uppercase mb-6 border-b pb-2">
                                        {category.name}
                                    </h3>
                                    
                                    {/* 3-column grid layout for level one categories */}
                                    <div className="grid grid-cols-3 gap-x-8 gap-y-6">
                                        {getLevelOneByMainCategory(category._id).map((levelOne) => (
                                            <div key={levelOne._id} className="space-y-3">
                                                {/* Level One Category as header */}
                                                <Link
                                                    href={`/room/${levelOne.short_name}`}
                                                    className="block text-base font-semibold text-primary hover:text-primary/80 transition-colors"
                                                >
                                                    {levelOne.name}
                                                </Link>
                                                
                                                {/* Level Two Categories as list */}
                                                <ul className="space-y-2">
                                                    {getLevelTwoByLevelOne(levelOne._id).map((levelTwo) => (
                                                        <li key={levelTwo._id}>
                                                            <Link
                                                                href={`/room/${levelOne.short_name}/${levelTwo.short_name}`}
                                                                className="group flex items-center text-sm text-gray-600 hover:text-primary transition-colors"
                                                            >
                                                                <span className="w-1.5 h-1.5 rounded-full bg-gray-300 mr-2 group-hover:bg-primary transition-colors"></span>
                                                                <span className="group-hover:translate-x-0.5 transition-transform duration-200">
                                                                    {levelTwo.name}
                                                                </span>
                                                            </Link>
                                                        </li>
                                                    ))}
                                                </ul>
                                            </div>
                                        ))}
                                    </div>
                                </div>
                                
                                {/* Featured banner with gradient */}
                                <div className="bg-gradient-to-r from-primary/5 to-primary/10 p-4 border-t border-gray-100">
                                    <div className="flex items-center justify-between">
                                        <p className="text-sm text-gray-600 font-medium">
                                            Free delivery on orders over R2000
                                        </p>
                                        <Link 
                                            href="/promotions" 
                                            className="text-sm font-medium text-primary hover:text-primary/80 transition-colors"
                                        >
                                            View current promotions →
                                        </Link>
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