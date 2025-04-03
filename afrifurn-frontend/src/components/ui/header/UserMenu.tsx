'use client'

import { useRouter } from 'next/navigation'
import { LogOut, Settings, UserCircle, LogIn } from 'lucide-react'
import { Button } from "@/components/ui/button"
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import { auth } from '@/config/firebase/firebase'
import assert from 'assert'
import { useAuthContext } from '@/ui/auth-provider'
interface UserMenuProps {
  isAuthenticated?: boolean;
  userImage: string | undefined | null;
  userName: string | undefined | null;
}

const UserMenu = ({ userImage, userName }: UserMenuProps) => {
  const router = useRouter()
  const {user}=useAuthContext()

  const isAuthenticated =   user!== null
  const handleSignOut = () => {
    // Implement your sign out logic here
    console.log('Sign out clicked')
    auth.signOut()
    assert(auth.currentUser === null, 'User is not signed out')

  }

  if (!isAuthenticated) {
    return (
      <Button
        variant="ghost"
        size="icon"
        className="rounded-full w-10 h-10 hover:bg-gray-100"
        onClick={() => router.push('/login')}
      >
    <Button
          variant="ghost"
          size="icon"
          className="rounded-full w-10 h-10 hover:bg-gray-100"
        >
          <Avatar className="h-8 w-8">
            <AvatarImage src={userImage?.toString() || ""} alt={userName?.toString() || ""} />
            <AvatarFallback>
              {userName ? userName[0].toUpperCase() : <UserCircle className="h-6 w-6 text-gray-700" />}
            </AvatarFallback>
          </Avatar>
        </Button>      </Button>
    )
  }

  return (
    <DropdownMenu>
      <DropdownMenuTrigger asChild>
        <Button
          variant="ghost"
          size="icon"
          className="rounded-full w-10 h-10 hover:bg-gray-100"
        >
          <Avatar className="h-8 w-8">
            <AvatarImage src={userImage?.toString() || ""} alt={userName?.toString() || ""} />
            <AvatarFallback>
              {userName ? userName[0].toUpperCase() : <UserCircle className="h-6 w-6 text-gray-700" />}
            </AvatarFallback>
          </Avatar>
        </Button>
      </DropdownMenuTrigger>
      <DropdownMenuContent align="end" className="w-56">
        <DropdownMenuItem onClick={() => router.push('/profile')} className="cursor-pointer">
          <UserCircle className="mr-2 h-4 w-4" />
          <span>Profile</span>
        </DropdownMenuItem>
        <DropdownMenuItem onClick={() => router.push('/settings')} className="cursor-pointer">
          <Settings className="mr-2 h-4 w-4" />
          <span>Settings</span>
        </DropdownMenuItem>
        <DropdownMenuSeparator />
        <DropdownMenuItem onClick={handleSignOut} className="cursor-pointer text-red-600">
          <LogOut className="mr-2 h-4 w-4" />
          <span>Sign out</span>
        </DropdownMenuItem>
      </DropdownMenuContent>
    </DropdownMenu>
  )
}

export default UserMenu 