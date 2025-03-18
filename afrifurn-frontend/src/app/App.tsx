import React from "react";
import Home from "./(home)/page";
import { AuthProvider } from "@/ui/auth-provider";
import { DataProvider } from "@/data/data.provider";

function App() {
  return (
    <AuthProvider>
        <DataProvider>
        <Home />

        </DataProvider>
    </AuthProvider>
  );
}

export default App;
