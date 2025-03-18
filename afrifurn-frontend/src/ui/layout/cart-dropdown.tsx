import { Close } from "@radix-ui/react-toast";

export const CartDropdown: React.FC = () => {
    const cartItems = [
      { id: 1, name: 'Product 1', price: 19.99, quantity: 2 },
      { id: 2, name: 'Product 2', price: 29.99, quantity: 1 },
    ];
  
    return (
      <div className="absolute right-0 mt-2 w-80 bg-white rounded-lg shadow-xl overflow-hidden transition-all duration-300 ease-in-out transform origin-top-right">
        <div className="p-4">
          <h3 className="text-lg font-semibold mb-2">Your Cart</h3>
          {cartItems.map((item) => (
            <div key={item.id} className="flex items-center justify-between py-2 border-b">
              <div>
                <p className="font-medium">{item.name}</p>
                <p className="text-sm text-gray-500">${item.price} x {item.quantity}</p>
              </div>
              <button className="text-red-500 hover:text-red-700 transition-colors duration-200">
                <Close  />
              </button>
            </div>
          ))}
          <div className="mt-4 flex justify-between items-center">
            <p className="font-semibold">Total: $69.97</p>
            <button className="bg-blue-500 text-white px-4 py-2 rounded-full hover:bg-blue-600 transition-colors duration-200">
              Checkout
            </button>
          </div>
        </div>
      </div>
    );
  };