'use client'
import { Color } from '@/types';
import { useState, useMemo } from 'react';
import Image from 'next/image';
import { PRODUCT_IMAGE_URLS } from '@/data/urls';
import { Material } from '@/types';

// Helper to get perceived brightness from hex color
function getBrightness(hex: string) {
  // Remove # if present
  hex = hex.replace('#', '');
  // Convert 3-digit hex to 6-digit
  if (hex.length === 3) {
    hex = hex.split('').map(x => x + x).join('');
  }
  const r = parseInt(hex.substring(0, 2), 16);
  const g = parseInt(hex.substring(2, 4), 16);
  const b = parseInt(hex.substring(4, 6), 16);
  // Perceived brightness formula
  return 0.299 * r + 0.587 * g + 0.114 * b;
}

const ColorFilter = ({ colors, onFilterChange }: { colors: Color[], onFilterChange: Function }) => {
  const [selectedColor, setSelectedColor] = useState<string | null>(null);

  // Sort colors from lightest to darkest and ensure uniqueness by color_code
  const sortedColors = useMemo(() => {
    const uniqueMap = new Map<string, Color>();
    colors.forEach(color => {
      if (!uniqueMap.has(color.color_code)) {
        uniqueMap.set(color.color_code, color);
      }
    });
    return Array.from(uniqueMap.values()).sort((a, b) => getBrightness(b.color_code) - getBrightness(a.color_code));
  }, [colors]);

  const handleChange = (newColor: string) => {
    setSelectedColor(newColor === selectedColor ? null : newColor);
    onFilterChange(newColor === selectedColor ? null : newColor);
  };

  return (
    <div className="p-2 sm:p-4">
      <h3 className="text-md font-medium mb-2">Colors</h3>
      <div className="grid grid-cols-3 gap-6">
        {sortedColors.map((color, index) => (
          <button
            key={index}
            className={`w-12 h-12 rounded-full border-2 relative overflow-hidden flex items-center justify-center ${selectedColor == color.color_code ? 'border-black' : 'border-blue-400'}`}
            style={{ backgroundColor: color.color_code }}
            onClick={() => handleChange(color.color_code)}
            aria-label={`Filter by ${color.name}`}
          >
            {color.image && (
              <Image
                src={color.image.startsWith('http') ? color.image : PRODUCT_IMAGE_URLS + color.image}
                alt={color.name}
                fill
                style={{ objectFit: 'cover', opacity: 0.7, borderRadius: '50%' }}
              />
            )}
          </button>
        ))}
      </div>
    </div>
  );
};

const MaterialFilter = ({
  materials,
  onFilterChange,
}: {
  materials: Material[];
  onFilterChange: (selected: string[]) => void;
}) => {
  const [selectedMaterial, setSelectedMaterial] = useState<string | null>(null);

  const handleSelect = (materialId: string) => {
    const newValue = materialId === selectedMaterial ? null : materialId;
    setSelectedMaterial(newValue);
    onFilterChange(newValue ? [newValue] : []);
  };

  return (
    <div className="p-2 sm:p-4 min-w-[220px]">
      <h3 className="text-md font-medium mb-2">Materials</h3>
      <div className="grid grid-cols-2 gap-3">
        {materials.map((material) => (
          <button
            key={material._id}
            className={`rounded-full px-4 py-2 border-2 font-semibold transition-colors duration-150
              ${selectedMaterial === material._id
                ? 'bg-blue-600 text-white border-blue-600 shadow'
                : 'bg-gray-100 text-gray-800 border-gray-300 hover:bg-blue-50 hover:border-blue-400'}
            `}
            onClick={() => handleSelect(material._id)}
            aria-label={`Filter by ${material.name}`}
            type="button"
          >
            {material.name}
          </button>
        ))}
      </div>
    </div>
  );
};

export default ColorFilter;