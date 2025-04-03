'use client'
import axios from 'axios';
import { GoogleAuthProvider, signInWithPopup } from 'firebase/auth';
import { createContext, useState, useCallback } from 'react';
import { auth } from '@/config/firebase/firebase';
interface AuthContextType {
  isLoading: boolean;
  isAuthenticated:boolean;
  signUp: (email: string, password: string) => void;
  signUpWithGoogle: () => void;
}

export const AuthContext = createContext<AuthContextType>({
  isLoading: false,
isAuthenticated:false,
  signUp: () => { },
  signUpWithGoogle: () => { },
});

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [isLoading, setIsLoading] = useState(false);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  // Define the base URL for your FastAPI backend
  const API_BASE_URL = 'http://localhost:8001/api/v1/auth'
  // Create an axios instance
  const api = axios.create({
    baseURL: API_BASE_URL,
    headers: {
      'Content-Type': 'application/json',
    },
  });
  const provider = new GoogleAuthProvider();

  const signUp = useCallback((email: string, password: string) => {
    setIsLoading(true);
    // Implement your signup logic here
    console.log('Signing up with:', email, password);
    setIsLoading(false);
  }, []);

  const signUpWithGoogle = useCallback(async () => {
    setIsLoading(true)

    // Implement your Google signup logic here

    console.log('Signing up with Google')

    try {
      const result = await signInWithPopup(auth, provider);

      // Get the user information
      const user = result.user;
      const { displayName, email, photoURL, uid, phoneNumber } = user;

      // Send user information to FastAPI backend
      const response = await api.post(`/register`, {
        firebase_uid: uid,
        email: email,
        name: displayName,
        phone_number: phoneNumber
      });
      if (response.status != 201) {
        console.log("Error: ", response.status)
      }
      setIsAuthenticated(true)
      return result;
    } catch (error) {
      console.error('Google Sign-In error:', error);
      throw error;

    }
    finally {
      setIsLoading(false)

    }

  }, [])

  return (
    <AuthContext.Provider value={{ isLoading,isAuthenticated, signUp, signUpWithGoogle }}>
      {children}
    </AuthContext.Provider>
  );
};