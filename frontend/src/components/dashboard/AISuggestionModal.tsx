'use client'

import { useState } from 'react'
import { X, Check, X as XIcon, Edit3 } from 'lucide-react'
import { Button } from '@/components/ui/Button'
import { Input } from '@/components/ui/Input'
import { Textarea } from '@/components/ui/Textarea'
import toast from 'react-hot-toast'

interface AITask {
  id: string
  title: string
  description: string
  priority: number
  ai_category?: string
  ai_priority_score?: number
  ai_reasoning?: string
}

interface AISuggestionModalProps {
  isOpen: boolean
  onClose: () => void
  onApprove: (tasks: AITask[]) => Promise<void>
  originalThought: string
  aiSuggestions: AITask[]
  isLoading?: boolean
}

export function AISuggestionModal({
  isOpen,
  onClose,
  onApprove,
  originalThought,
  aiSuggestions,
  isLoading = false,
}: AISuggestionModalProps) {
  const [tasks, setTasks] = useState<AITask[]>(aiSuggestions)
  const [editingTask, setEditingTask] = useState<string | null>(null)
  const [showReasoning, setShowReasoning] = useState<Record<string, boolean>>({})

  if (!isOpen) return null

  const groupedTasks = tasks.reduce((acc, task) => {
    const category = task.ai_category || 'Uncategorized'
    if (!acc[category]) acc[category] = []
    acc[category].push(task)
    return acc
  }, {} as Record<string, AITask[]>)

  const handleTaskChange = (taskId: string, field: keyof AITask, value: string | number) => {
    setTasks((prev) =>
      prev.map((task) =>
        task.id === taskId ? { ...task, [field]: value } : task
      )
    )
  }

  const handleRemoveTask = (taskId: string) => {
    setTasks((prev) => prev.filter((task) => task.id !== taskId))
  }

  const getPriorityColor = (score: number) => {
    if (score >= 8) return 'text-red-400 bg-red-500/10 border-red-500/30'
    if (score >= 5) return 'text-yellow-400 bg-yellow-500/10 border-yellow-500/30'
    return 'text-green-400 bg-green-500/10 border-green-500/30'
  }

  const getCategoryIcon = (category: string) => {
    const icons: Record<string, string> = {
      Planning: '📋',
      Development: '💻',
      Design: '🎨',
      Marketing: '📢',
      Research: '🔍',
      Testing: '🧪',
      Deployment: '🚀',
      Documentation: '📝',
      Default: '📌',
    }
    return icons[category] || icons.Default
  }

  const handleApprove = async () => {
    try {
      await onApprove(tasks)
    } catch (error) {
      toast.error('Failed to save tasks')
    }
  }

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/70 backdrop-blur-sm">
      <div className="glass-card w-full max-w-5xl max-h-[90vh] overflow-hidden flex flex-col">
        {/* Header */}
        <div className="p-6 border-b border-white/10">
          <div className="flex items-start justify-between">
            <div className="flex-1">
              <div className="flex items-center gap-3 mb-2">
                <div className="w-10 h-10 rounded-lg bg-gradient-to-br from-accent-primary to-accent-secondary flex items-center justify-center">
                  <Edit3 className="w-5 h-5 text-white" />
                </div>
                <div>
                  <h2 className="text-2xl font-bold text-white">AI-Generated Plan</h2>
                  <p className="text-sm text-gray-400">
                    {tasks.length} tasks organized into {Object.keys(groupedTasks).length} categories
                  </p>
                </div>
              </div>
            </div>
            <button
              onClick={onClose}
              className="text-gray-400 hover:text-white transition-colors"
              disabled={isLoading}
            >
              <X className="w-6 h-6" />
            </button>
          </div>
        </div>

        {/* Content */}
        <div className="flex-1 overflow-y-auto p-6 space-y-6">
          {/* Original Thought */}
          {originalThought && (
            <div className="bg-accent-primary/5 border border-accent-primary/20 rounded-lg p-4">
              <p className="text-sm text-gray-400 mb-2 font-medium">Your Original Idea:</p>
              <p className="text-white">{originalThought}</p>
            </div>
          )}

          {/* Grouped Tasks */}
          <div className="space-y-6">
            {Object.entries(groupedTasks).map(([category, categoryTasks]) => (
              <div key={category}>
                <div className="flex items-center gap-2 mb-3">
                  <span className="text-2xl">{getCategoryIcon(category)}</span>
                  <h3 className="text-lg font-semibold text-white">{category}</h3>
                  <span className="text-sm text-gray-500">({categoryTasks.length} tasks)</span>
                </div>
                <div className="space-y-3 ml-8">
                  {categoryTasks.map((task) => (
                    <div
                      key={task.id}
                      className="bg-white/5 border border-white/10 rounded-lg p-4 hover:border-accent-primary/30 transition-colors"
                    >
                      {editingTask === task.id ? (
                        <div className="space-y-3">
                          <Input
                            label="Task Title"
                            value={task.title}
                            onChange={(e) => handleTaskChange(task.id, 'title', e.target.value)}
                          />
                          <Textarea
                            label="Description"
                            value={task.description}
                            onChange={(e) => handleTaskChange(task.id, 'description', e.target.value)}
                            rows={2}
                          />
                          <div className="grid grid-cols-2 gap-3">
                            <div>
                              <label className="block text-sm text-gray-400 mb-1">Priority (1-5)</label>
                              <input
                                type="number"
                                min="1"
                                max="5"
                                value={task.priority}
                                onChange={(e) => handleTaskChange(task.id, 'priority', parseInt(e.target.value))}
                                className="w-full px-3 py-2 bg-white/5 border border-white/10 rounded-lg text-white"
                              />
                            </div>
                            <div>
                              <label className="block text-sm text-gray-400 mb-1">Category</label>
                              <input
                                type="text"
                                value={task.ai_category || ''}
                                onChange={(e) => handleTaskChange(task.id, 'ai_category', e.target.value)}
                                className="w-full px-3 py-2 bg-white/5 border border-white/10 rounded-lg text-white"
                              />
                            </div>
                          </div>
                          <div className="flex gap-2">
                            <Button
                              type="button"
                              variant="primary"
                              size="sm"
                              onClick={() => setEditingTask(null)}
                            >
                              <Check className="w-4 h-4 mr-1" />
                              Save
                            </Button>
                            <Button
                              type="button"
                              variant="ghost"
                              size="sm"
                              onClick={() => setEditingTask(null)}
                            >
                              Cancel
                            </Button>
                          </div>
                        </div>
                      ) : (
                        <div>
                          <div className="flex items-start justify-between mb-2">
                            <div className="flex-1">
                              <div className="flex items-center gap-2 mb-1">
                                <h4 className="text-white font-medium">{task.title}</h4>
                                {task.ai_priority_score && (
                                  <span
                                    className={`px-2 py-0.5 text-xs font-medium rounded border ${getPriorityColor(
                                      task.ai_priority_score
                                    )}`}
                                  >
                                    Score: {task.ai_priority_score}/10
                                  </span>
                                )}
                              </div>
                              <p className="text-sm text-gray-400">{task.description}</p>
                            </div>
                            <div className="flex items-center gap-2 ml-4">
                              <button
                                onClick={() => setEditingTask(task.id)}
                                className="text-gray-400 hover:text-accent-primary transition-colors"
                              >
                                <Edit3 className="w-4 h-4" />
                              </button>
                              <button
                                onClick={() => handleRemoveTask(task.id)}
                                className="text-gray-400 hover:text-red-400 transition-colors"
                              >
                                <XIcon className="w-4 h-4" />
                              </button>
                            </div>
                          </div>

                          {/* AI Reasoning */}
                          {task.ai_reasoning && (
                            <details className="mt-2">
                              <summary
                                className="text-xs text-accent-primary cursor-pointer hover:text-accent-secondary transition-colors"
                                onClick={() => setShowReasoning((prev) => ({ ...prev, [task.id]: !prev[task.id] }))}
                              >
                                {showReasoning[task.id] ? 'Hide' : 'Show'} AI Reasoning
                              </summary>
                              {showReasoning[task.id] && (
                                <p className="mt-2 text-xs text-gray-500 bg-black/20 p-2 rounded">
                                  {task.ai_reasoning}
                                </p>
                              )}
                            </details>
                          )}
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Footer */}
        <div className="p-6 border-t border-white/10 bg-white/5">
          <div className="flex items-center justify-between">
            <div className="text-sm text-gray-400">
              <p>You can edit tasks before approving. Removed tasks won't be created.</p>
            </div>
            <div className="flex gap-3">
              <Button
                type="button"
                variant="ghost"
                size="lg"
                onClick={onClose}
                disabled={isLoading}
              >
                Reject All
              </Button>
              <Button
                type="button"
                variant="primary"
                size="lg"
                onClick={handleApprove}
                disabled={isLoading || tasks.length === 0}
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
                    Saving...
                  </span>
                ) : (
                  <span className="flex items-center gap-2">
                    <Check className="w-5 h-5" />
                    Approve & Create {tasks.length} Tasks
                  </span>
                )}
              </Button>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
