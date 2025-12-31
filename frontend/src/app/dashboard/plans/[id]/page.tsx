'use client'

import { useEffect, useState } from 'react'
import { useRouter, useParams } from 'next/navigation'
import { usePlanStore } from '@/stores/plan-store'
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

export default function PlanDetailsPage() {
  const router = useRouter()
  const params = useParams()
  const planId = params.id as string

  const { currentPlan, tasks, isLoading, fetchPlan, fetchTasks, updateTask, generateAIDashboard, isGeneratingAI } = usePlanStore()
  const [filterCategory, setFilterCategory] = useState<string | null>(null)

  useEffect(() => {
    if (planId) {
      fetchPlan(planId)
      fetchTasks(planId)
    }
  }, [planId, fetchPlan, fetchTasks])

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

  // Get filtered categories
  const filteredCategories = filterCategory
    ? { [filterCategory]: groupedTasks[filterCategory] }
    : groupedTasks

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

  const getPriorityColor = (score?: number) => {
    if (!score) return 'bg-gray-500/20 text-gray-400 border-gray-500/30'
    if (score >= 8) return 'bg-red-500/20 text-red-400 border-red-500/30'
    if (score >= 6) return 'bg-orange-500/20 text-orange-400 border-orange-500/30'
    if (score >= 4) return 'bg-yellow-500/20 text-yellow-400 border-yellow-500/30'
    return 'bg-green-500/20 text-green-400 border-green-500/30'
  }

  const handleTaskStatusChange = async (taskId: string, newStatus: 'pending' | 'in_progress' | 'completed') => {
    await updateTask(taskId, { status: newStatus })
  }

  const handleGenerateAI = async () => {
    if (currentPlan) {
      await generateAIDashboard(currentPlan.id)
    }
  }

  if (isLoading || !currentPlan) {
    return (
      <div className="flex items-center justify-center py-12">
        <svg className="animate-spin h-8 w-8 text-accent-primary" viewBox="0 0 24 24">
          <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
          <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
        </svg>
      </div>
    )
  }

  // Get unique categories for filter
  const categories = Object.keys(groupedTasks)

  return (
    <div className="space-y-6">
      {/* Back button */}
      <Button
        variant="ghost"
        size="sm"
        onClick={() => router.push('/dashboard/plans')}
        className="flex items-center gap-2"
      >
        <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
        </svg>
        Back to Plans
      </Button>

      {/* Plan header */}
      <div className="glass-card p-6">
        <div className="flex items-start justify-between">
          <div className="flex-1">
            <h1 className="text-3xl font-bold text-white mb-2">{currentPlan.title}</h1>
            <p className="text-gray-400 mb-4">{currentPlan.description}</p>

            {currentPlan.original_thought && (
              <div className="p-4 rounded-lg bg-white/5 border border-white/10">
                <p className="text-sm text-gray-300 italic">&ldquo;{currentPlan.original_thought}&rdquo;</p>
              </div>
            )}
          </div>

          <div className="flex items-center gap-2">
            <Button
              variant="secondary"
              size="md"
              onClick={handleGenerateAI}
              disabled={isGeneratingAI}
              className="flex items-center gap-2"
            >
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
              </svg>
              {isGeneratingAI ? 'Generating...' : 'Regenerate AI'}
            </Button>
          </div>
        </div>
      </div>

      {/* Filters */}
      <div className="flex items-center gap-4 flex-wrap">
        <span className="text-sm text-gray-400">Filter by:</span>

        {/* Category filter */}
        <div className="flex items-center gap-2">
          <button
            onClick={() => setFilterCategory(null)}
            className={cn(
              'px-3 py-1.5 text-sm rounded-lg border transition-colors',
              filterCategory === null
                ? 'bg-accent-primary/20 text-accent-primary border-accent-primary/30'
                : 'bg-white/5 text-gray-400 border-white/10 hover:border-white/20'
            )}
          >
            All Categories
          </button>
          {categories.map((cat) => (
            <button
              key={cat}
              onClick={() => setFilterCategory(cat)}
              className={cn(
                'px-3 py-1.5 text-sm rounded-lg border transition-colors capitalize',
                filterCategory === cat
                  ? 'bg-accent-primary/20 text-accent-primary border-accent-primary/30'
                  : 'bg-white/5 text-gray-400 border-white/10 hover:border-white/20'
              )}
            >
              {cat === 'uncategorized' ? 'Other' : cat}
            </button>
          ))}
        </div>
      </div>

      {/* Categorized tasks */}
      {Object.keys(filteredCategories).length > 0 ? (
        <div className="space-y-6">
          {Object.entries(filteredCategories).map(([category, categoryTasks]) => {
            if (categoryTasks.length === 0) return null

            return (
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
                    <h3 className="text-lg font-semibold text-white capitalize">
                      {category === 'uncategorized' ? 'Other Tasks' : category}
                    </h3>
                    <p className="text-sm text-gray-400">
                      {categoryTasks.length} task{categoryTasks.length !== 1 ? 's' : ''}
                    </p>
                  </div>
                </div>

                {/* Tasks list */}
                <div className="space-y-3">
                  {categoryTasks.map((task) => (
                    <div
                      key={task.id}
                      className={cn(
                        'p-4 rounded-lg border transition-all duration-200',
                        task.status === 'completed'
                          ? 'bg-green-500/5 border-green-500/20 opacity-70'
                          : 'bg-white/5 border-white/10 hover:border-accent-primary/50'
                      )}
                    >
                      <div className="flex items-start gap-3">
                        {/* Status checkbox */}
                        <button
                          onClick={() => {
                            const newStatus = task.status === 'completed' ? 'pending' : 'completed'
                            handleTaskStatusChange(task.id, newStatus)
                          }}
                          className={cn(
                            'mt-0.5 w-5 h-5 rounded border flex items-center justify-center flex-shrink-0 transition-colors',
                            task.status === 'completed'
                              ? 'bg-green-500 border-green-500'
                              : 'border-gray-500 hover:border-accent-primary'
                          )}
                        >
                          {task.status === 'completed' && (
                            <svg className="w-3 h-3 text-white" fill="currentColor" viewBox="0 0 20 20">
                              <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                            </svg>
                          )}
                        </button>

                        {/* Task content */}
                        <div className="flex-1 min-w-0">
                          <div className="flex items-center gap-2 mb-1 flex-wrap">
                            <h4 className={cn(
                              'text-sm font-medium text-white',
                              task.status === 'completed' && 'line-through'
                            )}>
                              {task.title}
                            </h4>
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
                            <p className="text-sm text-gray-400">{task.description}</p>
                          )}
                          {task.ai_reasoning && (
                            <p className="text-xs text-gray-500 mt-2 italic">
                              AI: {task.ai_reasoning}
                            </p>
                          )}
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )
          })}
        </div>
      ) : (
        /* Empty state */
        <div className="glass-card p-12 text-center">
          <h3 className="text-xl font-semibold text-white mb-2">No tasks yet</h3>
          <p className="text-gray-400">
            Generate tasks with AI or create them manually
          </p>
        </div>
      )}
    </div>
  )
}
