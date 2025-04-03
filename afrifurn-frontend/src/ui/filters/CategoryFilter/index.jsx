'use client'
import React from 'react';
import { Checkbox } from "@material-tailwind/react";



const CategoryFilter = ({onFilterChange}) => {
    const [selectedCategories, setSelectedCategories] = React.useState([]);

    const {categories}=state
    const handleCategoryChange = (categoryId) => {
        setSelectedCategories(prev =>
            prev.includes(categoryId)
                ? prev.filter(id => id !== categoryId)
                : [...prev, categoryId]
        );
    };

    return (
        <div className="p-4">
            <h2 className="text-xl font-semibold mb-4">Product Categories</h2>
            <div className="flex flex-col gap-2">
                {categories.map(category => (
                    <label key={category.id} className="flex items-center gap-2">
                        <Checkbox
                            color="blue"
                            id={`category-${category.id}`}
                            checked={selectedCategories.includes(category.id)}
                            onChange={() => handleCategoryChange(category.id)}
                        />
                        <span>{`${category.name} (${category.count})`}</span>
                    </label>
                ))}
            </div>
        </div>
    );
};

export default CategoryFilter;
