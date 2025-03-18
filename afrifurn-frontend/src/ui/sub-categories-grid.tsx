// components/SubCategoriesGrid.jsx
'use client'
import React, { useEffect, useState } from 'react';
import Image from 'next/image';
import { PUBLIC_URL } from '../data/urls';
import { Level2Category } from '../types';
import { categoryService } from '@/services/category.service';


  const SubCategoriesGrid = ({ category }: { category: string }) => {
  const [data, setData] = useState<Array<Level2Category>>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<any>(null);
  useEffect(() => {
    // Function to fetch data
    const fetchData = async () => {
      try {
        const data = await categoryService.getLevel2CategoriesByLevel1(category);
        setData(data);
        setLoading(false);
      } catch (error:any) {
        setError(error);
        setLoading(false);
      }
    };

    // Call the fetch function
    fetchData();
  }, [category]);
  return (
    <div className="w-full p-4 grid grid-cols-2 gap-4">
      {data.map((subCat, index) => (
        <div
          key={index}
          className="relative cursor-pointer aspect-video"
        >
          <Image
            src={`${PUBLIC_URL}images/img_bedside.svg`}
            alt={subCat.name}
            layout="fill"
            objectFit="cover"
          />
          <div className="absolute inset-0 bg-black bg-opacity-40 hover:bg-opacity-60 transition-opacity flex items-center justify-center">
            <span className="text-white text-xl font-medium">{subCat.name}</span>
          </div>
        </div>
      ))}
    </div>
  );
};

export default SubCategoriesGrid;