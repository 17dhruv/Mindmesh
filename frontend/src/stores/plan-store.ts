import { create } from 'zustand'
import { apiClient, type Plan, type Task } from '@/lib/api'

interface PlanState {
  plans: Plan[]
  currentPlan: Plan | null
  tasks: Task[]
  isLoading: boolean
  error: string | null
  isGeneratingAI: boolean

  // Plan actions
  fetchPlans: () => Promise<void>
  fetchPlan: (planId: string) => Promise<void>
  createPlan: (data: { title: string; description: string; original_thought?: string; status?: string }) => Promise<Plan>
  updatePlan: (planId: string, data: Partial<Plan>) => Promise<void>
  deletePlan: (planId: string) => Promise<void>
  setCurrentPlan: (plan: Plan | null) => void

  // Task actions
  fetchTasks: (planId?: string) => Promise<void>
  createTask: (data: { plan_id: string; title: string; description: string; priority: number }) => Promise<Task>
  updateTask: (taskId: string, data: Partial<Task>) => Promise<void>
  deleteTask: (taskId: string) => Promise<void>

  // AI actions
  generateAIDashboard: (planId: string) => Promise<void>
  approveAIDashboard: (approved: boolean, feedback?: string) => Promise<void>

  // Utility
  clearError: () => void
  reset: () => void
}

export const usePlanStore = create<PlanState>((set, get) => ({
  plans: [],
  currentPlan: null,
  tasks: [],
  isLoading: false,
  error: null,
  isGeneratingAI: false,

  fetchPlans: async () => {
    set({ isLoading: true, error: null })
    try {
      const plans = await apiClient.getPlans()
      set({ plans, isLoading: false })
    } catch (error) {
      set({
        error: error instanceof Error ? error.message : 'Failed to fetch plans',
        isLoading: false,
      })
    }
  },

  fetchPlan: async (planId: string) => {
    set({ isLoading: true, error: null })
    try {
      const plan = await apiClient.getPlan(planId)
      set({ currentPlan: plan, isLoading: false })
    } catch (error) {
      set({
        error: error instanceof Error ? error.message : 'Failed to fetch plan',
        isLoading: false,
      })
    }
  },

  createPlan: async (data) => {
    set({ isLoading: true, error: null })
    try {
      const plan = await apiClient.createPlan(data)
      set((state) => ({
        plans: [plan, ...state.plans],
        currentPlan: plan,
        isLoading: false,
      }))
      return plan
    } catch (error) {
      set({
        error: error instanceof Error ? error.message : 'Failed to create plan',
        isLoading: false,
      })
      throw error
    }
  },

  updatePlan: async (planId, data) => {
    set({ isLoading: true, error: null })
    try {
      const updatedPlan = await apiClient.updatePlan(planId, data)
      set((state) => ({
        plans: state.plans.map((p) => (p.id === planId ? updatedPlan : p)),
        currentPlan: state.currentPlan?.id === planId ? updatedPlan : state.currentPlan,
        isLoading: false,
      }))
    } catch (error) {
      set({
        error: error instanceof Error ? error.message : 'Failed to update plan',
        isLoading: false,
      })
    }
  },

  deletePlan: async (planId) => {
    set({ isLoading: true, error: null })
    try {
      await apiClient.deletePlan(planId)
      set((state) => ({
        plans: state.plans.filter((p) => p.id !== planId),
        currentPlan: state.currentPlan?.id === planId ? null : state.currentPlan,
        tasks: state.tasks.filter((t) => t.plan_id !== planId),
        isLoading: false,
      }))
    } catch (error) {
      set({
        error: error instanceof Error ? error.message : 'Failed to delete plan',
        isLoading: false,
      })
    }
  },

  setCurrentPlan: (plan) => set({ currentPlan: plan }),

  fetchTasks: async (planId) => {
    set({ isLoading: true, error: null })
    try {
      const tasks = await apiClient.getTasks(planId)
      set({ tasks, isLoading: false })
    } catch (error) {
      set({
        error: error instanceof Error ? error.message : 'Failed to fetch tasks',
        isLoading: false,
      })
    }
  },

  createTask: async (data) => {
    set({ isLoading: true, error: null })
    try {
      const task = await apiClient.createTask(data)
      set((state) => ({
        tasks: [...state.tasks, task],
        isLoading: false,
      }))
      return task
    } catch (error) {
      set({
        error: error instanceof Error ? error.message : 'Failed to create task',
        isLoading: false,
      })
      throw error
    }
  },

  updateTask: async (taskId, data) => {
    set({ isLoading: true, error: null })
    try {
      const updatedTask = await apiClient.updateTask(taskId, data)
      set((state) => ({
        tasks: state.tasks.map((t) => (t.id === taskId ? updatedTask : t)),
        isLoading: false,
      }))
    } catch (error) {
      set({
        error: error instanceof Error ? error.message : 'Failed to update task',
        isLoading: false,
      })
    }
  },

  deleteTask: async (taskId) => {
    set({ isLoading: true, error: null })
    try {
      await apiClient.deleteTask(taskId)
      set((state) => ({
        tasks: state.tasks.filter((t) => t.id !== taskId),
        isLoading: false,
      }))
    } catch (error) {
      set({
        error: error instanceof Error ? error.message : 'Failed to delete task',
        isLoading: false,
      })
    }
  },

  generateAIDashboard: async (planId) => {
    set({ isGeneratingAI: true, error: null })
    try {
      await apiClient.generateDashboard(planId)
      // Refresh the plan to get updated AI data
      await get().fetchPlan(planId)
      set({ isGeneratingAI: false })
    } catch (error) {
      set({
        error: error instanceof Error ? error.message : 'Failed to generate AI dashboard',
        isGeneratingAI: false,
      })
    }
  },

  approveAIDashboard: async (approved, feedback) => {
    set({ isLoading: true, error: null })
    try {
      await apiClient.approveDashboard({ approved, feedback })
      // Refresh current plan if we have one
      if (get().currentPlan) {
        await get().fetchPlan(get().currentPlan!.id)
      }
      set({ isLoading: false })
    } catch (error) {
      set({
        error: error instanceof Error ? error.message : 'Failed to approve dashboard',
        isLoading: false,
      })
    }
  },

  clearError: () => set({ error: null }),

  reset: () => set({
    plans: [],
    currentPlan: null,
    tasks: [],
    isLoading: false,
    error: null,
    isGeneratingAI: false,
  }),
}))