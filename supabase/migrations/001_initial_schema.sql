-- Mindmesh Database Schema
-- This file sets up the initial database structure for MVP

-- Extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- Users table (syncs with Supabase auth.users)
CREATE TABLE public.users (
    id UUID REFERENCES auth.users(id) PRIMARY KEY,
    email TEXT UNIQUE NOT NULL,
    full_name TEXT,
    avatar_url TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Plans table - the main container for task plans
CREATE TABLE public.plans (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    user_id UUID REFERENCES public.users(id) ON DELETE CASCADE NOT NULL,
    title TEXT NOT NULL,
    description TEXT,
    original_thought TEXT, -- The raw user input/thought
    status TEXT DEFAULT 'draft' CHECK (status IN ('draft', 'approved', 'active', 'completed', 'archived')),
    ai_generated_data JSONB, -- Structured AI output (tasks, priorities, etc.)
    metadata JSONB, -- Additional plan metadata
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Tasks table - individual tasks within plans
CREATE TABLE public.tasks (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    plan_id UUID REFERENCES public.plans(id) ON DELETE CASCADE NOT NULL,
    parent_task_id UUID REFERENCES public.tasks(id) ON DELETE CASCADE, -- For subtasks
    title TEXT NOT NULL,
    description TEXT,
    priority INTEGER DEFAULT 3 CHECK (priority BETWEEN 1 AND 5), -- 1=highest, 5=lowest
    status TEXT DEFAULT 'pending' CHECK (status IN ('pending', 'in_progress', 'completed', 'cancelled')),
    estimated_duration INTEGER, -- in minutes
    actual_duration INTEGER, -- in minutes
    position_x FLOAT, -- For graph visualization
    position_y FLOAT, -- For graph visualization
    metadata JSONB, -- Additional task metadata
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    completed_at TIMESTAMP WITH TIME ZONE
);

-- Task dependencies table
CREATE TABLE public.task_dependencies (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    task_id UUID REFERENCES public.tasks(id) ON DELETE CASCADE,
    depends_on_task_id UUID REFERENCES public.tasks(id) ON DELETE CASCADE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(task_id, depends_on_task_id)
);

-- AI interactions table - track AI usage and costs
CREATE TABLE public.ai_interactions (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    user_id UUID REFERENCES public.users(id) ON DELETE CASCADE NOT NULL,
    plan_id UUID REFERENCES public.plans(id) ON DELETE CASCADE,
    interaction_type TEXT NOT NULL CHECK (interaction_type IN ('thought_to_plan', 'plan_refinement', 'task_suggestion')),
    input_tokens INTEGER,
    output_tokens INTEGER,
    model_used TEXT,
    cost DECIMAL(10, 6), -- Track costs
    response_time INTEGER, -- in milliseconds
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- User sessions table - track active planning sessions
CREATE TABLE public.user_sessions (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    user_id UUID REFERENCES public.users(id) ON DELETE CASCADE NOT NULL,
    started_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    ended_at TIMESTAMP WITH TIME ZONE,
    session_data JSONB -- Store session state
);

-- Indexes for performance
CREATE INDEX idx_plans_user_id ON public.plans(user_id);
CREATE INDEX idx_plans_status ON public.plans(status);
CREATE INDEX idx_plans_created_at ON public.plans(created_at DESC);

CREATE INDEX idx_tasks_plan_id ON public.tasks(plan_id);
CREATE INDEX idx_tasks_parent_task_id ON public.tasks(parent_task_id);
CREATE INDEX idx_tasks_status ON public.tasks(status);
CREATE INDEX idx_tasks_priority ON public.tasks(priority);

CREATE INDEX idx_ai_interactions_user_id ON public.ai_interactions(user_id);
CREATE INDEX idx_ai_interactions_created_at ON public.ai_interactions(created_at DESC);

CREATE INDEX idx_user_sessions_user_id ON public.user_sessions(user_id);

-- RLS (Row Level Security) Policies
ALTER TABLE public.users ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.plans ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.tasks ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.task_dependencies ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.ai_interactions ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.user_sessions ENABLE ROW LEVEL SECURITY;

-- Users can only see their own data
CREATE POLICY "Users can view own profile" ON public.users
    FOR SELECT USING (auth.uid() = id);

CREATE POLICY "Users can update own profile" ON public.users
    FOR UPDATE USING (auth.uid() = id);

-- Plans policies
CREATE POLICY "Users can view own plans" ON public.plans
    FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can create own plans" ON public.plans
    FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own plans" ON public.plans
    FOR UPDATE USING (auth.uid() = user_id);

CREATE POLICY "Users can delete own plans" ON public.plans
    FOR DELETE USING (auth.uid() = user_id);

-- Tasks policies
CREATE POLICY "Users can view own tasks" ON public.tasks
    FOR SELECT USING (EXISTS (
        SELECT 1 FROM public.plans
        WHERE plans.id = tasks.plan_id AND plans.user_id = auth.uid()
    ));

CREATE POLICY "Users can create own tasks" ON public.tasks
    FOR INSERT WITH CHECK (EXISTS (
        SELECT 1 FROM public.plans
        WHERE plans.id = tasks.plan_id AND plans.user_id = auth.uid()
    ));

CREATE POLICY "Users can update own tasks" ON public.tasks
    FOR UPDATE USING (EXISTS (
        SELECT 1 FROM public.plans
        WHERE plans.id = tasks.plan_id AND plans.user_id = auth.uid()
    ));

CREATE POLICY "Users can delete own tasks" ON public.tasks
    FOR DELETE USING (EXISTS (
        SELECT 1 FROM public.plans
        WHERE plans.id = tasks.plan_id AND plans.user_id = auth.uid()
    ));

-- Task dependencies policies
CREATE POLICY "Users can view own task dependencies" ON public.task_dependencies
    FOR SELECT USING (EXISTS (
        SELECT 1 FROM public.tasks
        JOIN public.plans ON plans.id = tasks.plan_id
        WHERE (tasks.id = task_dependencies.task_id OR tasks.id = task_dependencies.depends_on_task_id)
        AND plans.user_id = auth.uid()
    ));

CREATE POLICY "Users can create own task dependencies" ON public.task_dependencies
    FOR INSERT WITH CHECK (EXISTS (
        SELECT 1 FROM public.tasks
        JOIN public.plans ON plans.id = tasks.plan_id
        WHERE (tasks.id = task_dependencies.task_id OR tasks.id = task_dependencies.depends_on_task_id)
        AND plans.user_id = auth.uid()
    ));

-- AI interactions policies
CREATE POLICY "Users can view own AI interactions" ON public.ai_interactions
    FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can create own AI interactions" ON public.ai_interactions
    FOR INSERT WITH CHECK (auth.uid() = user_id);

-- User sessions policies
CREATE POLICY "Users can view own sessions" ON public.user_sessions
    FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can create own sessions" ON public.user_sessions
    FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own sessions" ON public.user_sessions
    FOR UPDATE USING (auth.uid() = user_id);

-- Functions and Triggers for updated_at
CREATE OR REPLACE FUNCTION public.handle_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Triggers for updated_at
CREATE TRIGGER handle_users_updated_at
    BEFORE UPDATE ON public.users
    FOR EACH ROW EXECUTE FUNCTION public.handle_updated_at();

CREATE TRIGGER handle_plans_updated_at
    BEFORE UPDATE ON public.plans
    FOR EACH ROW EXECUTE FUNCTION public.handle_updated_at();

CREATE TRIGGER handle_tasks_updated_at
    BEFORE UPDATE ON public.tasks
    FOR EACH ROW EXECUTE FUNCTION public.handle_updated_at();

-- Trigger for task completion timestamp
CREATE TRIGGER set_task_completed_at
    BEFORE UPDATE ON public.tasks
    FOR EACH ROW
    WHEN (OLD.status != 'completed' AND NEW.status = 'completed')
    EXECUTE FUNCTION public.handle_updated_at();

-- Function to create user profile on signup
CREATE OR REPLACE FUNCTION public.handle_new_user()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO public.users (id, email, full_name, avatar_url)
    VALUES (
        NEW.id,
        NEW.email,
        NEW.raw_user_meta_data->>'full_name',
        NEW.raw_user_meta_data->>'avatar_url'
    );
    RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Trigger to create user profile on signup
CREATE TRIGGER on_auth_user_created
    AFTER INSERT ON auth.users
    FOR EACH ROW EXECUTE FUNCTION public.handle_new_user();