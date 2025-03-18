import React, { useState, useRef, useEffect } from 'react';
import { ChevronDown, Menu, X } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";
import { Menu as HeadlessMenu } from '@headlessui/react';
import { Category, Level1Category } from '@/types';
export const MenuItems = ({ 
  parentCategories, 
  filteredCategories, 
  handleLinkClick 
}: {
  parentCategories: Level1Category[];
  filteredCategories: Function;
  handleLinkClick: Function;
}) => {
  const [dropdownOpen, setDropdownOpen] = useState<string | null>(null);
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const dropdownRef = useRef<HTMLDivElement>(null);
  const timeoutRef = useRef<NodeJS.Timeout | null>(null);

  useEffect(() => {
    const handleClickOutside = (event:MouseEvent) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        closeDropdown();
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
      if (timeoutRef.current) clearTimeout(timeoutRef.current);
    };
  }, []);

  const openDropdown = (categoryId:string) => {
    if (timeoutRef.current) clearTimeout(timeoutRef.current);
    setDropdownOpen(categoryId);
  };

  const closeDropdown = () => {
    timeoutRef.current = setTimeout(() => {
      setDropdownOpen(null);
    }, 150); // Delay before closing
  };

  const handleKeyDown = (e:KeyboardEvent, categoryId:string) => {
    if (e.key === 'Enter' || e.key === ' ') {
      e.preventDefault();
      setDropdownOpen(categoryId === dropdownOpen ? null : categoryId);
    }
  };

  const NavLink = ({ href, children }: { href: string, children: React.ReactNode }) => (
    <a href={href} className="text-gray-700 hover:text-blue-600 font-semibold transition-colors duration-300">
      {children}
    </a>
  );

  const DesktopMenu = () => (
    <div className="hidden lg:flex justify-center items-center space-x-8">
      <NavLink href="/">Home</NavLink>
      {parentCategories.map((category) => (
        <div 
          key={category._id} 
          className="relative"
          onMouseEnter={() => openDropdown(category._id)}
          onMouseLeave={closeDropdown}
        >
          <button 
            className="flex items-center space-x-1 text-gray-700 hover:text-blue-600 font-semibold transition-colors duration-300"
            onKeyDown={(e:any) => handleKeyDown(e, category._id)}
            aria-haspopup="true"
            aria-expanded={dropdownOpen === category._id}
          >
            <span>{category.name}</span>
            <ChevronDown size={16} />
          </button>
          <AnimatePresence>
            {dropdownOpen === category._id && (
              <motion.div 
                ref={dropdownRef}
                initial={{ opacity: 0, y: -10 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -10 }}
                transition={{ duration: 0.2 }}
                // onMouseEnter={() => openDropdown(category._id)}
                // onMouseLeave={closeDropdown}
              >
                <h3 className="text-xl font-bold mb-4 text-blue-600">{category.name}</h3>
                <div className="grid grid-cols-4 gap-4">
                  {filteredCategories(category._id).map((subCategory:Category) => (
                    <a
                      key={subCategory._id}
                      href={`/shop/${subCategory.name}`}
                      className="text-gray-600 hover:text-blue-600 transition-colors duration-300"
                      onClick={(e) => handleLinkClick(e, `/shop/${subCategory._id}`)}
                    >
                      {subCategory.name}
                    </a>
                  ))}
                </div>
              </motion.div>
            )}
          </AnimatePresence>
        </div>
      ))}
      <NavLink href="/contact">Contact us</NavLink>
    </div>
  );

  const MobileMenu = () => (
    <HeadlessMenu as="div" className="lg:hidden">
      {({ open }) => (
        <>
          <HeadlessMenu.Button className="text-gray-700 hover:text-blue-600 transition-colors duration-300">
            {open ? <X size={24} /> : <Menu size={24} />}
          </HeadlessMenu.Button>
          <AnimatePresence>
            {open && (
              <motion.div
                initial={{ opacity: 0, y: -10 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -10 }}
                transition={{ duration: 0.2 }}
              >
                <HeadlessMenu.Item>
                  {({ active }) => (
                    <NavLink href="/">Home</NavLink>
                  )}
                </HeadlessMenu.Item>
                {parentCategories.map((category) => (
                  <HeadlessMenu.Item key={category._id}>
                    {({ active }) => (
                      <div className="py-2">
                        <button 
                          className="text-left w-full text-gray-700 hover:text-blue-600 font-semibold transition-colors duration-300"
                          onClick={() => setMobileMenuOpen(true)}
                        >
                          {category.name}
                        </button>
                        {mobileMenuOpen && (
                          <div className="mt-2 ml-4 space-y-2">
                            {filteredCategories(category._id).map((subCategory:Category) => (
                              <a
                                key={subCategory._id}
                                href={`/shop/${subCategory.name}`}
                                className="block text-gray-600 hover:text-blue-600 transition-colors duration-300"
                                onClick={(e) => handleLinkClick(e, `/shop/${subCategory._id}`)}
                              >
                                {subCategory.name}
                              </a>
                            ))}
                          </div>
                        )}
                      </div>
                    )}
                  </HeadlessMenu.Item>
                ))}
                <HeadlessMenu.Item>
                  {({ active }) => (
                    <NavLink href="/contact">Contact us</NavLink>
                  )}
                </HeadlessMenu.Item>
              </motion.div>
            )}
          </AnimatePresence>
        </>
      )}
    </HeadlessMenu>
  );

  return (
    <nav className="py-4 border-t border-gray-200">
      <div className="container mx-auto px-4">
        <DesktopMenu />
        {/* <MobileMenu /> */}
      </div>
    </nav>
  );
};