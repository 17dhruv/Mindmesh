'use client'

import { useState, FormEvent, useEffect } from 'react'
import { useRouter, useSearchParams } from 'next/navigation'
import { auth } from '@/lib/supabase'
import { Button } from '@/components/ui/Button'
import { Input } from '@/components/ui/Input'
import toast from 'react-hot-toast'

export const dynamic = 'force-dynamic'

export default function ResetPasswordPage() {
  const router = useRouter()
  const searchParams = useSearchParams()
  const [password, setPassword] = useState('')
  const [confirmPassword, setConfirmPassword] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [passwordError, setPasswordError] = useState('')

  useEffect(() => {
    // Check if we have the reset token in the URL
    // Supabase handles this automatically via the access_token in the URL
    const accessToken = searchParams.get('access_token')
    if (!accessToken) {
      toast.error('Invalid or expired reset link')
      router.push('/auth/forgot-password')
    }
  }, [searchParams, router])

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault()
    setPasswordError('')

    // Validate passwords match
    if (password !== confirmPassword) {
      setPasswordError('Passwords do not match')
      return
    }

    // Validate password strength
    if (password.length < 8) {
      setPasswordError('Password must be at least 8 characters')
      return
    }

    setIsLoading(true)

    try {
      await auth.updatePassword(password)
      toast.success('Password updated successfully!')
      router.push('/auth/login')
    } catch (error) {
      toast.error(
        error instanceof Error ? error.message : 'Failed to reset password'
      )
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

      {/* Reset password card */}
      <div className="glass-card w-full max-w-md p-8 relative z-10 animate-scale-in">
        {/* Logo/Brand */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold gradient-text mb-2">Set New Password</h1>
          <p className="text-gray-400">
            Enter your new password below
          </p>
        </div>

        {/* Password error message */}
        {passwordError && (
          <div className="mb-6 p-4 rounded-lg bg-red-500/10 border border-red-500/20">
            <p className="text-red-400 text-sm text-center">{passwordError}</p>
          </div>
        )}

        {/* Reset password form */}
        <form onSubmit={handleSubmit} className="space-y-5">
          <Input
            label="New Password"
            type="password"
            placeholder="••••••••"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
            autoComplete="new-password"
            minLength={8}
          />

          <Input
            label="Confirm New Password"
            type="password"
            placeholder="••••••••"
            value={confirmPassword}
            onChange={(e) => setConfirmPassword(e.target.value)}
            error={passwordError}
            required
            autoComplete="new-password"
            minLength={8}
          />

          {/* Password requirements */}
          <div className="text-xs text-gray-500 space-y-1">
            <p>Password must:</p>
            <ul className="list-disc list-inside space-y-1 ml-2">
              <li>Be at least 8 characters long</li>
              <li>Match the confirmation password</li>
            </ul>
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
                Updating password...
              </span>
            ) : (
              'Update Password'
            )}
          </Button>
        </form>

        {/* Back to login link */}
        <p className="mt-8 text-center text-gray-400 text-sm">
          Remember your password?{' '}
          <button
            onClick={() => router.push('/auth/login')}
            className="text-accent-primary hover:text-accent-secondary font-medium transition-colors"
          >
            Sign in
          </button>
        </p>
      </div>
    </div>
  )
}
