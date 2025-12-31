'use client'

import React, { createContext, useContext, useEffect, ReactNode } from 'react'
import { useAuthStore } from '@/stores/auth-store'
import { auth } from '@/lib/supabase'
import type { User, Session } from '@supabase/supabase-js'

interface AuthContextType {
  user: User | null
  session: Session | null
  isLoading: boolean
  error: string | null
  signIn: (email: string, password: string) => Promise<void>
  signUp: (email: string, password: string, metadata?: Record<string, unknown>) => Promise<void>
  signOut: () => Promise<void>
  clearError: () => void
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

interface AuthProviderProps {
  children: ReactNode
}

export function AuthProvider({ children }: AuthProviderProps) {
  const { user, session, isLoading, error, signIn, signUp, signOut, initializeAuth, clearError, setUser } =
    useAuthStore()

  // Initialize auth on mount
  useEffect(() => {
    initializeAuth()

    // Set up auth state listener
    const { data: authListener } = auth.onAuthStateChange(async (event, session) => {
      console.log('Auth event:', event)
      setUser(session?.user ?? null)
    })

    return () => {
      authListener.subscription.unsubscribe()
    }
  }, [])

  const value: AuthContextType = {
    user,
    session,
    isLoading,
    error,
    signIn,
    signUp,
    signOut,
    clearError,
  }

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

export function useAuth() {
  const context = useContext(AuthContext)
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider')
  }
  return context
}
