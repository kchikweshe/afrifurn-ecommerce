import { Product } from "../types";

interface AddToCartButtonProps {
  product: Product;
  handleAddToCartFn:VoidFunction
}

export default function AddToCartButton({ product ,handleAddToCartFn}: AddToCartButtonProps) {
  const handleAddToCart = () => {
    // Implement add to cart logic
    console.log(`Added ${product.name} to cart`);
   handleAddToCartFn()
    
  };

  return (
    <button 
      onClick={handleAddToCart}
      className="mt-6 w-full bg-blue-600 text-white py-3 px-6 rounded-full hover:bg-blue-700 transition duration-300"
    >
      Add to Cart
    </button>
  );
}