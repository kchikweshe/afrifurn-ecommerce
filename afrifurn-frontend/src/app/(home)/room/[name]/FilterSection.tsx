import React from 'react'
import { ChevronDown, X } from 'lucide-react'
import { Button } from "@/components/ui/button"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Slider } from "@/components/ui/slider"
import { Checkbox } from "@/components/ui/checkbox"
import { ScrollArea } from "@/components/ui/scroll-area"
import { Popover, PopoverContent, PopoverTrigger } from "@/components/ui/popover"
import { FilterParams, Level2Category } from '@/types'
import { Material } from '@/types'

interface FilterSectionProps {
    isVisible: boolean
    isSticky: boolean
    filters: FilterParams
    colors: any[]
    materials: any[],
    categories:Level2Category[],

    onFilterChange: (newFilters: Partial<FilterParams>) => void
    onClearFilters: () => void
}

// eslint-disable-next-line react/display-name
export const FilterSection = React.forwardRef<HTMLDivElement, FilterSectionProps>(
    ({ isVisible, isSticky, filters, colors, materials, categories,onFilterChange, onClearFilters }, ref) => (
        <div
            ref={ref}
            className={`transition-all duration-300 ease-in-out ${
                isVisible ? 'opacity-100 max-h-[1000px]' : 'opacity-0 max-h-0 overflow-hidden'
            } ${isSticky ? 'sticky top-0 bg-white z-20 py-4 shadow-md' : ''}`}
        >
            <div className="flex flex-wrap gap-4 items-center justify-between">
                
                <div className="flex flex-wrap gap-4 items-center">
                <Level2CategoriesFilter onFilterChange={onFilterChange} arr={categories}/>

                    <Select onValueChange={(value) => onFilterChange({ sort_order: Number(value) })}>
                        <SelectTrigger className="w-[180px]">
                            <SelectValue placeholder="Sort by" />
                        </SelectTrigger>
                        <SelectContent>
                            <SelectItem value="name">Name</SelectItem>
                            <SelectItem value="1">Price: Low to High</SelectItem>
                            <SelectItem value="-1">Price: High to Low</SelectItem>
                        </SelectContent>
                    </Select>

                    <ColorFilter colors={colors} selectedColors={filters.colors || []} onColorToggle={(color: string) => {
                        const newColors = filters.colors?.includes(color)
                            ? filters.colors?.filter(c => c !== color)
                            : [...(filters.colors || []), color]
                        onFilterChange({ colors: newColors })
                    }} />

                    <MaterialFilter materials={materials} selectedMaterials={filters.materials || []    } onMaterialToggle={(material: string) => {
                            const newMaterials = filters.materials?.includes(material)
                            ? filters.materials?.filter(m => m !== material)
                            : [...(filters.materials || []), material]
                        onFilterChange({ materials: newMaterials })
                    }} />

                    <PriceFilter
                        startPrice={filters.start_price || 0}
                        endPrice={filters.end_price || 1000}
                        onPriceChange={(start: any, end: any) => onFilterChange({ start_price: start, end_price: end })}
                    />
                </div>

                <Button variant="outline" onClick={onClearFilters} className="bg-red-600 whitespace-nowrap text-base font-semibold text-white">
                    Clear Filters
                    <X className="ml-2 h-4 w-4" />
                </Button>
            </div>
        </div>
    )
)

const ColorFilter = ({ colors, selectedColors, onColorToggle }: { colors: any[], selectedColors: string[], onColorToggle: (color: string) => void }) => (
    <Popover>
        <PopoverTrigger asChild>
            <Button variant="outline" className="w-[180px] justify-start">
                {selectedColors.length > 0 ? `${selectedColors.length} colors` : "Select colors"}
                <ChevronDown className="ml-2 h-4 w-4 shrink-0 opacity-50" />
            </Button>
            </PopoverTrigger>
            <PopoverContent className="w-[200px] p-0">
            <ScrollArea className="h-[300px] p-4">
                {colors.map((color) => (
                    <div key={color.color_code} className="flex items-center space-x-2 mb-2">
                        <Checkbox
                            id={`color-${color.color_code}`}
                            checked={selectedColors.includes(color.color_code as string)}
                            onCheckedChange={() => onColorToggle(color.color_code as string)}
                        />
                        <label
                            htmlFor={`color-${color.color_code}`}
                            className="text-base font-semibold flex items-center cursor-pointer"
                        >
                            <div
                                className="w-4 h-4 rounded-full mr-2"
                                style={{ backgroundColor: color.color_code as string }}
                            />
                            <span>{color.name}</span>
                        </label>
                    </div>
                ))}
            </ScrollArea>
        </PopoverContent>
    </Popover>
)

const MaterialFilter = ({ materials, selectedMaterials, onMaterialToggle }: { materials: Material[], selectedMaterials: string[], onMaterialToggle: (material: string) => void }) => (
    <Popover>
        <PopoverTrigger asChild>
            <Button variant="outline" className="w-[180px] justify-start">
                {selectedMaterials.length > 0 ? `${selectedMaterials.length} materials` : "Select materials"}
                <ChevronDown className="ml-2 h-4 w-4 shrink-0 opacity-50" />
            </Button>
        </PopoverTrigger>
        <PopoverContent className="w-[200px] p-0">
            <ScrollArea className="h-[300px] p-4">
                {materials.map((material: Material) => (
                    <div key={material._id} className="flex items-center space-x-2 mb-2">
                        <Checkbox
                            id={`material-${material._id}`}
                            className='text-base font-semibold'
                            checked={selectedMaterials.includes(material._id)}
                            onCheckedChange={() => onMaterialToggle(material._id)}
                        />
                        <label
                            htmlFor={`material-${material.name}`}
                            className="cursor-pointer"
                        >
                            {material.name}
                        </label>
                    </div>
                ))}
            </ScrollArea>
        </PopoverContent>
    </Popover>
)

const Level2CategoriesFilter = ({
  arr,
  onFilterChange,
}: {
  arr: Level2Category[];
  onFilterChange: (filters: Partial<FilterParams>) => void;
}) => (
  <Select
    onValueChange={(value) =>
      onFilterChange({
        category_short_name: value === "" ? undefined : value,
      })
    }
  >
   
    <SelectContent>
      {arr.map((cat) => (
        <SelectItem key={cat.short_name} value={cat.short_name}>
          <span className='text-base font-semibold'>
          {cat.name}
          </span>
        </SelectItem>
      ))}
    </SelectContent>
  </Select>
);

const PriceFilter = ({ startPrice, endPrice, onPriceChange }: { startPrice: number, endPrice: number, onPriceChange: (start: number, end: number) => void }) => (
    <div className="flex items-center  space-x-2">
        <span className="text-base font-semibold">Price:</span>
        <Slider
            min={0}
            max={1000}
            step={50}
            value={[startPrice, endPrice]}
            onValueChange={(value) => onPriceChange(value[0], value[1])}
            className="w-[200px]"
        />
        <span className="text-base font-semibold">${startPrice} - ${endPrice}</span>
    </div>
)