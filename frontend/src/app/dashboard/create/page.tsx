'use client'

import { useState, FormEvent } from 'react'
import { useRouter } from 'next/navigation'
import { usePlanStore } from '@/stores/plan-store'
import { AISuggestionModal } from '@/components/dashboard/AISuggestionModal'
import { Button } from '@/components/ui/Button'
import { Textarea } from '@/components/ui/Textarea'
import { Input } from '@/components/ui/Input'
import toast from 'react-hot-toast'
import { apiClient } from '@/lib/api'
import type { Task } from '@/lib/api'

interface AITask {
  id: string
  title: string
  description: string
  priority: number
  ai_category?: string
  ai_priority_score?: number
  ai_reasoning?: string
}

export default function CreatePlanPage() {
  const router = useRouter()
  const { createPlan, isLoading, error, clearError } = usePlanStore()

  const [title, setTitle] = useState('')
  const [description, setDescription] = useState('')
  const [originalThought, setOriginalThought] = useState('')

  // AI Modal state
  const [showAIModal, setShowAIModal] = useState(false)
  const [aiTasks, setAiTasks] = useState<AITask[]>([])
  const [isGeneratingAI, setIsGeneratingAI] = useState(false)
  const [createdPlan, setCreatedPlan] = useState<any>(null)  // Store the created plan

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault()
    clearError()

    // If there's an original thought, generate AI suggestions first
    if (originalThought.trim()) {
      await generateAISuggestions()
    } else {
      // Create plan directly without AI
      try {
        const plan = await createPlan({
          title,
          description,
          original_thought: originalThought,
        })
        router.push(`/dashboard/plans/${plan.id}`)
      } catch {
        // Error is handled by the store
      }
    }
  }

  const generateAISuggestions = async () => {
    setIsGeneratingAI(true)
    try {
      // First create the plan
      const plan = await createPlan({
        title,
        description,
        original_thought: originalThought,
        status: 'draft',
      })

      // Store the created plan for later use
      setCreatedPlan(plan)

      // Generate AI dashboard
      await apiClient.generateDashboard(plan.id)

      // Get the updated plan with AI data
      const updatedPlan = await apiClient.getPlan(plan.id)

      // Parse AI generated data
      if (updatedPlan.ai_generated_data) {
        const aiData = JSON.parse(updatedPlan.ai_generated_data)

        // Convert to AITask format
        const tasks: AITask[] = aiData.tasks?.map((task: any, index: number) => ({
          id: `ai-${index}`,
          title: task.title || task.description?.substring(0, 50) || 'Task',
          description: task.description || '',
          priority: task.priority || 3,
          ai_category: task.category || 'General',
          ai_priority_score: task.priority_score || 5,
          ai_reasoning: task.reasoning || '',
        })) || []

        setAiTasks(tasks)
        setShowAIModal(true)
      } else {
        // No AI data generated, just go to plan
        toast.success('Plan created successfully!')
        router.push(`/dashboard/plans/${plan.id}`)
      }
    } catch (err) {
      toast.error(err instanceof Error ? err.message : 'Failed to generate AI suggestions')
    } finally {
      setIsGeneratingAI(false)
    }
  }

  const handleApproveAITasks = async (approvedTasks: AITask[]) => {
    try {
      // Use the stored created plan
      if (!createdPlan) {
        throw new Error('Plan not found. Please try again.')
      }

      // Create all the approved tasks
      const taskPromises = approvedTasks.map((task) =>
        apiClient.createTask({
          plan_id: createdPlan.id,
          title: task.title,
          description: task.description,
          priority: task.priority,
        })
      )

      await Promise.all(taskPromises)

      // Update plan status to active
      await apiClient.updatePlan(createdPlan.id, { status: 'active' })

      toast.success(`Created ${approvedTasks.length} tasks successfully!`)
      setShowAIModal(false)
      router.push(`/dashboard/plans/${createdPlan.id}`)
    } catch (err) {
      toast.error(err instanceof Error ? err.message : 'Failed to create plan and tasks')
    }
  }

  const examplePrompts = [
    {
      title: 'Launch a SaaS Product',
      thought: 'I want to launch a project management tool for remote teams with AI-powered task prioritization',
    },
    {
      title: 'Learn Web Development',
      thought: 'I want to become a full-stack web developer in 6 months, focusing on React and Node.js',
    },
    {
      title: 'Build a Mobile App',
      thought: 'Create a fitness tracking app with social features and personalized workout plans',
    },
  ]

  return (
    <div className="max-w-4xl mx-auto">
      {/* Error message */}
      {error && (
        <div className="mb-6 p-4 rounded-lg bg-red-500/10 border border-red-500/20">
          <p className="text-red-400 text-sm">{error}</p>
        </div>
      )}

      <form onSubmit={handleSubmit} className="space-y-6">
        {/* Title */}
        <Input
          label="Plan Title"
          type="text"
          placeholder="What do you want to accomplish?"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          required
        />

        {/* Description */}
        <Textarea
          label="Description"
          placeholder="Provide a brief description of your plan..."
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          required
        />

        {/* Original Thought */}
        <div>
          <label className="block text-sm font-medium text-gray-300 mb-3">
            Tell AI about your goal (optional)
          </label>
          <Textarea
            placeholder="Describe your idea in detail. The AI will analyze this and generate a structured plan with tasks categorized by priority and domain..."
            value={originalThought}
            onChange={(e) => setOriginalThought(e.target.value)}
            rows={6}
          />
          <p className="mt-2 text-sm text-gray-500">
            The more details you provide, the better the AI can organize your tasks
          </p>
        </div>

        {/* Example prompts */}
        {!originalThought && (
          <div className="space-y-3">
            <p className="text-sm font-medium text-gray-400">Need inspiration? Try an example:</p>
            <div className="grid gap-3">
              {examplePrompts.map((example, index) => (
                <button
                  key={index}
                  type="button"
                  onClick={() => {
                    setTitle(example.title)
                    setOriginalThought(example.thought)
                  }}
                  className="text-left p-4 rounded-lg bg-white/5 border border-white/10 hover:border-accent-primary/50 hover:bg-white/10 transition-all duration-200 group"
                >
                  <div className="flex items-start gap-3">
                    <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-accent-primary/20 to-accent-secondary/20 flex items-center justify-center flex-shrink-0 group-hover:from-accent-primary/30 group-hover:to-accent-secondary/30 transition-colors">
                      <svg className="w-4 h-4 text-accent-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                      </svg>
                    </div>
                    <div className="flex-1 min-w-0">
                      <p className="text-sm font-medium text-white group-hover:text-accent-primary transition-colors">
                        {example.title}
                      </p>
                      <p className="text-sm text-gray-400 mt-1 line-clamp-2">
                        {example.thought}
                      </p>
                    </div>
                  </div>
                </button>
              ))}
            </div>
          </div>
        )}

        {/* Action buttons */}
        <div className="flex items-center gap-4 pt-4">
          <Button
            type="submit"
            variant="primary"
            size="lg"
            disabled={isLoading || isGeneratingAI}
            className="flex-1"
          >
            {isLoading || isGeneratingAI ? (
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
                {isGeneratingAI ? 'AI is analyzing...' : 'Creating Plan...'}
              </span>
            ) : (
              <span className="flex items-center gap-2">
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                </svg>
                {originalThought.trim() ? 'Generate AI Tasks' : 'Create Plan'}
              </span>
            )}
          </Button>
          <Button
            type="button"
            variant="secondary"
            size="lg"
            onClick={() => router.back()}
            disabled={isLoading}
          >
            Cancel
          </Button>
        </div>
      </form>

      {/* AI Suggestion Modal */}
      {showAIModal && (
        <AISuggestionModal
          isOpen={showAIModal}
          onClose={() => setShowAIModal(false)}
          onApprove={handleApproveAITasks}
          originalThought={originalThought}
          aiSuggestions={aiTasks}
          isLoading={isLoading}
        />
      )}
    </div>
  )
}
