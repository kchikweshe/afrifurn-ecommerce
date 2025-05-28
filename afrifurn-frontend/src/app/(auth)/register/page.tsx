'use client'
import React, { useState, useTransition } from 'react';
import { useRouter } from 'next/navigation';
import Image from 'next/image';
import Link from 'next/link';
import { createUserWithEmailAndPassword, sendEmailVerification, updateProfile } from 'firebase/auth';
import { auth } from '@/config/firebase/firebase';
import { EyeOff, Eye } from 'lucide-react';
import SocialAuth from '@/ui/social-auth';

const RegisterPage: React.FC = () => {
  const router = useRouter();
  const [isPending, startTransition] = useTransition();
  const [isEmailRegister, setIsEmailRegister] = useState(true);
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [showPassword, setShowPassword] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setSuccess('');
    setIsLoading(true);

    if (password !== confirmPassword) {
      setError("Passwords don't match");
      setIsLoading(false);
      return;
    }

    try {
      const userCredential = await createUserWithEmailAndPassword(auth, email, password);
      // await updateProfile(userCredential.user, { displayName: name });
      let user=userCredential.user

      if (userCredential)
        setSuccess("Account created successfuly for " + user.displayName + ". Redirecting you to the homepage........");
        // Set a flag for the toast
      localStorage.setItem('showRegisterSuccess', 'true');
      localStorage.setItem('showRegisterSuccessMessage', success);
      await sendEmailVerification(user);

        startTransition(() => {
          router.push('/');
        });
    } catch (error: any) {
      const errorMessage = error.code ? getFirebaseErrorMessage(error.code) : 'Failed to register. Please try again.';
      setError(errorMessage);
      console.error('Registration error:', error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex ">


      {/* Right side - Form */}
      <div className="w-full flex items-center justify-center p-8 sm:p-12 bg-white">
        <div className="w-full max-w-md space-y-8">
          <div className=' flex justify-center'>
            <Image src="/logo.svg" alt="Afri Furn Logo" width={150} height={150} />
          </div>

          <div className="text-center">
            <h2 className="mt-6 text-3xl font-bold text-gray-900">
              Create your account
            </h2>
            <p className="mt-2 text-sm text-gray-600">
              Already have an account?{' '}
              <Link href="/login" className="font-medium text-blue-600 hover:text-blue-500 transition-colors">
                Log in
              </Link>
            </p>
          </div>

          {/* Auth Method Tabs */}
          <div className="flex justify-center mb-8 p-1 bg-gray-100 rounded-xl">
            <button
              onClick={() => setIsEmailRegister(true)}
              className={`py-2.5 px-5 rounded-lg transition-all duration-200 text-sm font-medium w-1/2 ${isEmailRegister ? 'bg-white text-blue-600 shadow-sm' : 'text-gray-600 hover:text-gray-800'
                }`}
            >
              Email
            </button>
            <button
              onClick={() => setIsEmailRegister(false)}
              className={`py-2.5 px-5 rounded-lg transition-all duration-200 text-sm font-medium w-1/2 ${!isEmailRegister ? 'bg-white text-blue-600 shadow-sm' : 'text-gray-600 hover:text-gray-800'
                }`}
            >
              Social
            </button>
          </div>

          {error && (
            <div className="bg-red-50 border-l-4 border-red-500 text-red-700 p-4 rounded-md shadow-sm" role="alert">
              <div className="flex">
                <div className="py-1">
                  <svg className="h-6 w-6 text-red-500 mr-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                </div>
                <span className="block sm:inline">{error}</span>
              </div>
            </div>
          )}

          {success && (
            <div className="bg-green-50 border-l-4 border-green-500 text-green-700 p-4 rounded-md shadow-sm" role="alert">
              <div className="flex">
                <div className="py-1">
                  <svg className="h-6 w-6 text-green-500 mr-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7" />
                  </svg>
                </div>
                <span className="block sm:inline">{success}</span>
              </div>
            </div>
          )}

          {isEmailRegister ? (
            <form className="mt-8 space-y-6" onSubmit={handleSubmit}>
              <div className="space-y-4">

                <div>
                  <label htmlFor="email-address" className="block text-sm font-medium text-gray-700 mb-1">Email address</label>
                  <input
                    id="email-address"
                    name="email"
                    type="email"
                    autoComplete="email"
                    required
                    className="appearance-none relative block w-full px-4 py-3 border border-gray-300 placeholder-gray-400 text-gray-900 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 focus:z-10 sm:text-sm"
                    placeholder="example@domain.com"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                  />
                </div>
                <div className="relative">
                  <label htmlFor="password" className="block text-sm font-medium text-gray-700 mb-1">Password</label>
                  <div className="relative">
                    <input
                      id="password"
                      name="password"
                      type={showPassword ? "text" : "password"}
                      autoComplete="new-password"
                      required
                      className="appearance-none relative block w-full px-4 py-3 border border-gray-300 placeholder-gray-400 text-gray-900 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 focus:z-10 sm:text-sm pr-12"
                      placeholder="••••••••"
                      value={password}
                      onChange={(e) => setPassword(e.target.value)}
                    />
                    <button
                      type="button"
                      className="absolute inset-y-0 right-0 pr-3 flex items-center"
                      onClick={() => setShowPassword(!showPassword)}
                    >
                      {showPassword ? (
                        <EyeOff className="h-5 w-5 text-gray-500" />
                      ) : (
                        <Eye className="h-5 w-5 text-gray-500" />
                      )}
                    </button>
                  </div>
                </div>
                <div>
                  <label htmlFor="confirm-password" className="block text-sm font-medium text-gray-700 mb-1">Confirm password</label>
                  <input
                    id="confirm-password"
                    name="confirm-password"
                    type="password"
                    autoComplete="new-password"
                    required
                    className="appearance-none relative block w-full px-4 py-3 border border-gray-300 placeholder-gray-400 text-gray-900 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 focus:z-10 sm:text-sm"
                    placeholder="••••••••"
                    value={confirmPassword}
                    onChange={(e) => setConfirmPassword(e.target.value)}
                  />
                </div>
              </div>

              <div>
                <button
                  type="submit"
                  disabled={isLoading || isPending}
                  className="group relative w-full flex justify-center py-3 px-4 border border-transparent text-sm font-medium rounded-lg text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-colors shadow-md"
                >
                  {(isLoading || isPending) ? (
                    <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                      <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                  ) : 'Create Account'}
                </button>
              </div>
            </form>
          ) : (
            <div className="mt-6">
              <SocialAuth />
            </div>
          )}

          <div className="text-center mt-6">
            <p className="text-xs text-gray-600">
              By registering, you agree to our{' '}
              <Link href="/terms" className="font-medium text-blue-600 hover:text-blue-500 transition-colors">
                Terms of Service
              </Link>{' '}
              and{' '}
              <Link href="/privacy" className="font-medium text-blue-600 hover:text-blue-500 transition-colors">
                Privacy Policy
              </Link>
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};
// Helper function for Firebase error messages
const getFirebaseErrorMessage = (errorCode: string): string => {
  switch (errorCode) {
    case 'auth/email-already-in-use':
      return 'This email is already registered. Please try logging in instead.';
    case 'auth/weak-password':
      return 'Password should be at least 6 characters long.';
    case 'auth/invalid-email':
      return 'Please enter a valid email address.';
    case 'auth/operation-not-allowed':
      return 'This authentication method is not enabled. Please contact support.';
    case 'auth/network-request-failed':
      return 'Network error. Please check your internet connection.';
    default:
      return 'Failed to register. Please try again.';
  }
};

export default RegisterPage;