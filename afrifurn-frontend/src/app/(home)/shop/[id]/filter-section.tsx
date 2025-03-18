import { Slider } from "@/components/ui/slider"

interface FilterSectionProps {
    priceRange: number[]
    setPriceRange: (value: number[]) => void
    selectedColors: string[]
    colorOptions: string[]
    handleColorToggle: (color: string) => void
}

export default function FilterSection({
    priceRange,
    setPriceRange,
    selectedColors,
    colorOptions,
    handleColorToggle
}: FilterSectionProps) {
    return (
        <aside className="w-full md:w-64 space-y-6">
            <div>
                <h2 className="text-lg font-semibold mb-4">Filters</h2>
                <div className="space-y-4">
                    <div>
                        <h3 className="text-md font-medium mb-2">Price Range</h3>
                        <Slider
                            min={0}
                            max={200}
                            step={10}
                            value={priceRange}
                            onValueChange={setPriceRange}
                            className="mb-2"
                        />
                        <div className="flex justify-between text-sm text-gray-600">
                            <span>${priceRange[0]}</span>
                            <span>${priceRange[1]}</span>
                        </div>
                    </div>
                    <div>
                        <h3 className="text-md font-medium mb-2">Colors</h3>
                        <div className="flex flex-wrap gap-2">
                            {colorOptions.map(color => (
                                <button
                                    key={color}
                                    className={`w-8 h-8 rounded-full border-2 ${selectedColors.includes(color) ? 'border-black' : 'border-transparent'
                                        }`}
                                    style={{ backgroundColor: color }}
                                    onClick={() => handleColorToggle(color)}
                                    aria-label={`Filter by ${color}`}
                                />
                            ))}
                        </div>
                    </div>
                </div>
            </div>
        </aside>
    )
}