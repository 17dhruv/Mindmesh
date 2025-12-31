'use client'

import { useEffect } from 'react'
import { useRouter } from 'next/navigation'
import Link from 'next/link'
import { usePlanStore } from '@/stores/plan-store'
import { useAuthStore } from '@/stores/auth-store'
import { Button } from '@/components/ui/Button'
import { cn } from '@/lib/utils'

export const dynamic = 'force-dynamic'

// Category icons mapping
const categoryIcons: Record<string, JSX.Element> = {
  research: (
    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
    </svg>
  ),
  development: (
    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4" />
    </svg>
  ),
  design: (
    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 21a4 4 0 01-4-4V5a2 2 0 012-2h4a2 2 0 012 2v12a4 4 0 01-4 4zm0 0h12a2 2 0 002-2v-4a2 2 0 00-2-2h-2.343M11 7.343l1.657-1.657a2 2 0 012.828 0l2.829 2.829a2 2 0 010 2.828l-8.486 8.485M7 17h.01" />
    </svg>
  ),
  marketing: (
    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 5.882V19.24a1.76 1.76 0 01-3.417.592l-2.147-6.15M18 13a3 3 0 100-6M5.436 13.683A4.001 4.001 0 017 6h1.832c4.1 0 7.625-1.234 9.168-3v14c-1.543-1.766-5.067-3-9.168-3H7a3.988 3.988 0 01-1.564-.317z" />
    </svg>
  ),
  testing: (
    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
    </svg>
  ),
  deployment: (
    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
    </svg>
  ),
  planning: (
    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01" />
    </svg>
  ),
  default: (
    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z" />
    </svg>
  ),
}

// Category colors
const categoryColors: Record<string, string> = {
  research: 'from-blue-500/20 to-cyan-500/20 border-blue-500/30',
  development: 'from-purple-500/20 to-pink-500/20 border-purple-500/30',
  design: 'from-pink-500/20 to-rose-500/20 border-pink-500/30',
  marketing: 'from-green-500/20 to-emerald-500/20 border-green-500/30',
  testing: 'from-orange-500/20 to-amber-500/20 border-orange-500/30',
  deployment: 'from-indigo-500/20 to-violet-500/20 border-indigo-500/30',
  planning: 'from-teal-500/20 to-cyan-500/20 border-teal-500/30',
  default: 'from-gray-500/20 to-slate-500/20 border-gray-500/30',
}

export default function DashboardPage() {
  const router = useRouter()
  const { user } = useAuthStore()
  const { plans, tasks, isLoading, fetchPlans, fetchTasks } = usePlanStore()

  useEffect(() => {
    if (user) {
      fetchPlans()
      fetchTasks()
    }
  }, [user, fetchPlans, fetchTasks])

  // Group tasks by category
  const groupedTasks = tasks.reduce((acc, task) => {
    const category = task.ai_category || 'uncategorized'
    if (!acc[category]) {
      acc[category] = []
    }
    acc[category].push(task)
    return acc
  }, {} as Record<string, typeof tasks>)

  // Sort tasks within each category by priority
  Object.keys(groupedTasks).forEach(category => {
    groupedTasks[category].sort((a, b) => (b.ai_priority_score || 0) - (a.ai_priority_score || 0))
  })

  // Get status badge color
  const getStatusColor = (status: string) => {
    switch (status) {
      case 'completed':
        return 'bg-green-500/20 text-green-400 border-green-500/30'
      case 'in_progress':
        return 'bg-blue-500/20 text-blue-400 border-blue-500/30'
      default:
        return 'bg-gray-500/20 text-gray-400 border-gray-500/30'
    }
  }

  // Get priority badge color
  const getPriorityColor = (score?: number) => {
    if (!score) return 'bg-gray-500/20 text-gray-400 border-gray-500/30'
    if (score >= 8) return 'bg-red-500/20 text-red-400 border-red-500/30'
    if (score >= 6) return 'bg-orange-500/20 text-orange-400 border-orange-500/30'
    if (score >= 4) return 'bg-yellow-500/20 text-yellow-400 border-yellow-500/30'
    return 'bg-green-500/20 text-green-400 border-green-500/30'
  }

  return (
    <div className="space-y-8">
      {/* Welcome section */}
      <div className="glass-card p-6 relative overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-r from-accent-primary/10 to-accent-secondary/10" />
        <div className="relative z-10">
          <h2 className="text-2xl font-bold text-white mb-2">
            Welcome back! 👋
          </h2>
          <p className="text-gray-400">
            {tasks.length === 0
              ? "Start by creating your first plan and let AI organize your tasks."
              : `You have ${tasks.filter(t => t.status === 'pending').length} pending tasks across ${plans.length} plans.`}
          </p>
        </div>
      </div>

      {/* Quick actions */}
      <div className="flex items-center gap-4">
        <Button
          variant="primary"
          size="lg"
          onClick={() => router.push('/dashboard/create')}
          className="flex items-center gap-2"
        >
          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
          </svg>
          Create New Plan
        </Button>
        <Button
          variant="glass"
          size="lg"
          onClick={() => router.push('/dashboard/plans')}
        >
          View All Plans
        </Button>
      </div>

      {/* Stats cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="glass-card p-5">
          <div className="flex items-center gap-4">
            <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-blue-500/20 to-cyan-500/20 flex items-center justify-center">
              <svg className="w-6 h-6 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
              </svg>
            </div>
            <div>
              <p className="text-2xl font-bold text-white">{plans.length}</p>
              <p className="text-sm text-gray-400">Total Plans</p>
            </div>
          </div>
        </div>

        <div className="glass-card p-5">
          <div className="flex items-center gap-4">
            <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-purple-500/20 to-pink-500/20 flex items-center justify-center">
              <svg className="w-6 h-6 text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4" />
              </svg>
            </div>
            <div>
              <p className="text-2xl font-bold text-white">{tasks.length}</p>
              <p className="text-sm text-gray-400">Total Tasks</p>
            </div>
          </div>
        </div>

        <div className="glass-card p-5">
          <div className="flex items-center gap-4">
            <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-yellow-500/20 to-orange-500/20 flex items-center justify-center">
              <svg className="w-6 h-6 text-yellow-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <div>
              <p className="text-2xl font-bold text-white">{tasks.filter(t => t.status === 'pending').length}</p>
              <p className="text-sm text-gray-400">Pending</p>
            </div>
          </div>
        </div>

        <div className="glass-card p-5">
          <div className="flex items-center gap-4">
            <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-green-500/20 to-emerald-500/20 flex items-center justify-center">
              <svg className="w-6 h-6 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <div>
              <p className="text-2xl font-bold text-white">{tasks.filter(t => t.status === 'completed').length}</p>
              <p className="text-sm text-gray-400">Completed</p>
            </div>
          </div>
        </div>
      </div>

      {/* Categorized tasks */}
      {isLoading ? (
        <div className="flex items-center justify-center py-12">
          <svg className="animate-spin h-8 w-8 text-accent-primary" viewBox="0 0 24 24">
            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
          </svg>
        </div>
      ) : Object.keys(groupedTasks).length > 0 ? (
        <div className="space-y-6">
          <h3 className="text-xl font-bold text-white">Tasks by Category</h3>
          {Object.entries(groupedTasks).map(([category, categoryTasks]) => (
            <div key={category} className="glass-card p-6">
              {/* Category header */}
              <div className="flex items-center gap-3 mb-4 pb-4 border-b border-white/10">
                <div className={cn(
                  'w-10 h-10 rounded-lg flex items-center justify-center border bg-gradient-to-br',
                  categoryColors[category] || categoryColors.default
                )}>
                  {categoryIcons[category] || categoryIcons.default}
                </div>
                <div className="flex-1">
                  <h4 className="text-lg font-semibold text-white capitalize">
                    {category === 'uncategorized' ? 'Other Tasks' : category}
                  </h4>
                  <p className="text-sm text-gray-400">
                    {categoryTasks.length} task{categoryTasks.length !== 1 ? 's' : ''}
                  </p>
                </div>
              </div>

              {/* Tasks list */}
              <div className="space-y-3">
                {categoryTasks.map((task) => (
                  <Link
                    key={task.id}
                    href={`/dashboard/plans/${task.plan_id}`}
                    className="block p-4 rounded-lg bg-white/5 border border-white/10 hover:border-accent-primary/50 hover:bg-white/10 transition-all duration-200 group"
                  >
                    <div className="flex items-start gap-3">
                      {/* Status indicator */}
                      <div className={cn(
                        'mt-1 w-2 h-2 rounded-full flex-shrink-0',
                        task.status === 'completed' ? 'bg-green-400' :
                        task.status === 'in_progress' ? 'bg-blue-400' :
                        'bg-gray-400'
                      )} />

                      {/* Task content */}
                      <div className="flex-1 min-w-0">
                        <div className="flex items-center gap-2 mb-1">
                          <h5 className={cn(
                            'text-sm font-medium text-white group-hover:text-accent-primary transition-colors',
                            task.status === 'completed' && 'line-through opacity-60'
                          )}>
                            {task.title}
                          </h5>
                          <span className={cn(
                            'px-2 py-0.5 text-xs font-medium rounded-full border',
                            getStatusColor(task.status)
                          )}>
                            {task.status.replace('_', ' ')}
                          </span>
                          {task.ai_priority_score && (
                            <span className={cn(
                              'px-2 py-0.5 text-xs font-medium rounded-full border',
                              getPriorityColor(task.ai_priority_score)
                            )}>
                              P{task.ai_priority_score}
                            </span>
                          )}
                        </div>
                        {task.description && (
                          <p className="text-sm text-gray-400 line-clamp-1">
                            {task.description}
                          </p>
                        )}
                      </div>

                      {/* Arrow icon */}
                      <svg className="w-5 h-5 text-gray-500 group-hover:text-accent-primary group-hover:translate-x-1 transition-all flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                      </svg>
                    </div>
                  </Link>
                ))}
              </div>
            </div>
          ))}
        </div>
      ) : (
        /* Empty state */
        <div className="glass-card p-12 text-center">
          <div className="w-20 h-20 rounded-full bg-gradient-to-br from-accent-primary/20 to-accent-secondary/20 flex items-center justify-center mx-auto mb-6">
            <svg className="w-10 h-10 text-accent-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01" />
            </svg>
          </div>
          <h3 className="text-xl font-semibold text-white mb-2">No tasks yet</h3>
          <p className="text-gray-400 mb-6">
            Create your first plan and let AI organize your tasks into categories
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
