'use client'

import { useState, FormEvent, useEffect } from 'react'
import { useRouter, useSearchParams } from 'next/navigation'
import Link from 'next/link'
import { useAuthStore } from '@/stores/auth-store'
import { auth } from '@/lib/supabase'
import { Button } from '@/components/ui/Button'
import { Input } from '@/components/ui/Input'
import toast from 'react-hot-toast'

export const dynamic = 'force-dynamic'

export default function LoginPage() {
  const router = useRouter()
  const searchParams = useSearchParams()
  const { signIn, user } = useAuthStore()
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState('')

  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')

  // Show message from URL params (e.g., after email verification)
  useEffect(() => {
    const message = searchParams.get('message')
    if (message) {
      toast.success(message)
    }
    const urlError = searchParams.get('error')
    if (urlError) {
      toast.error(urlError)
    }
  }, [searchParams])

  // Redirect to dashboard when user is authenticated
  useEffect(() => {
    if (user && !isLoading) {
      const redirect = searchParams.get('redirect')
      router.push(redirect || '/dashboard')
    }
  }, [user, isLoading, router, searchParams])

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault()
    setError('')
    setIsLoading(true)

    try {
      await signIn(email, password)
      toast.success('Signed in successfully!')
      // The useEffect will handle the redirect when user state updates
    } catch (err) {
      const errorMsg = err instanceof Error ? err.message : 'Failed to sign in'
      setError(errorMsg)
      toast.error(errorMsg)
      setIsLoading(false)
    }
  }

  const handleGoogleSignIn = async () => {
    try {
      setIsLoading(true)
      await auth.signInWithGoogle()
    } catch (error) {
      toast.error(error instanceof Error ? error.message : 'Failed to sign in with Google')
    } finally {
      setIsLoading(false)
    }
  }

  const handleGitHubSignIn = async () => {
    try {
      setIsLoading(true)
      await auth.signInWithGitHub()
    } catch (error) {
      toast.error(error instanceof Error ? error.message : 'Failed to sign in with GitHub')
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-animated flex items-center justify-center px-4 relative overflow-hidden">
      {/* Background effects */}
      <div className="absolute inset-0 grid-pattern opacity-30" />
      <div className="aurora-glow w-96 h-96 bg-accent-primary top-0 left-0" />
      <div className="aurora-glow w-96 h-96 bg-accent-secondary bottom-0 right-0" />

      {/* Login card */}
      <div className="glass-card w-full max-w-md p-8 relative z-10 animate-scale-in">
        {/* Logo/Brand */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold gradient-text mb-2">Welcome Back</h1>
          <p className="text-gray-400">Sign in to continue to Mindmesh</p>
        </div>

        {/* Error message */}
        {error && (
          <div className="mb-6 p-4 rounded-lg bg-red-500/10 border border-red-500/20">
            <p className="text-red-400 text-sm text-center">{error}</p>
          </div>
        )}

        {/* Login form */}
        <form onSubmit={handleSubmit} className="space-y-5">
          <Input
            label="Email"
            type="email"
            placeholder="you@example.com"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
            autoComplete="email"
          />

          <Input
            label="Password"
            type="password"
            placeholder="••••••••"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
            autoComplete="current-password"
          />

          <div className="flex items-center justify-between text-sm">
            <label className="flex items-center text-gray-400">
              <input
                type="checkbox"
                className="w-4 h-4 rounded border-white/10 bg-white/5 text-accent-primary focus:ring-accent-primary/50 mr-2"
              />
              Remember me
            </label>
            <Link
              href="/auth/forgot-password"
              className="text-accent-primary hover:text-accent-secondary transition-colors"
            >
              Forgot password?
            </Link>
          </div>

          <Button
            type="submit"
            variant="primary"
            size="lg"
            className="w-full"
            disabled={isLoading}
          >
            {isLoading ? (
              <span className="flex items-center gap-2">
                <svg className="animate-spin h-5 w-5" viewBox="0 0 24 24">
                  <circle
                    className="opacity-25"
                    cx="12"
                    cy="12"
                    r="10"
                    stroke="currentColor"
                    strokeWidth="4"
                    fill="none"
                  />
                  <path
                    className="opacity-75"
                    fill="currentColor"
                    d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                  />
                </svg>
                Signing in...
              </span>
            ) : (
              'Sign In'
            )}
          </Button>
        </form>

        {/* Divider */}
        <div className="relative my-8">
          <div className="absolute inset-0 flex items-center">
            <div className="w-full border-t border-white/10" />
          </div>
          <div className="relative flex justify-center text-sm">
            <span className="px-4 bg-[#0a0a0b] text-gray-500">Or continue with</span>
          </div>
        </div>

        {/* Social login buttons */}
        <div className="grid grid-cols-2 gap-4">
          <Button
            type="button"
            variant="glass"
            size="md"
            className="w-full"
            onClick={handleGoogleSignIn}
            disabled={isLoading}
          >
            <svg className="w-5 h-5" viewBox="0 0 24 24">
              <path
                fill="currentColor"
                d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"
              />
              <path
                fill="currentColor"
                d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"
              />
              <path
                fill="currentColor"
                d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"
              />
              <path
                fill="currentColor"
                d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"
              />
            </svg>
            Google
          </Button>
          <Button
            type="button"
            variant="glass"
            size="md"
            className="w-full"
            onClick={handleGitHubSignIn}
            disabled={isLoading}
          >
            <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
              <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/>
            </svg>
            GitHub
          </Button>
        </div>

        {/* Sign up link */}
        <p className="mt-8 text-center text-gray-400 text-sm">
          Don&apos;t have an account?{' '}
          <Link
            href="/auth/signup"
            className="text-accent-primary hover:text-accent-secondary font-medium transition-colors"
          >
            Sign up
          </Link>
        </p>
      </div>
    </div>
  )
}
