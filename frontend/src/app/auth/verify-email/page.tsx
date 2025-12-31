'use client'

import { useState, useEffect } from 'react'
import { useSearchParams, useRouter } from 'next/navigation'
import { useAuth } from '@/contexts/AuthContext'
import { auth } from '@/lib/supabase'
import { Button } from '@/components/ui/Button'
import toast from 'react-hot-toast'

export const dynamic = 'force-dynamic'

export default function VerifyEmailPage() {
  const router = useRouter()
  const searchParams = useSearchParams()
  const { user } = useAuth()
  const [isResending, setIsResending] = useState(false)
  const [isChecking, setIsChecking] = useState(true)

  useEffect(() => {
    // Check if user is already verified
    if (user?.email_confirmed_at) {
      toast.success('Email already verified!')
      setTimeout(() => router.push('/dashboard'), 1500)
    } else {
      setIsChecking(false)
    }
  }, [user, router])

  const handleResendEmail = async () => {
    setIsResending(true)
    try {
      await auth.sendVerificationEmail()
      toast.success('Verification email resent!')
    } catch (error) {
      toast.error(
        error instanceof Error ? error.message : 'Failed to resend verification email'
      )
    } finally {
      setIsResending(false)
    }
  }

  const handleContinueAnyway = () => {
    router.push('/dashboard')
  }

  if (isChecking) {
    return (
      <div className="min-h-screen bg-animated flex items-center justify-center px-4 relative overflow-hidden">
        <div className="glass-card p-8 relative z-10">
          <div className="flex items-center gap-4">
            <svg className="animate-spin h-6 w-6 text-accent-primary" viewBox="0 0 24 24">
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
            <p className="text-gray-400">Checking verification status...</p>
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

      {/* Verification card */}
      <div className="glass-card w-full max-w-md p-8 relative z-10 animate-scale-in">
        {/* Icon */}
        <div className="w-20 h-20 bg-accent-primary/20 rounded-full flex items-center justify-center mx-auto mb-6">
          <svg className="w-10 h-10 text-accent-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
          </svg>
        </div>

        {/* Message */}
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold gradient-text mb-3">Verify Your Email</h1>
          <p className="text-gray-400">
            We've sent a verification email to{' '}
            <span className="text-white font-medium">{user?.email}</span>
          </p>
        </div>

        {/* Instructions */}
        <div className="bg-white/5 rounded-lg p-4 mb-8 space-y-2 text-sm text-gray-400">
          <p>1. Check your email inbox</p>
          <p>2. Click the verification link in the email</p>
          <p>3. You'll be automatically redirected</p>
          <p className="text-xs mt-3 text-gray-500">
            The link will expire in 24 hours
          </p>
        </div>

        {/* Actions */}
        <div className="space-y-4">
          <Button
            type="button"
            variant="primary"
            size="lg"
            className="w-full"
            onClick={handleResendEmail}
            disabled={isResending}
          >
            {isResending ? (
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
                Resending email...
              </span>
            ) : (
              'Resend Verification Email'
            )}
          </Button>

          <Button
            type="button"
            variant="glass"
            size="lg"
            className="w-full"
            onClick={handleContinueAnyway}
          >
            Continue to Dashboard
          </Button>

          <p className="text-center text-gray-400 text-sm">
            Already verified?{' '}
            <button
              onClick={() => router.refresh()}
              className="text-accent-primary hover:text-accent-secondary font-medium transition-colors"
            >
              Refresh page
            </button>
          </p>
        </div>
      </div>
    </div>
  )
}
