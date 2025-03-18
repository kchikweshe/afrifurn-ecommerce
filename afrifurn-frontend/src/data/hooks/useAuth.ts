// // hooks/useAuth.ts

// 'use client'

// import axios from 'axios';
// import { useState, useCallback } from 'react';
// import { signInWithPopup, GoogleAuthProvider } from 'firebase/auth';
// import { auth } from '@/firebase/firebase';

// // Define the base URL for your FastAPI backend
// const API_BASE_URL = 'http://localhost:8001/api/v1/auth'
// // Create an axios instance
// const api = axios.create({
//   baseURL: API_BASE_URL,
//   headers: {
//     'Content-Type': 'application/json',
//   },
// });
// const provider = new GoogleAuthProvider();

// export function useAuth() {
//   const [isLoading, setIsLoading] = useState(false)

//   const signUp = useCallback(async (email: string, password: string) => {
//     setIsLoading(true)
//     // Implement your signup logic here
//     console.log('Signing up with:', email, password)
//     await new Promise(resolve => setTimeout(resolve, 2000)) // Simulating API call
//     setIsLoading(false)
//   }, [])

//   const signUpWithGoogle = useCallback(async () => {
//     setIsLoading(true)

//     // Implement your Google signup logic here

//     console.log('Signing up with Google')

//     try {
//       const result = await signInWithPopup(auth, provider);

//       // Get the user information
//       const user = result.user;
//       const { displayName, email, uid ,phoneNumber} = user;

//       // Send user information to FastAPI backend
//       const response =await api.post(`/register`, {
//         firebase_uid: uid,
//         email: email,
//         name: displayName,
//         phone_number:phoneNumber
//       });
//       if(response.status!=201){
//         console.log("Error: ",response.status)
//       }
//       return result;
//     } catch (error) {
//       console.error('Google Sign-In error:', error);
//       throw error;

//     }
//     finally{
//       setIsLoading(false)

//     }

//   }, [])

//   return { isLoading, signUp, signUpWithGoogle }
// }
// File: hooks/useAuth.ts
import { useState, useEffect } from 'react';
import { User, onAuthStateChanged } from 'firebase/auth';
import { auth } from '@/config/firebase/firebase';

export function useAuth() {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const unsubscribe = onAuthStateChanged(auth, (user) => {
      setUser(user);
      setLoading(false);
    });

    return () => unsubscribe();
  }, []);

  return { user, loading };
}