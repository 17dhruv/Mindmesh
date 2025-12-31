'use client'

import { useEffect } from 'react'
import { useRouter } from 'next/navigation'
import Link from 'next/link'
import { usePlanStore } from '@/stores/plan-store'
import { useAuthStore } from '@/stores/auth-store'
import { Button } from '@/components/ui/Button'
import { cn } from '@/lib/utils'
import { formatRelativeTime } from '@/lib/utils'

export const dynamic = 'force-dynamic'

export default function PlansPage() {
  const router = useRouter()
  const { user } = useAuthStore()
  const { plans, isLoading, fetchPlans } = usePlanStore()

  useEffect(() => {
    if (user) {
      fetchPlans()
    }
  }, [user, fetchPlans])

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'accepted':
        return 'bg-green-500/20 text-green-400 border-green-500/30'
      case 'draft':
        return 'bg-yellow-500/20 text-yellow-400 border-yellow-500/30'
      case 'archived':
        return 'bg-gray-500/20 text-gray-400 border-gray-500/30'
      default:
        return 'bg-gray-500/20 text-gray-400 border-gray-500/30'
    }
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold text-white">My Plans</h2>
          <p className="text-gray-400 mt-1">
            {plans.length === 0
              ? "Create your first plan to get started"
              : `${plans.length} plan${plans.length !== 1 ? 's' : ''} total`
            }
          </p>
        </div>
        <Button
          variant="primary"
          size="lg"
          onClick={() => router.push('/dashboard/create')}
          className="flex items-center gap-2"
        >
          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
          </svg>
          New Plan
        </Button>
      </div>

      {/* Plans list */}
      {isLoading ? (
        <div className="flex items-center justify-center py-12">
          <svg className="animate-spin h-8 w-8 text-accent-primary" viewBox="0 0 24 24">
            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
          </svg>
        </div>
      ) : plans.length > 0 ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {plans.map((plan) => (
            <Link
              key={plan.id}
              href={`/dashboard/plans/${plan.id}`}
              className="glass-card p-6 hover:border-accent-primary/50 transition-all duration-200 group"
            >
              {/* Status badge */}
              <div className="flex items-center justify-between mb-4">
                <span className={cn(
                  'px-3 py-1 text-xs font-medium rounded-full border',
                  getStatusColor(plan.status)
                )}>
                  {plan.status}
                </span>
                <svg className="w-5 h-5 text-gray-500 group-hover:text-accent-primary group-hover:translate-x-1 transition-all" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                </svg>
              </div>

              {/* Title */}
              <h3 className="text-lg font-semibold text-white mb-2 group-hover:text-accent-primary transition-colors">
                {plan.title}
              </h3>

              {/* Description */}
              <p className="text-sm text-gray-400 line-clamp-2 mb-4">
                {plan.description}
              </p>

              {/* Original thought snippet */}
              {plan.original_thought && (
                <div className="p-3 rounded-lg bg-white/5 border border-white/10 mb-4">
                  <p className="text-xs text-gray-500 line-clamp-2 italic">
                    &ldquo;{plan.original_thought}&rdquo;
                  </p>
                </div>
              )}

              {/* Footer */}
              <div className="flex items-center justify-between text-xs text-gray-500">
                <span>Created {formatRelativeTime(plan.created_at)}</span>
                {plan.updated_at !== plan.created_at && (
                  <span>Updated {formatRelativeTime(plan.updated_at)}</span>
                )}
              </div>
            </Link>
          ))}
        </div>
      ) : (
        /* Empty state */
        <div className="glass-card p-12 text-center">
          <div className="w-20 h-20 rounded-full bg-gradient-to-br from-accent-primary/20 to-accent-secondary/20 flex items-center justify-center mx-auto mb-6">
            <svg className="w-10 h-10 text-accent-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
            </svg>
          </div>
          <h3 className="text-xl font-semibold text-white mb-2">No plans yet</h3>
          <p className="text-gray-400 mb-6">
            Create your first plan and let AI help you organize your tasks
          </p>
          <Button
            variant="primary"
            size="lg"
            onClick={() => router.push('/dashboard/create')}
          >
            Create Your First Plan
          </Button>
        </div>
      )}
    </div>
  )
}
