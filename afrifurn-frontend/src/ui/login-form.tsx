'use client'
import React, { useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { signInWithEmailAndPassword } from 'firebase/auth';
import { auth } from '@/config/firebase/firebase';
import SocialAuth from './social-auth';


const LoginForm = () => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const router = useRouter();


    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setError(''); // Clear any previous errors
        try {
            await signInWithEmailAndPassword(auth, email, password);
            router.push('/');
        } catch (error: any) {
            // More specific error messages based on Firebase error codes
            const errorMessage = (() => {
                switch (error.code) {
                    case 'auth/invalid-email':
                        return 'Invalid email address format.';
                    case 'auth/user-disabled':
                        return 'This account has been disabled.';
                    case 'auth/user-not-found':
                    case 'auth/wrong-password':
                        return 'Invalid email or password.';
                    case 'auth/too-many-requests':
                        return 'Too many failed login attempts. Please try again later.';
                    default:
                        return 'An error occurred during login. Please try again.';
                }
            })();
            setError(errorMessage);
            console.error('Login error:', error);
        }
    };

    return (
        <RegisterForm />



    );

    function RegisterForm() {
        return <div className="max-w-md mx-auto">
            <form onSubmit={handleSubmit} className="mb-4">
                {error && <p className="text-red-500 mb-4">{error}</p>}
                <div className="mb-4">
                    <label htmlFor="email" className="block mb-2">Email</label>
                    <input
                        type="email"
                        id="email"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        required
                        className="w-full px-3 py-2 border rounded" />
                </div>
                <div className="mb-4">
                    <label htmlFor="password" className="block mb-2">Password</label>
                    <input
                        type="password"
                        id="password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        required
                        className="w-full px-3 py-2 border rounded" />
                </div>
                <button type="submit" className="w-full bg-blue-500 text-white py-2 rounded hover:bg-blue-600">
                    Login
                </button>
            </form>
            <div className="text-center mb-4">
                <Link href="/reset-password" className="text-blue-500 hover:underline">
                    Forgot Password?
                </Link>
            </div>
            <div className="mb-4">
                <p className="text-center mb-2">Or sign in with:</p>
                <SocialAuth />
            </div>
        </div>;
    }
};

export default LoginForm;