// 'use client';

// import React from 'react';
// import { Box, Typography, Button, List, ListItem, ListItemText, ListItemSecondaryAction, IconButton } from '@mui/material';
// import { Plus, Minus, Trash2 } from 'lucide-react';
// import { Cart, CartItem } from '@/types';
// import useCart from '@/context/cart/hook';
// const CartDropdown = ({cart}:{cart:Cart}) => {
//   const {updateQuantity} = useCart();

//   const totalPrice = cart.items.reduce((  total:number, item:CartItem) => total + item.product.price * item.quantity, 0);
//   return (
//     <Box sx={{ width: 300, maxHeight: 400, overflow: 'auto' }}>
//       <Typography variant="h6" sx={{ p: 2, borderBottom: 1, borderColor: 'divider' }}>
//         Your Cart
//       </Typography>
//       {cart.items.length === 0 ? (
//         <Typography sx={{ p: 2 }}>Your cart is empty.</Typography>
//       ) : (
//         <>
//           <List>
//             {cart.items.map((item) => (
//               <ListItem key={item.product._id} divider>
//                 <ListItemText
//                   primary={item.product.name}
//                   secondary={`$${item.product.price.toFixed(2)}`}
//                 />
//                 <ListItemSecondaryAction>
//                   <IconButton size="small" onClick={() => updateQuantity(item.product._id, item.quantity - 1)}>
//                     <Minus size={16} />
//                   </IconButton>
//                   <Typography component="span" sx={{ mx: 1 }}>
//                     {item.quantity}
//                   </Typography>
//                   <IconButton size="small" onClick={() => updateQuantity(item.product._id, item.quantity + 1)}>
//                     <Plus size={16} />
//                   </IconButton>
//                   <IconButton edge="end" onClick={() =>{}}>
//                     <Trash2 size={16} />
//                   </IconButton>
//                 </ListItemSecondaryAction>
//               </ListItem>
//             ))}
//           </List>
//           <Box sx={{ p: 2, borderTop: 1, borderColor: 'divider' }}>
//             <Typography variant="subtitle1" sx={{ fontWeight: 'bold', mb: 1 }}>
//               Total: ${totalPrice.toFixed(2)}
//             </Typography>
//             <Button variant="contained" fullWidth>
//               Proceed to Checkout
//             </Button>
//           </Box>
//         </>
//       )}
//     </Box>
//   );
// };

// export default CartDropdown;