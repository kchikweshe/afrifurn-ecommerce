import { DataContext } from "@/data/data.context";
import { Product, ProductVariant } from "@/types";
import { useContext } from "react";
interface ProductDetailsProps {
  product: Product;
  selectedVariant: ProductVariant;
  setSelectedVariant: (variant: ProductVariant) => void;
}

export default function ProductDetails({ product, selectedVariant, setSelectedVariant }: ProductDetailsProps) {
    const state = useContext(DataContext);
    if (!state) return null;
  const getMaterialName = (material: string) => {
    return state.materials.find(m => m._id === material)?.name || material;
  };
 
  return (
    <div>
      <h1 className="text-3xl font-bold mb-4">{product.name}</h1>
      <p className="text-xl font-semibold mb-4">
        {product.currency}{product.price.toFixed(2)} {product.currency}
      </p>
      <p className="mb-4">{product.description}</p>
      <div className="mb-4">
        <h2 className="text-xl font-semibold mb-2">Color</h2>
        <div className="flex gap-2">
          {product.product_variants.map((variant: ProductVariant) => (
            <button
              key={variant._id}
              onClick={() => setSelectedVariant(variant)}
              className={`w-8 h-8 rounded-full ${selectedVariant._id === variant._id ? 'ring-2 ring-offset-2 ring-blue-500' : ''}`}
              style={{ backgroundColor: variant.color_id }}
              title={variant.color_id}
            />
          ))}
        </div>
      </div>
      <div className="mb-4">
        <h2 className="text-xl font-semibold mb-2">Specifications</h2>
        <dl className="grid grid-cols-2 gap-2">
          <div>
            <dt className="font-semibold">Dimensions</dt>
            <dd>{`${product.dimensions.width}x${product.dimensions.height}x${product.dimensions.length} cm`}</dd>
          </div>
          {product.dimensions.weight && (
            <div>
              <dt className="font-semibold">Weight</dt>
              <dd>{`${product.dimensions.weight} kg`}</dd>
            </div>
          )}
          {product.material && (
            <div>
              <dt className="font-semibold">Material</dt>
              <dd>{getMaterialName(product.material) }</dd>
            </div>
          )}
        </dl>
      </div>
    </div>
  );
}