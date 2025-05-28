'use client'
import React, { useState } from 'react';
import { Sheet, SheetContent, SheetHeader, SheetTitle } from "@/components/ui/sheet";
import Link from 'next/link';
import { ChevronRight, Home, Info, Phone, Tag } from 'lucide-react';
import { Category, Level1Category, Level2Category } from '@/types';
import { useAuth } from '@/data/hooks/useAuth';

interface UtilityLink {
    name: string;
    href: string;
}

interface MobileMenuProps {
    isOpen: boolean;
    onClose: () => void;
    mainCategories: Category[]|undefined;
    levelOneCategories: Level1Category[]|undefined;
    levelTwoCategories: Level2Category[]|undefined;
    utilityLinks?: UtilityLink[];
    logo?: React.ReactNode;
    user?: {
        displayName: string | null;
        photoURL: string | null;
        email: string | null;
    } | null;
}

const MobileMenu: React.FC<MobileMenuProps> = ({ 
    isOpen, 
    onClose,        
    levelOneCategories,
    levelTwoCategories,
    mainCategories,
    utilityLinks = [],
    logo,
   
}) => {
    const [activeMainCategory, setActiveMainCategory] = useState<Category | null>(null);
    const [activeLevel1Category, setActiveLevel1Category] = useState<Level1Category | null>(null);
     const {user}=useAuth()
    const handleMainCategoryClick = (category: Category) => {
        setActiveMainCategory(activeMainCategory?._id === category._id ? null : category);
        setActiveLevel1Category(null); // Reset level 1 when changing main category
    };

    const handleLevel1CategoryClick = (category: Level1Category) => {
        setActiveLevel1Category(activeLevel1Category?._id === category._id ? null : category);
    };

    // Helper function to get icon for utility links
    const getUtilityIcon = (name: string) => {
        switch (name.toLowerCase()) {
            case 'about':
                return <Info className="h-6 w-6 text-gray-600" />;
            case 'contact us':
                return <Phone className="h-6 w-6 text-gray-600" />;
            case 'sales':
                return <Tag className="h-6 w-6 text-gray-600" />;
            default:
                return <ChevronRight className="h-6 w-6 text-gray-600" />;
        }
    };

    return (
        <Sheet open={isOpen} onOpenChange={onClose}>
            <SheetContent 
                side="left" 
                className="w-full sm:w-[380px] p-0 flex flex-col"
            >
                {/* Header Section */}
                <SheetHeader className="p-4 border-b">
                    <div className="flex items-center justify-between w-full">
                        <SheetTitle className="text-lg font-semibold">                        {logo && <div className="flex-shrink-0">{logo}</div>}
                        </SheetTitle>
                    </div>
                </SheetHeader>

                {/* User Profile Section */}
                <div className="px-4 py-3 border-b bg-gray-50">
                    {user ? (
                        <div className="flex items-center space-x-3">
                            <div className="w-10 h-10 rounded-full overflow-hidden">
                                {user.photoURL ? (
                                    <img src={user.photoURL} alt={user.displayName || ''} className="w-full h-full object-cover" />
                                ) : (
                                    <div className="w-full h-full bg-primary/10 flex items-center justify-center">
                                        <span className="text-primary text-lg font-medium">
                                            {user.displayName?.[0]?.toUpperCase() || 'U'}
                                        </span>
                                    </div>
                                )}
                            </div>
                            <div className="flex-1">
                                <p className="font-medium text-gray-900">{user.displayName}</p>
                                <p className="text-sm text-gray-500">{user.email}</p>
                            </div>
                        </div>
                    ) : (
                        <div className="flex items-center justify-between">
                            <span className="text-gray-600">Welcome, Guest</span>
                            <Link 
                                href="/auth/signin" 
                                className="text-primary hover:text-primary/80 text-sm font-medium"
                                onClick={onClose}
                            >
                                Sign In
                            </Link>
                        </div>
                    )}
                </div>

                {/* Navigation Menu */}
                <div className="flex-1 overflow-y-auto">
                    <div className="divide-y divide-gray-100">
                        {mainCategories?.map((mainCategory) => (
                            <div key={mainCategory._id}>
                                <button
                                    onClick={() => handleMainCategoryClick(mainCategory)}
                                    className="flex items-center justify-between w-full px-4 py-3 hover:bg-gray-50 transition-colors"
                                >
                                    <span className="text-base font-medium">{mainCategory.name}</span>
                                    <ChevronRight 
                                        className={`h-5 w-5 text-gray-400 transition-transform duration-200
                                            ${activeMainCategory?._id === mainCategory._id ? 'rotate-90' : ''}
                                        `}
                                    />
                                </button>

                                {/* Level One Categories */}
                                <div className={`
                                    overflow-hidden transition-all duration-200 ease-in-out bg-gray-50
                                    ${activeMainCategory?._id === mainCategory._id ? 'max-h-[1600px]' : 'max-h-0'}
                                `}>
                                    {levelOneCategories
                                        ?.filter((c) => c.category._id === mainCategory._id)
                                        .map((level1Category) => (
                                            <div key={level1Category._id}>
                                                <button
                                                    onClick={() => handleLevel1CategoryClick(level1Category)}
                                                    className="flex items-center justify-between w-full pl-12 pr-6 py-4 text-base text-gray-600 hover:bg-gray-100 transition-colors"
                                                >
                                                    <span>{level1Category.name}</span>
                                                    <ChevronRight 
                                                        className={`h-5 w-5 text-gray-400 transition-transform duration-300
                                                            ${activeLevel1Category?._id === level1Category._id ? 'rotate-90' : ''}
                                                        `}
                                                    />
                                                </button>

                                                <div className={`
                                                    overflow-hidden transition-all duration-300 ease-in-out bg-gray-100
                                                    ${activeLevel1Category?._id === level1Category._id ? 'max-h-[800px]' : 'max-h-0'}
                                                `}>
                                                    {levelTwoCategories
                                                        ?.filter((c) => c.level_one_category._id === level1Category._id)
                                                        .map((level2Category) => (
                                                            <Link
                                                                key={level2Category._id}
                                                                href={`/room/${level1Category.short_name}/${level2Category.short_name}`}
                                                                className="block pl-20 pr-6 py-4 text-base text-gray-600 hover:bg-gray-100 hover:text-primary transition-colors"
                                                                onClick={onClose}
                                                            >
                                                                {level2Category.name}
                                                            </Link>
                                                        ))}
                                                </div>
                                            </div>
                                        ))}
                                </div>
                            </div>
                        ))}
                    </div>
                </div>

                {/* Utility Links Footer */}
                <div className="border-t mt-auto">
                    {utilityLinks.map((link) => (
                        <Link 
                            key={link.name} 
                            href={link.href} 
                            className="flex items-center px-4 py-3 text-gray-600 hover:bg-gray-50 transition-colors"
                            onClick={onClose}
                        >
                            {getUtilityIcon(link.name)}
                            <span className="ml-3 text-sm font-medium">{link.name}</span>
                        </Link>
                    ))}
                </div>
            </SheetContent>
        </Sheet>
    );
};

export default MobileMenu;