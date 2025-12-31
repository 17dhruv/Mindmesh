'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import { CategoryThreeRow, CategoryData } from '@/components/dashboard/CategoryThreeRow'
import toast from 'react-hot-toast'

export default function CreateAIPage() {
  const router = useRouter()
  const [prompt, setPrompt] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [result, setResult] = useState<CategoryData[] | null>(null)
  const [summary, setSummary] = useState('')
  const [suggestedSteps, setSuggestedSteps] = useState<string[]>([])

  const examplePrompts = [
    "I need to build a website, learn rust, deploy to vercel, design logo, set up database, create REST API, write documentation, test everything, launch marketing campaign",
    "Want to start a podcast: get equipment, find guests, record episodes, edit audio, publish on spotify, create social media, build website, monetize with sponsors",
    "Planning a wedding: book venue, send invitations, choose caterer, pick flowers, hire photographer, buy outfits, plan ceremony, arrange reception"
  ]

  const handleOrganize = async () => {
    if (!prompt.trim()) {
      toast.error('Please enter your thoughts and ideas')
      return
    }

    setIsLoading(true)
    setResult(null)

    try {
      // Call the backend API to organize the prompt
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/ai/organize-prompt`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ prompt }),
      })

      if (!response.ok) {
        throw new Error('Failed to organize tasks')
      }

      const data = await response.json()

      // Set the results
      setResult(data.categories)
      setSummary(data.summary || '')
      setSuggestedSteps(data.suggested_next_steps || [])

      toast.success('Tasks organized successfully!')
    } catch (error) {
      console.error('Error organizing tasks:', error)
      toast.error(error instanceof Error ? error.message : 'Failed to organize tasks')
    } finally {
      setIsLoading(false)
    }
  }

  const handleSaveToPlan = async () => {
    if (!result) return

    toast.success('Plan saved! Redirecting to dashboard...')
    setTimeout(() => {
      router.push('/dashboard')
    }, 1500)
  }

  const handleExampleClick = (example: string) => {
    setPrompt(example)
  }

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <div className="border-b border-white/10 bg-white/5">
        <div className="max-w-6xl mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-2xl font-bold gradient-text">AI Task Organizer</h1>
              <p className="text-sm text-gray-400 mt-1">Turn your messy thoughts into organized action plans</p>
            </div>
            <button
              onClick={() => router.push('/dashboard')}
              className="px-4 py-2 rounded-lg glass-card hover:bg-white/10 transition-colors text-sm"
            >
              ← Back to Dashboard
            </button>
          </div>
        </div>
      </div>

      <div className="max-w-6xl mx-auto px-6 py-8">
        {!result ? (
          /* Input Section */
          <div className="max-w-3xl mx-auto">
            <div className="glass-card rounded-2xl p-8">
              <div className="text-center mb-6">
                <div className="text-5xl mb-4">🪄</div>
                <h2 className="text-2xl font-bold text-white mb-2">Turn Your Messy Thoughts Into Action</h2>
                <p className="text-gray-400">
                  Paste your messy ideas, goals, thoughts, or random notes. AI will organize them into clear categories with actionable tasks.
                </p>
              </div>

              {/* Textarea */}
              <div className="mb-6">
                <label className="block text-sm font-medium text-gray-300 mb-2">
                  Your thoughts (the messier, the better)
                </label>
                <textarea
                  value={prompt}
                  onChange={(e) => setPrompt(e.target.value)}
                  placeholder="I need to build a website, learn rust, deploy to vercel, design logo, set up database..."
                  className="w-full h-48 px-4 py-3 rounded-xl bg-white/5 border border-white/10 text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-accent-primary/50 focus:border-transparent resize-none"
                  disabled={isLoading}
                />
                <p className="text-xs text-gray-500 mt-2">
                  {prompt.length} characters
                </p>
              </div>

              {/* Example Prompts */}
              <div className="mb-6">
                <p className="text-sm text-gray-400 mb-3">Not sure? Try an example:</p>
                <div className="space-y-2">
                  {examplePrompts.map((example, idx) => (
                    <button
                      key={idx}
                      onClick={() => handleExampleClick(example)}
                      className="w-full text-left px-4 py-3 rounded-lg bg-white/5 hover:bg-white/10 transition-colors text-sm text-gray-300 hover:text-white border border-white/10 hover:border-white/20"
                      disabled={isLoading}
                    >
                      {example}
                    </button>
                  ))}
                </div>
              </div>

              {/* Submit Button */}
              <button
                onClick={handleOrganize}
                disabled={isLoading || !prompt.trim()}
                className="w-full py-4 rounded-xl bg-gradient-to-r from-accent-primary to-accent-secondary text-white font-semibold text-lg hover:opacity-90 transition-opacity disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
              >
                {isLoading ? (
                  <>
                    <svg className="animate-spin h-5 w-5" viewBox="0 0 24 24">
                      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
                      <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                    </svg>
                    Organizing Your Thoughts...
                  </>
                ) : (
                  <>
                    <span>🪄</span>
                    AI Magic - Organize My Chaos
                  </>
                )}
              </button>
            </div>
          </div>
        ) : (
          /* Results Section */
          <div>
            {/* Summary */}
            {summary && (
              <div className="glass-card rounded-xl p-6 mb-6">
                <h3 className="text-lg font-semibold text-white mb-2">📊 Summary</h3>
                <p className="text-gray-300">{summary}</p>
              </div>
            )}

            {/* Categories */}
            <div className="space-y-4">
              {result.map((category, idx) => (
                <CategoryThreeRow key={idx} category={category} />
              ))}
            </div>

            {/* Suggested Next Steps */}
            {suggestedSteps.length > 0 && (
              <div className="glass-card rounded-xl p-6 mt-6">
                <h3 className="text-lg font-semibold text-white mb-3">🎯 Suggested Next Steps</h3>
                <ul className="space-y-2">
                  {suggestedSteps.map((step, idx) => (
                    <li key={idx} className="flex items-start gap-3 text-gray-300">
                      <span className="text-accent-primary mt-1">•</span>
                      <span>{step}</span>
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {/* Action Buttons */}
            <div className="flex gap-4 mt-6">
              <button
                onClick={handleSaveToPlan}
                className="flex-1 py-3 rounded-xl bg-gradient-to-r from-accent-primary to-accent-secondary text-white font-semibold hover:opacity-90 transition-opacity"
              >
                💾 Save as Plan
              </button>
              <button
                onClick={() => {
                  setResult(null)
                  setSummary('')
                  setSuggestedSteps([])
                }}
                className="px-6 py-3 rounded-xl glass-card hover:bg-white/10 transition-colors text-white font-medium"
              >
                Start Over
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}
