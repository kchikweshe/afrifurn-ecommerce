// IconButtons.tsx
import { IconButton } from '@mui/material';

export const CustomIconButton = ({ icon, onClick, label }) => (
  <IconButton
    color="inherit"
    className="hidden md:flex"
    onClick={() => onClick}
  />
)


