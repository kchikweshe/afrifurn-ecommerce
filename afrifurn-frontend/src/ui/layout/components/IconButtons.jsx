import { Favorite, Person, ShoppingCart } from "@mui/icons-material";
import { CustomIconButton } from "./IconButton";

// Usage in IconButtons.tsx
export const IconButtons = () => (
  <>
    <CustomIconButton icon={Person} onClick={() => setProfileOpen(!profileOpen)} label="Profile" />
    <CustomIconButton icon={Favorite} onClick={() => setWishlistOpen(!wishlistOpen)} label="Wishlist" />
    <CustomIconButton icon={ShoppingCart} onClick={() => setCartOpen(!cartOpen)} label="Cart" />
  </>
);