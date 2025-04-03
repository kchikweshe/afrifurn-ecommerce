
// useCategoryFilter.ts

import { Level2Category } from "@/types";

export const useCategoryFilter = (categories: Level2Category[]) => {
  const filteredCategories = (parentId: string) => categories.filter(category => category.level_one_category._id === parentId);
  return filteredCategories;
};
