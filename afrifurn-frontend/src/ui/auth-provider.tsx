
import React, { createContext, useContext, useEffect, useState } from 'react';
import { useAuth } from '../data/hooks/useAuth';
import { onAuthStateChanged, User } from 'firebase/auth';
import { auth } from '@/config/firebase/firebase';

interface AuthContextType {
    user: User | null|undefined;
    loading: boolean;
  }
  
  const AuthContext = createContext<AuthContextType>({ user: null, loading: true });
  
  export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
    const [user, setUser] = useState<User|null>();
    const [loading, setLoading] = useState(true);
   console.log("User State: ", user)
    useEffect(() => {
      const unsubscribe = onAuthStateChanged(auth, (user) => {
        
        setUser(user);
        setLoading(false);
      });
  
      return () => unsubscribe();
    }, [user]);
  
    return (
      <AuthContext.Provider value={{ user, loading }}>
        {children}
      </AuthContext.Provider>
    );
  };
  
  export const useAuthContext = () => {
    const context = useContext(AuthContext);

    return context;
  };