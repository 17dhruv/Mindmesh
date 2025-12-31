'use client'

import { useState, FormEvent } from 'react'
import Link from 'next/link'
import { useRouter } from 'next/navigation'
import { auth } from '@/lib/supabase'
import { Button } from '@/components/ui/Button'
import { Input } from '@/components/ui/Input'
import toast from 'react-hot-toast'

export const dynamic = 'force-dynamic'

export default function ForgotPasswordPage() {
  const router = useRouter()
  const [email, setEmail] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [isSuccess, setIsSuccess] = useState(false)

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault()
    setIsLoading(true)

    try {
      await auth.resetPassword(email)
      setIsSuccess(true)
      toast.success('Password reset email sent!')
    } catch (error) {
      toast.error(
        error instanceof Error ? error.message : 'Failed to send reset email'
      )
    } finally {
      setIsLoading(false)
    }
  }

  if (isSuccess) {
    return (
      <div className="min-h-screen bg-animated flex items-center justify-center px-4 relative overflow-hidden">
        {/* Background effects */}
        <div className="absolute inset-0 grid-pattern opacity-30" />
        <div className="aurora-glow w-96 h-96 bg-accent-primary top-0 left-0" />
        <div className="aurora-glow w-96 h-96 bg-accent-secondary bottom-0 right-0" />

        {/* Success card */}
        <div className="glass-card w-full max-w-md p-8 relative z-10 animate-scale-in text-center">
          <div className="w-16 h-16 bg-green-500/20 rounded-full flex items-center justify-center mx-auto mb-6">
            <svg className="w-8 h-8 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
            </svg>
          </div>

          <h1 className="text-3xl font-bold gradient-text mb-3">Check Your Email</h1>
          <p className="text-gray-400 mb-8">
            We've sent a password reset link to{' '}
            <span className="text-white font-medium">{email}</span>
          </p>

          <div className="space-y-4 text-sm text-gray-400 mb-8">
            <p>Click the link in the email to reset your password.</p>
            <p>The link will expire in 24 hours.</p>
          </div>

          <div className="space-y-4">
            <Button
              type="button"
              variant="primary"
              size="lg"
              className="w-full"
              onClick={() => router.push('/auth/login')}
            >
              Back to Login
            </Button>
            <p className="text-center text-gray-400 text-sm">
              Didn't receive the email?{' '}
              <button
                onClick={() => {
                  setIsSuccess(false)
                  handleSubmit(new Event('submit') as any)
                }}
                className="text-accent-primary hover:text-accent-secondary font-medium transition-colors"
                disabled={isLoading}
              >
                Resend email
              </button>
            </p>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-animated flex items-center justify-center px-4 relative overflow-hidden">
      {/* Background effects */}
      <div className="absolute inset-0 grid-pattern opacity-30" />
      <div className="aurora-glow w-96 h-96 bg-accent-primary top-0 left-0" />
      <div className="aurora-glow w-96 h-96 bg-accent-secondary bottom-0 right-0" />

      {/* Forgot password card */}
      <div className="glass-card w-full max-w-md p-8 relative z-10 animate-scale-in">
        {/* Logo/Brand */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold gradient-text mb-2">Forgot Password?</h1>
          <p className="text-gray-400">
            Enter your email to receive a reset link
          </p>
        </div>

        {/* Forgot password form */}
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
                Sending reset link...
              </span>
            ) : (
              'Send Reset Link'
            )}
          </Button>
        </form>

        {/* Back to login link */}
        <p className="mt-8 text-center text-gray-400 text-sm">
          Remember your password?{' '}
          <Link
            href="/auth/login"
            className="text-accent-primary hover:text-accent-secondary font-medium transition-colors"
          >
            Sign in
          </Link>
        </p>
      </div>
    </div>
  )
}
