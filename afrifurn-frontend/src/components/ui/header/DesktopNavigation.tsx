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

                            {/* Mega menu dropdown */}
                            <div 
                                className={`
                                    absolute left-1/2  -translate-x-1/2 mt-0.5 w-[1000px] bg-white rounded-lg shadow-xl border border-gray-200
                                    transition-all duration-200 ease-in-out transform origin-top z-50
                                    ${hoveredCategory === category._id 
                                        ? 'opacity-100 visible scale-100' 
                                        : 'opacity-0 invisible scale-95'}
                                `}
                                onMouseEnter={() => setHoveredCategory(category._id)}
                                onMouseLeave={() => setHoveredCategory(null)}
                            >
                                <div className="flex p-6">
                                    {/* Level One Categories Column */}
                                    <div className="w-1/3 border-r border-gray-100 pr-6">
                                        <h3 className="text-sm font-semibold text-gray-400 uppercase mb-4">
                                            {category.name} Categories
                                        </h3>
                                        <ul>
                                            {getLevelOneByMainCategory(category._id).map((levelOne) => (
                                                <li 
                                                    key={levelOne._id}
                                                    className="mb-1"
                                                    onMouseEnter={() => setHoveredLevelOne(levelOne._id)}
                                                >
                                                    <Link
                                                        href={`/room/${levelOne.short_name}`}
                                                        className={`
                                                            block px-3 py-2 rounded-md text-base
                                                            transition-colors duration-150
                                                            ${hoveredLevelOne === levelOne._id 
                                                                ? 'bg-gray-50 text-primary font-medium' 
                                                                : 'text-gray-700 hover:bg-gray-50 hover:text-primary'}
                                                        `}
                                                    >
                                                        {levelOne.name}
                                                    </Link>
                                                </li>
                                            ))}
                                        </ul>
                                    </div>

                                    {/* Level Two Categories Column */}
                                    <div className="w-2/3 pl-6">
                                        {hoveredLevelOne ? (
                                            <>
                                                <h3 className="text-sm font-semibold text-gray-400 uppercase mb-4">
                                                    {level_one_categories?.find(c => c._id === hoveredLevelOne)?.name} Subcategories
                                                </h3>
                                                <div className="grid grid-cols-2 gap-x-6 gap-y-2">
                                                    {getLevelTwoByLevelOne(hoveredLevelOne).map((levelTwo) => (
                                                        <Link
                                                            key={levelTwo._id}
                                                            href={`/room/${level_one_categories?.find(c => c._id === hoveredLevelOne)?.short_name}/${levelTwo.short_name}`}
                                                            className="
                                                                px-3 py-2 text-gray-600 hover:text-primary
                                                                transition-colors duration-150 rounded-md hover:bg-gray-50
                                                            "
                                                        >
                                                            {levelTwo.name}
                                                        </Link>
                                                    ))}
                                                </div>
                                            </>
                                        ) : (
                                            <div className="h-full flex items-center justify-center text-gray-400">
                                                <p>Hover over a category to see subcategories</p>
                                            </div>
                                        )}
                                    </div>
                                </div>
                                
                                {/* Featured or promotional content could go here */}
                                <div className="bg-gray-50 p-4 rounded-b-lg border-t border-gray-100">
                                    <p className="text-sm text-gray-500 text-center">
                                        Explore our collection of premium furniture for your home
                                    </p>
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