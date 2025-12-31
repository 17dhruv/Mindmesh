import { create } from 'zustand'
import { persist } from 'zustand/middleware'
import { supabase } from '@/lib/supabase'
import type { User as SupabaseUser, Session } from '@supabase/supabase-js'

interface AuthState {
  user: SupabaseUser | null
  session: Session | null
  isLoading: boolean
  error: string | null
  signIn: (email: string, password: string) => Promise<void>
  signUp: (email: string, password: string, metadata?: Record<string, unknown>) => Promise<void>
  signOut: () => Promise<void>
  initializeAuth: () => Promise<void>
  clearError: () => void
  setUser: (user: SupabaseUser | null) => void
  setSession: (session: Session | null) => void
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      user: null,
      session: null,
      isLoading: false, // Start with false - only load when actually checking
      error: null,

      signIn: async (email: string, password: string) => {
        set({ isLoading: true, error: null })
        try {
          const { data, error } = await supabase.auth.signInWithPassword({
            email,
            password,
          })
          if (error) throw error
          set({ user: data.user, session: data.session, isLoading: false })
        } catch (error) {
          set({
            error: error instanceof Error ? error.message : 'Failed to sign in',
            isLoading: false,
          })
          throw error
        }
      },

      signUp: async (email: string, password: string, metadata?: Record<string, unknown>) => {
        set({ isLoading: true, error: null })
        try {
          const { data, error } = await supabase.auth.signUp({
            email,
            password,
            options: {
              data: metadata,
            },
          })
          if (error) throw error
          set({ user: data.user, session: data.session, isLoading: false })
        } catch (error) {
          set({
            error: error instanceof Error ? error.message : 'Failed to sign up',
            isLoading: false,
          })
          throw error
        }
      },

      signOut: async () => {
        set({ isLoading: true, error: null })
        try {
          await supabase.auth.signOut()
          set({ user: null, session: null, isLoading: false })
        } catch (error) {
          set({
            error: error instanceof Error ? error.message : 'Failed to sign out',
            isLoading: false,
          })
          throw error
        }
      },

      initializeAuth: async () => {
        set({ isLoading: true, error: null })
        try {
          const { data: { session } } = await supabase.auth.getSession()
          set({ user: session?.user ?? null, session, isLoading: false })
        } catch (error) {
          // If no user is logged in, that's fine
          set({ user: null, session: null, isLoading: false })
        }
      },

      clearError: () => set({ error: null }),

      setUser: (user: SupabaseUser | null) => set({ user }),

      setSession: (session: Session | null) => set({ session }),
    }),
    {
      name: 'auth-storage',
      partialize: (state) => ({ user: state.user }),
    }
  )
)