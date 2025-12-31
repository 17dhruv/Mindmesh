-- Add missing AI columns to tasks table
-- This migration adds the AI-specific columns that the backend expects

-- Add AI columns to tasks table
ALTER TABLE public.tasks
ADD COLUMN IF NOT EXISTS ai_category VARCHAR(255),
ADD COLUMN IF NOT EXISTS ai_priority_score INTEGER,
ADD COLUMN IF NOT EXISTS ai_reasoning TEXT;

-- Add indexes for AI columns
CREATE INDEX IF NOT EXISTS idx_tasks_ai_category ON public.tasks(ai_category);
CREATE INDEX IF NOT EXISTS idx_tasks_ai_priority_score ON public.tasks(ai_priority_score);

-- Update ai_interactions table to match backend expectations
ALTER TABLE public.ai_interactions
ADD COLUMN IF NOT EXISTS request_data JSONB,
ADD COLUMN IF NOT EXISTS response_data JSONB,
ADD COLUMN IF NOT EXISTS tokens_used INTEGER DEFAULT 0,
ADD COLUMN IF NOT EXISTS cost_estimate DECIMAL(10, 6);

-- Add comment for documentation
COMMENT ON COLUMN public.tasks.ai_category IS 'AI-generated task category (e.g., Development, Design, Testing)';
COMMENT ON COLUMN public.tasks.ai_priority_score IS 'AI-calculated priority score (1-10)';
COMMENT ON COLUMN public.tasks.ai_reasoning IS 'AI reasoning for the assigned priority and category';
