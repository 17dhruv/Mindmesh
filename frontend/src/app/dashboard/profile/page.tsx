'use client'

import { useState, FormEvent } from 'react'
import { useAuth } from '@/contexts/AuthContext'
import { auth } from '@/lib/supabase'
import { Button } from '@/components/ui/Button'
import { Input } from '@/components/ui/Input'
import toast from 'react-hot-toast'

export const dynamic = 'force-dynamic'

export default function ProfilePage() {
  const { user } = useAuth()
  const [isUpdating, setIsUpdating] = useState(false)

  // Profile form state
  const [fullName, setFullName] = useState(user?.user_metadata?.full_name || '')
  const [email] = useState(user?.email || '')

  // Password change form state
  const [currentPassword, setCurrentPassword] = useState('')
  const [newPassword, setNewPassword] = useState('')
  const [confirmPassword, setConfirmPassword] = useState('')
  const [passwordError, setPasswordError] = useState('')

  const userInitial = user?.email?.[0].toUpperCase() || 'U'

  const handleUpdateProfile = async (e: FormEvent) => {
    e.preventDefault()
    setIsUpdating(true)

    try {
      await auth.updateMetadata({ full_name: fullName })
      toast.success('Profile updated successfully!')
    } catch (error) {
      toast.error(
        error instanceof Error ? error.message : 'Failed to update profile'
      )
    } finally {
      setIsUpdating(false)
    }
  }

  const handleChangePassword = async (e: FormEvent) => {
    e.preventDefault()
    setPasswordError('')

    // Validate passwords match
    if (newPassword !== confirmPassword) {
      setPasswordError('New passwords do not match')
      return
    }

    // Validate password strength
    if (newPassword.length < 8) {
      setPasswordError('Password must be at least 8 characters')
      return
    }

    setIsUpdating(true)

    try {
      // First verify current password
      const signInResult = await auth.signIn(email, currentPassword)
      if (signInResult.error) {
        setPasswordError('Current password is incorrect')
        toast.error('Current password is incorrect')
        setIsUpdating(false)
        return
      }

      // Update password
      await auth.updatePassword(newPassword)
      toast.success('Password updated successfully!')

      // Clear form
      setCurrentPassword('')
      setNewPassword('')
      setConfirmPassword('')
      setPasswordError('')
    } catch (error) {
      toast.error(
        error instanceof Error ? error.message : 'Failed to update password'
      )
    } finally {
      setIsUpdating(false)
    }
  }

  const accountCreated = user?.created_at
    ? new Date(user.created_at).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
      })
    : 'Unknown'

  return (
    <div className="max-w-4xl mx-auto space-y-8">
      {/* Profile Header */}
      <div className="glass-card p-8">
        <div className="flex items-center gap-6">
          <div className="w-20 h-20 rounded-full bg-gradient-to-br from-accent-primary to-accent-secondary flex items-center justify-center">
            <span className="text-white font-bold text-3xl">{userInitial}</span>
          </div>
          <div className="flex-1">
            <h2 className="text-2xl font-bold text-white mb-1">{fullName || 'User'}</h2>
            <p className="text-gray-400">{email}</p>
          </div>
        </div>

        <div className="mt-6 pt-6 border-t border-white/10 grid grid-cols-2 gap-4 text-sm">
          <div>
            <p className="text-gray-500 mb-1">Account Created</p>
            <p className="text-white font-medium">{accountCreated}</p>
          </div>
          <div>
            <p className="text-gray-500 mb-1">Email Verified</p>
            <p className="text-white font-medium">
              {user?.email_confirmed_at ? (
                <span className="text-green-400">Verified</span>
              ) : (
                <span className="text-yellow-400">Not Verified</span>
              )}
            </p>
          </div>
        </div>
      </div>

      {/* Update Profile Form */}
      <div className="glass-card p-8">
        <h3 className="text-xl font-bold text-white mb-6">Update Profile</h3>
        <form onSubmit={handleUpdateProfile} className="space-y-5">
          <Input
            label="Full Name"
            type="text"
            placeholder="John Doe"
            value={fullName}
            onChange={(e) => setFullName(e.target.value)}
            required
          />

          <div className="text-gray-500 text-sm">
            <p>Email cannot be changed. Contact support if you need to update your email address.</p>
          </div>

          <Button
            type="submit"
            variant="primary"
            size="lg"
            disabled={isUpdating}
          >
            {isUpdating ? 'Updating...' : 'Update Profile'}
          </Button>
        </form>
      </div>

      {/* Change Password Form */}
      <div className="glass-card p-8">
        <h3 className="text-xl font-bold text-white mb-6">Change Password</h3>
        <form onSubmit={handleChangePassword} className="space-y-5">
          <Input
            label="Current Password"
            type="password"
            placeholder="••••••••"
            value={currentPassword}
            onChange={(e) => setCurrentPassword(e.target.value)}
            required
            autoComplete="current-password"
          />

          <Input
            label="New Password"
            type="password"
            placeholder="••••••••"
            value={newPassword}
            onChange={(e) => setNewPassword(e.target.value)}
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
            disabled={isUpdating}
          >
            {isUpdating ? 'Updating...' : 'Change Password'}
          </Button>
        </form>
      </div>

      {/* Danger Zone */}
      <div className="glass-card p-8 border border-red-500/20">
        <h3 className="text-xl font-bold text-white mb-2">Danger Zone</h3>
        <p className="text-gray-400 text-sm mb-6">
          Irreversible and destructive actions
        </p>
        <div className="flex items-center justify-between p-4 bg-red-500/10 border border-red-500/20 rounded-lg">
          <div>
            <p className="text-white font-medium">Delete Account</p>
            <p className="text-gray-400 text-sm">
              Permanently delete your account and all data
            </p>
          </div>
          <Button
            variant="glass"
            size="md"
            className="text-red-400 hover:text-red-300 hover:bg-red-500/20"
            onClick={() => toast.info('Account deletion not implemented yet. Contact support.')}
          >
            Delete Account
          </Button>
        </div>
      </div>
    </div>
  )
}
