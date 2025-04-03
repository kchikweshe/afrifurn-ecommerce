// File: components/SignOutButton.tsx
import React from 'react';
import { useRouter } from 'next/router';
import { signOut } from 'firebase/auth';
import { auth } from '@/config/firebase/firebase';

const SignOutButton: React.FC = () => {
  const router = useRouter();

  const handleSignOut = async () => {
    try {
      await signOut(auth);
      router.push('/login'); // Redirect to login page after sign out
    } catch (error) {
      console.error('Error signing out:', error);
    }
  };

  return (
    <button
      onClick={handleSignOut}
      className="bg-red-500 text-white py-2 px-4 rounded hover:bg-red-600"
    >
      Sign Out
    </button>
  );
};

export default SignOutButton;