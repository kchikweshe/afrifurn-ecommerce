import React, { useState } from 'react';
import { Sheet, SheetContent, SheetHeader, SheetTitle } from "@/components/ui/sheet";
import Link from 'next/link';
import { ChevronRight, Home, Info, Phone, Tag } from 'lucide-react';
import { Category, Level1Category, Level2Category } from '@/types';

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
}

const MobileMenu: React.FC<MobileMenuProps> = ({ 
    isOpen, 
    onClose,        
    levelOneCategories,
    levelTwoCategories,
    mainCategories,
    utilityLinks = [],
    logo
}) => {
    const [activeMainCategory, setActiveMainCategory] = useState<Category | null>(null);
    const [activeLevel1Category, setActiveLevel1Category] = useState<Level1Category | null>(null);

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
                className="w-full sm:w-[380px] p-0"
            >
                <SheetHeader className="p-6 border-b">
                    <div className="flex items-center justify-between w-full">
                        <SheetTitle className="text-xl font-semibold">Menu</SheetTitle>
                        {logo && <div className="flex-shrink-0">{logo}</div>}
                    </div>
                </SheetHeader>

                <div className="p-4 border-b">
                    <div className="relative">
                        <input
                            type="text"
                            placeholder="Search..."
                            className="w-full p-2 pl-10 border rounded-md focus:outline-none focus:ring-2 focus:ring-primary"
                        />
                        <svg 
                            className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" 
                            xmlns="http://www.w3.org/2000/svg" 
                            fill="none" 
                            viewBox="0 0 24 24" 
                            stroke="currentColor"
                        >
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                        </svg>
                    </div>
                </div>

                <div className="overflow-y-auto h-full">
         
                    <div className="border-t">
                        {mainCategories?.map((mainCategory) => (
                            <div key={mainCategory._id} className="border-b last:border-b-0">
                                <button
                                    onClick={() => handleMainCategoryClick(mainCategory)}
                                    className="flex items-center justify-between w-full p-6 hover:bg-gray-50 transition-colors"
                                >
                                    <span className="text-xl">{mainCategory.name}</span>
                                    <ChevronRight 
                                        className={`h-6 w-6 text-gray-400 transition-transform duration-300
                                            ${activeMainCategory?._id === mainCategory._id ? 'rotate-90' : ''}
                                        `}
                                    />
                                </button>

                                <div className={`
                                    overflow-hidden transition-all duration-300 ease-in-out bg-gray-50
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
                        <div className="border-t">  
                            {utilityLinks.length > 0 && (
                                <div className="border-t">
                                    {utilityLinks.map((link) => (
                                        <Link key={link.name} href={link.href} className="flex items-center gap-4 p-6 hover:bg-gray-50 transition-colors" onClick={onClose}>
                                            <span className="text-lg">{link.name}</span>
                                        </Link>
                                    ))}
                                </div>
                            )}
                        </div>
                    </div>
                </div>
            </SheetContent>
        </Sheet>
    );
};

export default MobileMenu;