import { createClient } from '@supabase/supabase-js'
import type { AuthError, User, Session } from '@supabase/supabase-js'

const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL!
const supabaseAnonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!

export const supabase = createClient(supabaseUrl, supabaseAnonKey, {
  auth: {
    flowType: 'pkce',
    autoRefreshToken: true,
    persistSession: true,
    detectSessionInUrl: true,
    // Use cookies instead of localStorage so middleware can read the session
    storage: {
      getItem: (key) => {
        if (typeof window === 'undefined') return null
        const value = localStorage.getItem(key)
        return value
      },
      setItem: (key, value) => {
        if (typeof window === 'undefined') return
        localStorage.setItem(key, value)
      },
      removeItem: (key) => {
        if (typeof window === 'undefined') return
        localStorage.removeItem(key)
      },
    },
  },
})

// Types
export interface SignUpResult {
  user: User | null
  session: Session | null
  error: AuthError | null
}

export interface SignInResult {
  user: User | null
  session: Session | null
  error: AuthError | null
}

// Auth helper functions
export const auth = {
  /**
   * Get current user with session
   */
  async getCurrentUser() {
    const { data: { user }, error } = await supabase.auth.getUser()
    if (error) throw error
    return user
  },

  /**
   * Get current session
   */
  async getSession() {
    const { data: { session }, error } = await supabase.auth.getSession()
    if (error) throw error
    return session
  },

  /**
   * Refresh session
   */
  async refreshSession() {
    const { data: { session }, error } = await supabase.auth.refreshSession()
    if (error) throw error
    return session
  },

  /**
   * Sign in with email and password
   */
  async signIn(email: string, password: string): Promise<SignInResult> {
    const { data, error } = await supabase.auth.signInWithPassword({
      email,
      password,
    })
    return {
      user: data.user,
      session: data.session,
      error,
    }
  },

  /**
   * Sign up with email and password
   */
  async signUp(
    email: string,
    password: string,
    metadata?: Record<string, unknown>
  ): Promise<SignUpResult> {
    const { data, error } = await supabase.auth.signUp({
      email,
      password,
      options: {
        data: metadata,
        emailRedirectTo: `${window.location.origin}/auth/callback`,
      },
    })
    return {
      user: data.user,
      session: data.session,
      error,
    }
  },

  /**
   * Sign out
   */
  async signOut() {
    const { error } = await supabase.auth.signOut()
    if (error) throw error
  },

  /**
   * Send password reset email
   */
  async resetPassword(email: string) {
    const { error } = await supabase.auth.resetPasswordForEmail(email, {
      redirectTo: `${window.location.origin}/auth/reset-password`,
    })
    if (error) throw error
  },

  /**
   * Update user password
   */
  async updatePassword(newPassword: string) {
    const { error } = await supabase.auth.updateUser({
      password: newPassword,
    })
    if (error) throw error
  },

  /**
   * Update user metadata
   */
  async updateMetadata(metadata: Record<string, unknown>) {
    const { data, error } = await supabase.auth.updateUser({
      data: metadata,
    })
    if (error) throw error
    return data.user
  },

  /**
   * Send email verification
   */
  async sendVerificationEmail() {
    const { error } = await supabase.auth.resend({
      type: 'signup',
      email: (await supabase.auth.getUser()).data.user?.email,
    })
    if (error) throw error
  },

  /**
   * Sign in with OAuth (Google)
   */
  async signInWithGoogle() {
    const { data, error } = await supabase.auth.signInWithOAuth({
      provider: 'google',
      options: {
        redirectTo: `${window.location.origin}/auth/callback`,
      },
    })
    if (error) throw error
    return data
  },

  /**
   * Sign in with OAuth (GitHub)
   */
  async signInWithGitHub() {
    const { data, error } = await supabase.auth.signInWithOAuth({
      provider: 'github',
      options: {
        redirectTo: `${window.location.origin}/auth/callback`,
      },
    })
    if (error) throw error
    return data
  },

  /**
   * Listen to auth state changes
   */
  onAuthStateChange(
    callback: (event: string, session: Session | null) => void
  ) {
    return supabase.auth.onAuthStateChange(callback)
  },
}
