// MobileMenu.tsx
import React from 'react';
import { Sheet, SheetContent } from "@/components/ui/sheet";
import Link from 'next/link';
import { Menu, X } from 'lucide-react';

export const MobileMenu = ({ mobileMenuOpen, toggleMobileMenu, parentCategories, mobileExpandedCategory, toggleMobileCategory, filteredCategories, handleLinkClick }) => {
  // Render mobile menu
  return (  <Sheet open={mobileMenuOpen} onOpenChange={toggleMobileMenu}>
    <SheetContent side="left" className="w-[300px] sm:w-[400px]">
      <nav className="flex flex-col gap-4">
        {parentCategories.map((category) => (
          <div key={category.id}>
            <button
              onClick={() => toggleMobileCategory(category.id)}
              className="flex items-center justify-between w-full text-lg font-medium text-gray-700 hover:text-primary transition-colors"
            >
              {category.name}
              {mobileExpandedCategory === category.id ? <X size={20} /> : <Menu size={20} />}
            </button>
            {mobileExpandedCategory === category.id && (
              <div className="ml-4 mt-2 flex flex-col gap-2">
                {category.subcategories.map((subcat) => (
                  <Link
                    key={subcat.id}
                    href={`/category/${subcat.id}`}
                    className="text-sm text-gray-600 hover:text-primary transition-colors"
                    onClick={(e) => handleLinkClick(e, `/category/${subcat.id}`)}
                  >
                    {subcat.name}
                  </Link>
                ))}
              </div>
            )}
          </div>
        ))}
      </nav>
    </SheetContent>
  </Sheet>)
};
