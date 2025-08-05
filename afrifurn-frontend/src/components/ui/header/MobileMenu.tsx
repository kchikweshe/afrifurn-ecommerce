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
  mainCategories?: Category[];
  levelOneCategories?: Level1Category[];
  levelTwoCategories?: Level2Category[];
  utilityLinks?: UtilityLink[];
  logo?: React.ReactNode;
}

const MobileMenu: React.FC<MobileMenuProps> = ({
  isOpen,
  onClose,
  mainCategories = [],
  levelOneCategories = [],
  levelTwoCategories = [],
  utilityLinks = [],
  logo,
}) => {
  const [activeMainCategory, setActiveMainCategory] = useState<Category | null>(null);
  const [activeLevel1Category, setActiveLevel1Category] = useState<Level1Category | null>(null);

  if (!isOpen) return null;

  const getLevelOneByMainCategory = (mainCategoryId: string) =>
    levelOneCategories.filter(cat => cat.category?._id === mainCategoryId);

  const getLevelTwoByLevelOne = (levelOneCategoryId: string) =>
    levelTwoCategories.filter(cat => cat.level_one_category._id === levelOneCategoryId);

  // Level Two View
  const renderLevelTwo = () => {
    const levelTwo = getLevelTwoByLevelOne(activeLevel1Category!._id);
    return (
      <>
        <Header title={activeLevel1Category!.name} onBack={() => setActiveLevel1Category(null)} />
        <ul>
          {levelTwo.map(cat => (
            <li key={cat._id}>
              <Link
                href={`/room/${activeLevel1Category!.short_name}/${cat.short_name}`}
                onClick={onClose}
                className="block px-6 py-4 text-gray-700 hover:bg-gray-100 transition"
              >
                {cat.name}
              </Link>
            </li>
          ))}
        </ul>
      </>
    );
  };

  // Level One View
  const renderLevelOne = () => {
    const levelOne = getLevelOneByMainCategory(activeMainCategory!._id);
    return (
      <>
        <Header title={activeMainCategory!.name} onBack={() => setActiveMainCategory(null)} />
        <ul>
          {levelOne.map(cat => (
            <li key={cat._id}>
              <button
                onClick={() => setActiveLevel1Category(cat)}
                className="w-full px-6 py-4 flex items-center justify-between text-gray-900 hover:bg-gray-100 transition"
              >
                {cat.name}
                <ChevronRight className="w-5 h-5 text-gray-400" />
              </button>
            </li>
          ))}
        </ul>
      </>
    );
  };

  // Main Categories View
  const renderMain = () => (
    <ul>
      {mainCategories.map(cat => (
        <li key={cat._id}>
          <button
            onClick={() => setActiveMainCategory(cat)}
            className="w-full px-6 py-4 flex items-center justify-between text-lg font-semibold text-gray-900 hover:bg-gray-100 transition"
          >
            {cat.name}
            <ChevronRight className="w-5 h-5 text-gray-400" />
          </button>
        </li>
      ))}
    </ul>
  );

  return (
    <div className="fixed inset-0 z-50 bg-white flex flex-col">
      {/* Top Bar */}
      <div className="flex items-center justify-between px-4 py-3 border-b">
        <div>{logo || <Image src="/logo.svg" alt="Logo" width={160} height={40} />}</div>
        <div className="flex items-center gap-3">
          <Link href="/profile" onClick={onClose} className="p-2 rounded-full hover:bg-gray-100">
            <User className="w-6 h-6 text-gray-700" />
          </Link>
          <button onClick={onClose} className="p-2 rounded-full hover:bg-gray-100">
            <X className="w-6 h-6 text-gray-700" />
          </button>
        </div>
      </div>

      {/* Menu Content */}
      <nav className="flex-1 overflow-y-auto relative">
  <div
    key={
      activeLevel1Category?._id ||
      activeMainCategory?._id ||
      'main'
    }
    className="absolute inset-0 animate-slide-in"
  >
    {activeLevel1Category
      ? renderLevelTwo()
      : activeMainCategory
      ? renderLevelOne()
      : renderMain()}
  </div>
</nav>

      {/* Utility Links */}
      {utilityLinks.length > 0 && (
        <div className="border-t">
          {utilityLinks.map(link => (
            <Link
              key={link.name}
              href={link.href}
              onClick={onClose}
              className="flex items-center justify-between px-6 py-4 text-base text-gray-700 hover:bg-gray-100 transition"
            >
              {link.name}
              <ChevronRight className="w-5 h-5 text-gray-400" />
            </Link>
          ))}
        </div>
      )}

      {/* Delivery Info */}
      <div className="bg-gray-50 border-t flex items-center px-6 py-3 text-sm text-gray-600">
        <Truck className="w-5 h-5 mr-2" />
        Standard delivery starting at $25
      </div>
    </div>
  );
};

export default MobileMenu;

// Helper Header Component
const Header = ({ title, onBack }: { title: string; onBack: () => void }) => (
  <div className="flex items-center px-4 py-3 border-b bg-white sticky top-0 z-10">
    <button onClick={onBack} className="p-2 mr-2 rounded-full hover:bg-gray-100">
      <ChevronLeft className="w-5 h-5 text-gray-700" />
    </button>
    <h2 className="text-lg font-semibold text-gray-900">{title}</h2>
  </div>
);
