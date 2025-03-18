import { theme } from "./theme";

const config = {
    darkMode: ["class"],
    content: [
    "./src/app/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/**/*.{html,js,tsx}"
    
  ],
  
  theme:theme,
  plugins: [require("tailwindcss-animate")],
};
export default config;
